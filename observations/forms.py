from django import forms

import account.forms


class SignupForm(account.forms.SignupForm):

    public_homepage = forms.BooleanField()
