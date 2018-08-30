# -*- coding: utf-8 -*-
import pprint
import logging
from django.conf import settings
from django import forms
from django.forms import widgets
from django.forms.models import model_to_dict
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelChoiceField
from django.contrib.admin import widgets 

blank_choice = (('', 'Select'),)
        