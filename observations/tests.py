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

