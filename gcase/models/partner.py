# -*- coding: utf-8 -*-
"""
@note: This is the model class for Partner
@file: partner.py
"""
from .common_models import *
from django.contrib import admin
from datetime import datetime
from django.utils import timezone

log = logging.getLogger(__name__)

class Partner(models.Model):
    
    name_english = models.CharField(blank=False,max_length=256,verbose_name='Name(English)')
    name_locale = models.CharField(blank=False,max_length=256,verbose_name='Name(Locale)')
    geo_location = models.CharField(blank=False,null=False,max_length=2, choices=settings.GEO_LOCATION_CHOICES,verbose_name='Geo location')
    company_url = models.URLField(max_length=256,blank=True,verbose_name='Company web site')
    is_active = models.NullBooleanField(verbose_name='Active?')   
    created  = models.DateField(auto_now_add=False,blank=True,verbose_name='Added on')    
    modified  = models.DateTimeField(auto_now=True,null=True,blank=True,verbose_name='Modified')
    remarks  = models.CharField(max_length=255,help_text='255 characters max.',blank=True)
    
    def __unicode__(self):
        return u'%s' % (self.name_english)

    class Meta:
        app_label = 'gcase'
        db_table = 'partners'

"""
Partner Admin
"""
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','name_locale','geo_location','company_url','is_active')
    list_display_links = ('__unicode__',)
    search_fields = ['name_english','name_locale','geo_location']

    class Meta:
        model = Partner

admin.site.register(Partner, PartnerAdmin)
