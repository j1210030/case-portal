# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from django.forms.models import model_to_dict, fields_for_model
from django.conf import settings
from django.utils import timezone
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.core.validators import validate_ipv46_address,RegexValidator
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField
from django.contrib.contenttypes.models import ContentType

import sys
import os
import pprint
import logging
import re
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta 
import uuid
import time
import json

log = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)
#now = datetime.datetime.now()

blank_choice = (('', 'Select'))

"""
Validate a Phone Number separated with allowed Plus(+), Hyphen (-) or Dot(.) 
e.g 03-7821-2345 or 91.8282.123 or +54-45-1863-1236
"""
def validate_phone_number(value=None):
    if value:
        return True
        if not re.match('^[0-9.-/\+ ]+$',value):
            raise ValidationError('Invalid phone number')

"""
Validate Alphanumeric
"""
def validate_alphanum(value=None):
    if value:
        if not re.match('^[a-zA-Z0-9 ]+$',value):
            raise ValidationError('Only alpha numeric is allowed')

"""
Validate a ASCII 
"""            
def validate_ascii(value=None):
    if value:
        try:
            value.decode('ascii')
        except UnicodeDecodeError:
            raise ValidationError(_('txt_invalid_value') )


def get_date_diff(start,end):
    diff_str=''
    if start is None:
        start = datetime.today()
    diff = relativedelta.relativedelta(start, end)
    if diff.years > 0:
        diff_str='%dY ' % diff.years
    if diff.months >0:
        diff_str ='%s%sM ' % (diff_str,diff.months)
    if diff.days >0:
        diff_str ='%s%sD ' % (diff_str,diff.days)
   
    return diff_str

