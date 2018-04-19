# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class CustomSignupForm(SignupForm):
    role = forms.CharField(widget=forms.Select(choices=User.ROLES))
