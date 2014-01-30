import json
from datetime import date, timedelta

from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from observations.models import Telescope, Night, Exposure
from django.contrib.auth.models import User

# import account.views
# import observations.forms


# class SignupView(account.views.SignupView):

#     form_class = observations.forms.SignupForm

#     def after_signup(self, form):
#         self.create_profile(form)
#         super(SignupView, self).after_signup(form)

#     def create_profile(self, form):
#         profile = self.created_user.get_profile()
#         profile.public_homepage = form.cleaned_data["public_homepage"]
#         profile.save()


def user_view(request, username):
    """A user's home page."""
    user = get_object_or_404(User, username=username)
    return render(request, 'observations/user_home.html',
                  {'viewed_username': username,
                   'login_username': request.user.username})

def night_view(request, name, year, month, day):
    """A specific night on a specific telescope."""
    check_telescope_name(name)
    data_query = (
        'telescope_name:"%s", year:"%s", month:"%s", day:"%s"' % 
        (name, year, month, day))
    return render(request, 'observations/observations.html',
                  {'data_query': data_query})

def month_view(request, name, year, month):
    """A specific month on a specific telescope."""
    check_telescope_name(name)
    data_query = (
        'telescope_name:"%s", year:"%s", month:"%s"' % 
        (name, year, month))
    return render(request, 'observations/observations.html',
                  {'data_query': data_query})

def year_view(request, name, year):
    """A specific year on a specific telescope."""
    check_telescope_name(name)
    data_query = (
        'telescope_name:"%s", year:"%s"' % 
        (name, year))
    return render(request, 'observations/observations.html',
                  {'data_query': data_query})

def telescope_view(request, name):
    """All observations on a specific telescope."""
    check_telescope_name(name)
    data_query = (
        'telescope_name:"%s"' % name)
    return render(request, 'observations/observations.html',
                  {'data_query': data_query})

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

def getdata(request):
    filter_dict = {}
    get = request.GET
    if 'telescope_name' in get:
        filter_dict['night__instrument__telescope__name'] = (
            get['telescope_name'])
    if 'year' in get:
        filter_dict['night__ut_date__year'] = int(get['year'])
    if 'month' in get:
        filter_dict['night__ut_date__month'] = int(get['month'])
    if 'day' in get:
        filter_dict['night__ut_date__day'] = int(get['day'])
    filter_dict['object_exp'] = True
    exposure_list = Exposure.objects.filter(**filter_dict)
    exposure_json = json.dumps(
        [{'ra':e.ra, 'dec':e.dec, 'exposed':e.exposed, 
          'instrument_name':e.night.instrument.name} for e in exposure_list])
    return HttpResponse(exposure_json, content_type="application/json")
