# -*- coding: utf-8 -*-
"""
@note: This is the model class for gCases
"""
from .common_models import *
from django.contrib import admin
from datetime import datetime
from django.utils import timezone
from django.utils.regex_helper import Choice

from gcase.models import Product, GcaseUser

log = logging.getLogger(__name__)


class IndividualReport(models.Model):   

    week = models.DateField (blank=False,max_length=20,verbose_name='Incoming week')
    #product = models.ForeignKey(Product,blank=True,null=True,verbose_name="Product")
    gcase_user = models.ForeignKey(GcaseUser,blank=False,null=False,verbose_name="Assignee")
    pw_backlog = models.IntegerField(blank=True,null=True)
    incoming = models.IntegerField(blank=True,null=True)
    incoming_partner = models.IntegerField(blank=True,null=True)
    so = models.IntegerField(blank=True,null=True)
    so_partner = models.IntegerField(blank=True,null=True)
    
    def __unicode__(self):
        return u'%s' % (self.week)
    
    def get_backlog(self):
        return ( self.pw_backlog + self.incoming) - self.so

    class Meta:
        app_label = 'gcase'
        db_table = 'individual_report'