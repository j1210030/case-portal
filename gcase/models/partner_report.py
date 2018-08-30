# -*- coding: utf-8 -*-
"""
@note: This is the model class for gCases
"""
from .common_models import *
from django.contrib import admin
from datetime import datetime
from django.utils import timezone
from django.utils.regex_helper import Choice

from gcase.models import Product, Partner

log = logging.getLogger(__name__)


class PartnerReport(models.Model):   

    year = models.IntegerField (blank=False,verbose_name='Year')
    month = models.IntegerField (blank=False,verbose_name='Month')
    product = models.ForeignKey(Product,blank=False,verbose_name="Product")
    partner = models.ForeignKey(Partner,blank=False,verbose_name="Partner")
    case_count = models.IntegerField(blank=False,verbose_name="Case count")
    month_dt = models.DateField(blank=False,verbose_name="Month date")
    class Meta:
        app_label = 'gcase'
        db_table = 'partner_report'