# -*- coding: utf-8 -*-
"""
@note: This is the model class for User
@file: gcase_user.py
"""
from .common_models import *

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers  import *
from django.core.validators import RegexValidator

from django.forms.models import model_to_dict, fields_for_model
from datetime import datetime
from django.utils import timezone

log = logging.getLogger(__name__)

class GcaseUser(models.Model):
    
    #user = models.OneToOneField(User, on_delete=models.CASCADE,related_name = 'users')
    user = models.ForeignKey(User,blank=True,null=True,verbose_name="Assignee")
    profile_pict = models.ImageField(blank=True,verbose_name="Profile photo")
    date_released  = models.DateTimeField(auto_now_add=False,blank=True,verbose_name='Date of release')  
    gender = models.CharField(choices=settings.GENDER_CHOICES,blank=False,max_length=10,verbose_name="Gender")
    case_handler = models.NullBooleanField(verbose_name='Case handler?') 
    
    def __unicode__(self):
        return u'%s %s' % (self.user.first_name,self.user.last_name)
    
    class Meta:
         app_label = 'gcase' 
         db_table  = 'gcase_users'
         verbose_name='gCase user'
         verbose_name_plural = 'gCase users'
         
#@receiver(post_save, sender=User)
#def update_user_profile(sender, instance, created, **kwargs):
   # if created:
    #    GcaseUser.objects.create(user=instance)
    #instance.gcase_user.save()
