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
        populate_database('super_big_telescope', 'awesome_instrument')
        populate_database('really_big_telescope', 'excellent_instrument')
        response = self.client.get(reverse(
            'observations:telescope', args=('super_big_telescope',)))
        exposure_list = expected_exposure_list('super_big_telescope')
        self.assertQuerysetEqual(response.context['exposure_list'], 
                                 exposure_list)

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
