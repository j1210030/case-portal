# -*- coding: utf-8 -*-
"""
@note: This is the model class for Components of a product
@file: component.py
"""
from .common_models import *
from django.contrib import admin
from datetime import datetime
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth.hashers  import *
from django.core.validators import RegexValidator

log = logging.getLogger(__name__)

class DpsMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(choices=settings.GENDER_CHOICES,blank=False,max_length=10,verbose_name="Gender")
    profile_photo = models.ImageField(blank=True,verbose_name="Profile photo")
    contact_number = models.CharField(blank=True,max_length=20,verbose_name="Mobile(Ph) no")
    date_resigned = models.DateTimeField(auto_now_add=False,blank=True,verbose_name='Resigned on')  
    
    def __unicode__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        app_label = 'gcase'
        db_table = 'dps_members'
