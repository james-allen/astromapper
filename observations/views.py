import json
from datetime import date, timedelta
from calendar import monthrange

from django.http import Http404
from django.shortcuts import render

from observations.models import Telescope, Instrument, Night, Exposure

def night(request, name, year, month, day):
    """A specific night on a specific telescope."""
    check_telescope_name(name)
    date_obs = date(int(year), int(month), int(day))
    night_list = Night.objects.filter(
        instrument__telescope__name=name, ut_date=date_obs)
    return render_night_list(request, night_list)

def month(request, name, year, month):
    """A specific month on a specific telescope."""
    check_telescope_name(name)
    first_date = date(int(year), int(month), 1)
    last_date = date(int(year), int(month), monthrange(int(year), int(month))[1])
    return render_night_range(request, first_date, last_date, name)

def year(request, name, year):
    """A specific year on a specific telescope."""
    check_telescope_name(name)
    first_date = date(int(year), 1, 1)
    last_date = date(int(year), 12, 31)
    return render_night_range(request, first_date, last_date, name)

def telescope(request, name):
    """All observations on a specific telescope."""
    check_telescope_name(name)
    night_list = Night.objects.filter(
        instrument__telescope__name=name)
    return render_night_list(request, night_list)

def render_night_range(request, first_date, last_date, name):
    night_list = []
    current_date = first_date
    while current_date <= last_date:
        night_list.extend(Night.objects.filter(
            instrument__telescope__name=name, ut_date=current_date))
        current_date += timedelta(days=1)
    return render_night_list(request, night_list)

def render_night_list(request, night_list):
    instrument_name_set = {n.instrument.name for n in night_list}
    exposure_list = []
    for n in night_list:
        exposure_list.extend(e for e in Exposure.objects.filter(night=n)
                             if e.object_exp)
    exposure_dict_list = [
        {'ra':e.ra, 'dec':e.dec, 'exposed':e.exposed, 
         'instrument_name':e.night.instrument.name} for e in exposure_list]
    exposure_json = json.dumps(
        [{'ra':e.ra, 'dec':e.dec, 'exposed':e.exposed, 
          'instrument_name':e.night.instrument.name} for e in exposure_list])
    return render(request, 'observations/observations.html',
                  {'instrument_name_set': instrument_name_set,
                   'exposure_list': exposure_json})

def check_telescope_name(name):
    """
    Check that a telescope exists, and raise a 404 if it doesn't. Returns
    True if the telescope does exist.
    """
    try:
        Telescope.objects.get(name=name)
    except Telescope.DoesNotExist:
        raise Http404
    return True
