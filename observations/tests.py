from calendar import monthrange
from datetime import date, time

from django.test import TestCase
from django.core.urlresolvers import reverse

from observations.models import Telescope, Instrument, Night, Exposure

class ObservationsViewTests(TestCase):
    def test_view_nonexistent_telescope(self):
        """
        If a telescope that doesn't exist is requested, give a 404.
        """
        # Put a telescope with a different name in there
        Telescope.objects.create(
            name='really_big_telescope', latitude=25.0, longitude=45.0)
        response = self.client.get(reverse(
            'observations:telescope', args=('super_big_telescope',)))
        self.assertEqual(response.status_code, 404)

    def test_view_nonexistent_telescope_year(self):
        """
        If a telescope that doesn't exist is requested, give a 404.
        """
        # Put a telescope with a different name in there
        Telescope.objects.create(
            name='really_big_telescope', latitude=25.0, longitude=45.0)
        response = self.client.get(reverse(
            'observations:year', args=('super_big_telescope','2013')))
        self.assertEqual(response.status_code, 404)

    def test_view_nonexistent_telescope_month(self):
        """
        If a telescope that doesn't exist is requested, give a 404.
        """
        # Put a telescope with a different name in there
        Telescope.objects.create(
            name='really_big_telescope', latitude=25.0, longitude=45.0)
        response = self.client.get(reverse(
            'observations:month', args=('super_big_telescope','2013','12')))
        self.assertEqual(response.status_code, 404)

    def test_view_nonexistent_telescope_night(self):
        """
        If a telescope that doesn't exist is requested, give a 404.
        """
        # Put a telescope with a different name in there
        Telescope.objects.create(
            name='really_big_telescope', latitude=25.0, longitude=45.0)
        response = self.client.get(reverse(
            'observations:night', 
            args=('super_big_telescope','2013','12','1')))
        self.assertEqual(response.status_code, 404)

    def test_view_telescope(self):
        """
        Test which exposures are returned when a telescope is selected.
        """
        telescope_name = 'super_big_telescope'
        instrument_name = 'awesome_instrument'
        create_exposures(telescope_name, instrument_name, 2012, 6, 1)
        create_exposures(telescope_name, instrument_name, 2013, 7, 1)
        expected_exposures = [
            '<Exposure: %s 2012/06/01 run 1>' % telescope_name,
            '<Exposure: %s 2012/06/01 run 2>' % telescope_name,
            '<Exposure: %s 2013/07/01 run 1>' % telescope_name,
            '<Exposure: %s 2013/07/01 run 2>' % telescope_name,
            ]
        response = self.client.get(reverse(
            'observations:telescope', args=('super_big_telescope',)))
        self.assertQuerysetEqual(response.context['exposure_list'], 
                                 expected_exposures)

    def test_view_telescope_year(self):
        """
        Test which exposures are returned when a telescope and year are
        selected.
        """
        telescope_name = 'super_big_telescope'
        instrument_name = 'awesome_instrument'
        create_exposures(telescope_name, instrument_name, 2012, 12, 31)
        create_exposures(telescope_name, instrument_name, 2013, 1, 1)
        create_exposures(telescope_name, instrument_name, 2013, 12, 31)
        create_exposures(telescope_name, instrument_name, 2014, 1, 1)
        expected_exposures = [
            '<Exposure: %s 2013/01/01 run 1>' % telescope_name,
            '<Exposure: %s 2013/01/01 run 2>' % telescope_name,
            '<Exposure: %s 2013/12/31 run 1>' % telescope_name,
            '<Exposure: %s 2013/12/31 run 2>' % telescope_name,
            ]
        response = self.client.get(reverse(
            'observations:year', args=('super_big_telescope','2013')))
        self.assertQuerysetEqual(response.context['exposure_list'], 
                                 expected_exposures)

    def test_view_telescope_month(self):
        """
        Test which exposures are returned when a telescope and month are
        selected.
        """
        telescope_name = 'super_big_telescope'
        instrument_name = 'awesome_instrument'
        create_exposures(telescope_name, instrument_name, 2013, 3, 31)
        create_exposures(telescope_name, instrument_name, 2013, 4, 1)
        create_exposures(telescope_name, instrument_name, 2013, 4, 30)
        create_exposures(telescope_name, instrument_name, 2013, 5, 1)
        expected_exposures = [
            '<Exposure: %s 2013/04/01 run 1>' % telescope_name,
            '<Exposure: %s 2013/04/01 run 2>' % telescope_name,
            '<Exposure: %s 2013/04/30 run 1>' % telescope_name,
            '<Exposure: %s 2013/04/30 run 2>' % telescope_name,
            ]
        response = self.client.get(reverse(
            'observations:month', args=('super_big_telescope','2013','4')))
        self.assertQuerysetEqual(response.context['exposure_list'], 
                                 expected_exposures)

    def test_view_telescope_december(self):
        """
        Test which exposures are returned when a telescope and month are
        selected, for the slightly special case of December.
        """
        telescope_name = 'super_big_telescope'
        instrument_name = 'awesome_instrument'
        create_exposures(telescope_name, instrument_name, 2013, 11, 30)
        create_exposures(telescope_name, instrument_name, 2013, 12, 1)
        create_exposures(telescope_name, instrument_name, 2013, 12, 31)
        create_exposures(telescope_name, instrument_name, 2014, 1, 1)
        expected_exposures = [
            '<Exposure: %s 2013/12/01 run 1>' % telescope_name,
            '<Exposure: %s 2013/12/01 run 2>' % telescope_name,
            '<Exposure: %s 2013/12/31 run 1>' % telescope_name,
            '<Exposure: %s 2013/12/31 run 2>' % telescope_name,
            ]
        response = self.client.get(reverse(
            'observations:month', args=('super_big_telescope','2013','12')))
        self.assertQuerysetEqual(response.context['exposure_list'], 
                                 expected_exposures)

    def test_view_telescope_night(self):
        """
        Test which exposures are returned when a telescope and night are
        selected.
        """
        telescope_name = 'super_big_telescope'
        instrument_name = 'awesome_instrument'
        create_exposures(telescope_name, instrument_name, 2013, 8, 5)
        create_exposures(telescope_name, instrument_name, 2013, 8, 6)
        create_exposures(telescope_name, instrument_name, 2013, 8, 7)
        expected_exposures = [
            '<Exposure: %s 2013/08/06 run 1>' % telescope_name,
            '<Exposure: %s 2013/08/06 run 2>' % telescope_name,
            ]
        response = self.client.get(reverse(
            'observations:night', args=('super_big_telescope','2013','8','6')))
        self.assertQuerysetEqual(response.context['exposure_list'], 
                                 expected_exposures)

def create_exposures(telescope_name, instrument_name, year_int, month_int, 
                     night_int):
    """
    Put two object exposures and one calibration exposure on the given
    night for the specified telescope/instrument.
    """
    # Use an existing telescope if available, or create it
    try:
        telescope = Telescope.objects.get(name=telescope_name)
    except Telescope.DoesNotExist:
        telescope = Telescope.objects.create(
            name=telescope_name, latitude=25.0, longitude=45.0)
    # Use an existing instrument if available, or create it
    try:
        instrument = Instrument.objects.get(
            name=instrument_name, telescope=telescope)
    except Instrument.DoesNotExist:
        instrument = Instrument.objects.create(
            name=instrument_name, telescope=telescope)
    # Use an existing night if available, or create it
    ut_date = date(year_int, month_int, night_int)
    try:
        night = Night.objects.get(
            instrument=instrument, ut_date=ut_date)
    except Night.DoesNotExist:
        night = Night.objects.create(
            instrument=instrument, ut_date=ut_date)
    # Make the three exposures
    Exposure.objects.create(
        night=night, run_number=1, ut_start=time(10, 0, 0),
        exposed=20.0, ra=60.0, dec=30.0, object_exp=True)
    Exposure.objects.create(
        night=night, run_number=2, ut_start=time(11, 0, 0),
        exposed=30.0, ra=90.0, dec=0.0, object_exp=True)
    Exposure.objects.create(
        night=night, run_number=3, ut_start=time(12, 0, 0),
        exposed=40.0, ra=120.0, dec=-30.0, object_exp=False)


def populate_database(telescope_name, instrument_name):
    """
    Put two object exposures and one calibration exposure on the first and
    last of each month in 2012 and 2013, for the given instrument and
    telescope names.
    """
    telescope = Telescope.objects.create(
        name=telescope_name, latitude=25.0, longitude=45.0)
    instrument = Instrument.objects.create(
        name=instrument_name, telescope=telescope)
    for year_int in (2012, 2013):
        for month_int in range(1, 13):
            for night_int in (1, monthrange(year_int, month_int)[1]):
                ut_date = date(year_int, month_int, night_int)
                night = Night.objects.create(
                    ut_date=ut_date, instrument=instrument, observers='Smith')
                Exposure.objects.create(
                    night=night, run_number=1, ut_start=time(10, 0, 0),
                    exposed=20.0, ra=60.0, dec=30.0, object_exp=True)
                Exposure.objects.create(
                    night=night, run_number=2, ut_start=time(11, 0, 0),
                    exposed=30.0, ra=90.0, dec=0.0, object_exp=True)
                Exposure.objects.create(
                    night=night, run_number=3, ut_start=time(12, 0, 0),
                    exposed=40.0, ra=120.0, dec=-30.0, object_exp=False)
                
def expected_exposure_list(telescope_name, year=None, month=None, 
                           night=None):
    """
    Return the expected list of exposures given the database populated as
    above.
    """
    exposure_list = []
    if year is None:
        year_range = (2012, 2013)
    else:
        year_range = (year,)
    for year_int in year_range:
        if month is None:
            month_range = range(1, 13)
        else:
            month_range = (month,)
        for month_int in month_range:
            if night is None:
                night_range = (1, monthrange(year_int, month_int)[1])
            else:
                night_range = (night,)
            for night_int in night_range:
                for run_number in (1, 2):
                    exposure_list.append(
                        '<Exposure: %s %04i/%02i/%02i run %i>' %
                        (telescope_name, year_int, month_int, night_int, 
                         run_number))
    return exposure_list                    
