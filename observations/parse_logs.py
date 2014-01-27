from datetime import date, time
from operator import itemgetter
import re

from django.core.files import File
from django.db import IntegrityError

#import pytz
from astropy.coordinates.angles import Angle
from astropy.units import UnitsError

from observations.models import Telescope, Instrument, Night, Exposure

def parse_aat_log(log_file_path):
    """
    Reads a log file and adds the relevant night and exposures to the
    database, as well as instrument if it's new.
    """
    # REPLACE STRING CRUD WITH REGEX
    with open(log_file_path) as log_file:
        # This is for the AAT only
        aat = Telescope.objects.get(name='AAT')
        # First look for the UT date and instrument name
        line = '\n'
        while line != '' and not line.startswith('UT Date'):
            line = log_file.readline()
        if line == '':
            # The file didn't match the expected format; no UT date found
            raise IOError("File is not a valid AAT log file")
        # `line` should look like "UT Date : 2013-12-31     INSTRUMENT NAME"
        data = line[line.index(':')+1:].split()
        ut_date_str = data[0]
        ut_date = date(int(ut_date_str[:4]), int(ut_date_str[5:7]), 
                       int(ut_date_str[8:10]))
        instrument_name = ' '.join(data[1:])
        try:
            # Identify the instrument by name
            instrument = Instrument.objects.get(
                telescope=aat, name=instrument_name)
        except Instrument.DoesNotExist:
            # Make a new instrument with this name
            instrument = Instrument(telescope=aat, name=instrument_name)
            instrument.save()
        # Then look for the observers' names
        while line != '' and 'Observers' not in line:
            line = log_file.readline()
        if line == '':
            # The file didn't match the expected format; no observers found
            raise IOError("File is not a valid AAT log file")
        # `line` should look like 
        # "Session : A  Top End : 2DF     Observers : CLEESE, PALIN"
        observers = ' '.join(line[line.index('Observers')+11:].split())
        # We now have all the necessary data to make the night
        night = Night(instrument=instrument, ut_date=ut_date, observers=observers,
                      log_file=File(open(log_file_path)))
        try:
            night.save()
        except IntegrityError:
            # This night has already been processed. Abandon ship!
            return
        # Look for the column headers
        while line != '' and not line.startswith('Run'):
            line = log_file.readline()
        if line == '':
            # The file didn't match the expected format; no table found
            raise IOError("File is not a valid AAT log file")
        # Get the regex to match all the data
        regex = regex_for_data_line(line)
        # Parse the data line by line
        for line in log_file:
            parse_line(line, regex, night)
    return

def regex_for_data_line(column_headers):
    """
    Return a regular expression that will pick out the useful information
    from a line of a log file, based on the positions of the column headers.
    """
    # Each of the following dicts gives a column header that we want to
    # extract, and the name to give it in the regex
    useful_columns = [{'header':'Run', 'name':'run_number'},
                      {'header':'Object', 'name':'object_exp'},
                      {'header':'RA (J2000)', 'name':'ra'},
                      {'header':'Dec (J2000)', 'name':'dec'},
                      {'header':'UT start', 'name':'ut_start'},
                      {'header':'Exposed', 'name':'exposed'}]
    for column in useful_columns:
        # Find the start and finish positions of this column, and add them to
        # the dict
        start = column_headers.index(column['header'])
        finish = (len(column_headers) - 
                  len(column_headers[start+len(column['header']):].lstrip()))
        column['start'] = start
        column['finish'] = finish
    # Construct the regex piece by piece
    position = 0
    regex = '^'
    for column in sorted(useful_columns, key=itemgetter('start')):
        if column['start'] > position:
            # Add in some filler, for columns we're not interested in
            regex += r'(.){%i}' % (
                column['start'] - position)
        # Add in this column
        regex += r'(?P<%s>.{%i})' % (
            column['name'], column['finish'] - column['start'])
        # Update the position
        position = column['finish']
    return regex

def parse_line(line, regex, night):
    """
    Extract data from a single line of a log file and make a new Exposure
    object to describe it, unless a matching Exposure already exists.
    """
    if ' Comment ' in line:
        return
    match = re.match(regex, line)
    if match:
        # First parse the run number only
        run_number = parse_run_number(match.group('run_number'))
        # Check if this exposure has already been entered into the database
        try:
            existing_exposure = Exposure.objects.get(
                night=night, run_number=run_number)
        except Exposure.DoesNotExist:
            # Carry on with extracting the data
            pass
        else:
            # An exposure with this night and run number already exists
            return
        # Parse each header item individually
        object_exp = parse_object_exp(match.group('object_exp').strip())
        ra = parse_ra(match.group('ra').strip())
        dec = parse_dec(match.group('dec').strip())
        ut_start = parse_ut_start(match.group('ut_start').strip())
        exposed = parse_exposed(match.group('exposed').strip())
        # Put all the data into an Exposure object and save it
        exposure = Exposure(
            night=night,
            run_number=run_number,
            object_exp=object_exp,
            ra=ra,
            dec=dec,
            ut_start=ut_start,
            exposed=exposed)
        exposure.save()
    return

def parse_run_number(run_number_str):
    """Parse a run number string."""
    return int(run_number_str)

def parse_object_exp(object_exp_str):
    """Parse an object exposure string."""
    lowercase = object_exp_str.lower()
    return ('flat' not in lowercase and
            'arc' not in lowercase and
            'offset sky' not in lowercase and
            'cuar' not in lowercase and
            'fear' not in lowercase and
            'cuhe' not in lowercase and
            'cune' not in lowercase and
            'thar' not in lowercase and
            'bias' not in lowercase and
            'dark' not in lowercase)

def parse_ra(ra_str):
    """Parse an RA string."""
    # See if the string provides enough details for astropy to work it out
    try:
        angle = Angle(ra_str)
    except UnitsError:
        # If the string is a decimal number, assume degrees
        # Otherwise, assume hours
        if re.match(r'\d+\.\d*', ra_str):
            angle = Angle(ra_str+' degrees')
        else:
            angle = Angle(ra_str+' hours')
    return angle.degree

def parse_dec(dec_str):
    """Parse a Dec string."""
    # See if the string provides enough details for astropy to work it out
    try:
        angle = Angle(dec_str)
    except UnitsError:
        # Assume the units are degrees
        angle = Angle(dec_str+' degrees')
    return angle.degree

def parse_ut_start(ut_start_str):
    """Parse a UT start time string."""
    # return pytz.timezone('UTC').localize(time(
    #     int(ut_start_str[:2]), int(ut_start_str[3:5]), int(ut_start_str[6:8])))
    return time(
        int(ut_start_str[:2]), 
        int(ut_start_str[3:5]), 
        int(float(ut_start_str[6:8])))

def parse_exposed(exposed_str):
    """Parse an exposure time string."""
    return float(exposed_str)
