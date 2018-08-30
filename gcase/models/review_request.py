# -*- coding: utf-8 -*-
"""
@note: This is the model class for gCases
"""
from .common_models import *
from django.contrib import admin
from datetime import datetime
from django.utils import timezone
from django.utils.regex_helper import Choice

from gcase.models import Case

log = logging.getLogger(__name__)


class ReviewRequest(models.Model):   

    case = models.ForeignKey(Case,blank=True,null=True,verbose_name="Case")
    email_title = models.CharField(blank=True,max_length=200,verbose_name="Email title")
    requested_on = models.DateField(blank=True,verbose_name="Request date")
    request_week = models.DateField(blank=True,verbose_name="Request week")
    agent_remarks = models.TextField(blank=True, null=True, max_length=1024,verbose_name="Agent's Remarks")
    da_feedback = models.TextField(blank=True, null=True, max_length=1024,verbose_name="DA's Remarks")
    feedback_received_on = models.DateField(blank=True,verbose_name="Feedback received date")
    received_week = models.DateField(blank=True,verbose_name="Feedback week")
    status = models.CharField(blank=True,null=False,max_length=20, choices=settings.CASE_REVIEW_STATUS_CHOICES,verbose_name='Review Status')  
   
    class Meta:
        app_label = 'gcase'
        db_table = 'review_request'