# -*- coding: utf-8 -*-
"""
@note: This is the model class for gCases
"""
from .common_models import *
from django.contrib import admin
from datetime import datetime
from django.utils import timezone
from django.utils.regex_helper import Choice

from gcase.models import Product, Component

log = logging.getLogger(__name__)


class ComponentReport(models.Model):   

    week = models.DateField (blank=False,max_length=20,verbose_name='Incoming week')
    product = models.ForeignKey(Product,blank=True,null=True,verbose_name="Product")
    component = models.ForeignKey(Component,blank=True,null=True,verbose_name="Component")
    incoming = models.IntegerField(blank=True,null=True)
    incoming_partner = models.IntegerField(blank=True,null=True)
   
    
    def __unicode__(self):
        return u'%s' % (self.week)

    class Meta:
        app_label = 'gcase'
        db_table = 'component_report'