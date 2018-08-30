# -*- coding: utf-8 -*-
"""
@note: This is the model class for Components of a product
@file: component.py
"""
from .common_models import *
from django.contrib import admin
from datetime import datetime
from django.utils import timezone
from gcase.models import Product

log = logging.getLogger(__name__)

class Component(models.Model):
    
    name = models.CharField(blank=False,max_length=50,verbose_name='Name')
    product = models.ForeignKey(Product,blank=False,verbose_name="Product")
    active = models.NullBooleanField(verbose_name='Active?')   
    created  = models.DateTimeField(auto_now_add=False,blank=True,verbose_name='Added on')    
    modified  = models.DateTimeField(auto_now=True,null=True,blank=True,verbose_name='Modified')
    
    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        app_label = 'gcase'
        db_table = 'components'

"""
Partner Admin
"""
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','name','active')
    list_display_links = ('__unicode__',)
    search_fields = ['name']

    class Meta:
        model = Component

admin.site.register(Component, ComponentAdmin)
