# -*- coding: utf-8 -*-
"""
@note: This is the model class for gCases
"""
from .common_models import *
from django.contrib import admin
from datetime import datetime
from django.utils import timezone
from django.utils.regex_helper import Choice

from gcase.models import Product

log = logging.getLogger(__name__)


class BacklogReport(models.Model):   

    week = models.DateField (blank=False,max_length=20,verbose_name='Incoming week')
    product = models.ForeignKey(Product,blank=True,null=True,verbose_name="Product")
    incoming = models.IntegerField(blank=True,null=True)
    incoming_partner = models.IntegerField(blank=True,null=True)
    incoming_percent = models.DecimalField(blank=True,null=True, max_digits=5, decimal_places=2)
    so = models.IntegerField(blank=True,null=True)
    so_partner = models.IntegerField(blank=True,null=True)
    so_percent = models.DecimalField(blank=True, max_digits=5, decimal_places=2)
    forwarded = models.IntegerField(blank=True,null=True)
    assigned = models.IntegerField(blank=True,null=True)
    inconsult = models.IntegerField(blank=True,null=True)
    needinfo = models.IntegerField(blank=True,null=True)
    blocked = models.IntegerField(blank=True,null=True)
    review_requested =  models.IntegerField(blank=True,null=True)
    pw_backlog =  models.IntegerField(blank=True,null=True)
      
    def __unicode__(self):
        return u'%s' % (self.week)
    
    def get_backlog(self):
        return (self.assigned + self.needinfo + self.blocked + self.review_requested + self.inconsult) 
    
    class Meta:
        app_label = 'gcase'
        db_table = 'backlog_report'
