# -*- coding: utf-8 -*-
"""
@note: This is the model class for review request report
"""
from .common_models import *
from django.contrib import admin
from datetime import datetime
from django.utils import timezone
from django.utils.regex_helper import Choice

from gcase.models import Product

log = logging.getLogger(__name__)

class ReviewRequestReport(models.Model):   
    
    week = models.DateField (blank=False,max_length=20,verbose_name='Week')
    product = models.ForeignKey(Product,blank=True,null=True,verbose_name="Product")
    total_requested = models.IntegerField(blank=True,null=True)
    ok_count = models.IntegerField(blank=True,null=True)
    ng_count = models.IntegerField(blank=True,null=True)
    ok_ratio = models.IntegerField(blank=True,null=True)
    monthly_ratio = models.IntegerField(blank=True,null=True)
    
    def __unicode__(self):
        return u'%s' % (self.week)
    
    class Meta:
        app_label = 'gcase'
        db_table = 'review_request_report'
