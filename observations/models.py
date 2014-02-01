from django.db import models
from django.contrib.auth.models import User

def log_file_path(night, filename):
    telescope_name = night.instrument.telescope.name
    date = night.ut_date
    return "log_files/%s/log_%s_%04i%02i%02i.txt" % (
        telescope_name, telescope_name, date.year, date.month, date.day)


class Telescope(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Instrument(models.Model):
    name = models.CharField(max_length=100)
    telescope = models.ForeignKey(Telescope)

    def __str__(self):
        return self.name


class Night(models.Model):
    instrument = models.ForeignKey(Instrument)
    ut_date = models.DateField('UT date')
    observers = models.CharField(max_length=100)
    log_file = models.FileField(upload_to=log_file_path)

    class Meta:
        unique_together = ('instrument', 'ut_date')

    def __str__(self):
        telescope_name = self.instrument.telescope.name
        date = self.ut_date
        return "%s %04i/%02i/%02i" % (
            telescope_name, date.year, date.month, date.day)


class Exposure(models.Model):
    night = models.ForeignKey(Night)
    run_number = models.IntegerField()
    ut_start = models.TimeField('UT start time')
    exposed = models.FloatField('Exposure time (s)')
    ra = models.FloatField('RA (J2000, decimal degrees)')
    dec = models.FloatField('Dec (J2000, decimal degrees)')
    object_exp = models.BooleanField('Object exposure?')

    class Meta:
        unique_together = ('night', 'run_number')

    def __str__(self):
        return "%s run %i" % (self.night, self.run_number)


class Query(models.Model):
    """Details of a query that has or could be made."""
    get_str = models.TextField()
    path = models.TextField()


# class Profile(models.Model):
#     """Extra information about a user, to extend built-in User class."""
#     user = models.OneToOneField(User)
#     queries = models.ManyToManyField(Query, through='QueryInstance')

#     def __str__(self):
#         return self.user.username


class QueryInstance(models.Model):
    """Links a Profile to a Query with a timestamp."""
    query = models.ForeignKey(Query)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField()

