# -*- coding: utf-8 -*-
"""
@note: This is the model class for gCases
"""
from .common_models import *
from django.contrib import admin
from datetime import datetime
from django.utils import timezone
from django.utils.regex_helper import Choice

from gcase.models import Product,Partner, Component, GcaseUser

log = logging.getLogger(__name__)


class Case(models.Model):   
    
    id = models.CharField(blank=False,max_length=15,primary_key=True, verbose_name='Case id')
    subject = models.CharField(blank=False,max_length=256,verbose_name='Subject')
    language = models.CharField(blank=False,null=False,max_length=3,choices=settings.LANGUAGE_CHOICES,verbose_name='Language')
    incoming_date = models.DateTimeField (blank=False,verbose_name='Incoming date')
    week = models.DateField (blank=False,max_length=20,verbose_name='Incoming week')
    status = models.CharField(blank=False,null=False,max_length=20, choices=settings.CASE_STATUS_CHOICES,verbose_name='Status')  
    so_date  = models.DateTimeField(blank=True,null=True,verbose_name='So date')
    so_week  = models.DateField(blank=True,null=True,verbose_name='So week')
    buganizer_number = models.CharField(blank=True,max_length=20,verbose_name='Buganizer number')
    difficulty_level = models.CharField(blank=False,null=False,max_length=20, choices=settings.CASE_DIFFICULTY_CHOICES,verbose_name='Difficulty')  
    partner = models.ForeignKey(Partner,blank=True,null=True,verbose_name="Partner")
    product = models.ForeignKey(Product,blank=True,null=True,verbose_name="Product")
    component = models.ForeignKey(Component,blank=True,null=True,verbose_name="Component")
    sub_product = models.CharField (blank=True,max_length=50 ,verbose_name='Sub product') # choices=settings.SUB_PRODUCT_CHOICES
    gcase_user = models.ForeignKey(GcaseUser,blank=False,null=False,verbose_name="Assignee")
    remarks = models.TextField(blank=True, null=True, max_length=1024,verbose_name="Remarks")
    created  = models.DateTimeField(auto_now_add=True,blank=False,verbose_name='Created')    
    modified  = models.DateTimeField(auto_now=True,null=True,blank=True,verbose_name='Modified')

    def __unicode__(self):
        return u'%s' % (self.subject)
    
    @property
    def get_age(self):
       return get_date_diff(None, self.incoming_date)

    class Meta:
        app_label = 'gcase'
        db_table = 'cases'

"""
Case Admin
"""
class CaseAdmin(admin.ModelAdmin):
    list_display = ('id','__unicode__','product','component','language','incoming_date','week')
    list_display_links = ('__unicode__',)
    search_fields = ['subject','language','incoming_date','product','component']

    class Meta:
        model = Case

admin.site.register(Case, CaseAdmin)
