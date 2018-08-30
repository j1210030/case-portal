# -*- coding: utf-8 -*-

from .common_views import *
from gcase.models import Case,Product, Component, GcaseUser, Partner
from django.utils.functional import lazy
from gcase.forms import CaseAddEditForm
from django.db import DatabaseError
from itertools import chain
from datetime import timedelta
from django.http import StreamingHttpResponse
from django.core.exceptions import ObjectDoesNotExist
#import unicodecsv as csv
import csv
from io import TextIOWrapper, StringIO
from io import BytesIO
import sys;
from django.template.defaultfilters import default
from django.db.models.query import prefetch_related_objects
from re import search
log = logging.getLogger(__name__)

class PeriodSetView(View):
    
    def set_duration(self, data, context_dict, offset):
            
        from_year = None
        from_month = None
        to_year = None
        to_month = None
        if offset is None:
            offset = -2
        
        if not data:
            now = datetime.now()
            from_year = now.year
            from_month = now.month
        
            toDt = add_month(offset)
        
            to_year = toDt.year;
            to_month = toDt.month
            data['from_year']= from_year
            data['from_month'] = from_month
            data['to_year'] = to_year
            data['to_month'] = to_month
        else:
            from_year = int(data['from_year'])
            from_month = int(data['from_month'])
            to_year = int(data['to_year'])
            to_month = int(data['to_month'])
        
        context_dict['month_options'] = set_month_options()
        context_dict['from_year_options'] = set_year_options()
        context_dict['to_year_options'] = set_year_options()
        
        context_dict['from_year'] = from_year
        context_dict['from_month'] = from_month;
        
        context_dict['to_year'] = to_year
        context_dict['to_month'] = to_month;
        
        return context_dict
    
    def set_date_filter(self,data, field):
        
        from_days = get_days_in_month( int(data['from_year']), int(data['from_month']))
        date_filter = Q()
        
        if field == 'incoming_date':
            from_dt = '%04d-%02d-%02d 23:59:59' % (int(data['from_year']), int(data['from_month']), from_days)
            until_dt = '%04d-%02d-01 00:00:00' % (int(data['to_year']), int(data['to_month']))
        
            from_dt = datetime.strptime(from_dt, '%Y-%m-%d %H:%M:%S') #23:59:59
            until_dt = datetime.strptime(until_dt, '%Y-%m-%d %H:%M:%S') # 00:00:00'
            
            date_filter = Q(incoming_date__lte = from_dt, incoming_date__gte = until_dt)
        
        if field == 'week':
            # 2017-12-31
            from_dt = '%04d-%02d-%02d' % (int(data['from_year']), int(data['from_month']), from_days)
            #2017-11-01
            until_dt = '%04d-%02d-01' % (int(data['to_year']), int(data['to_month']))
        
            from_dt = datetime.strptime(from_dt, '%Y-%m-%d') # Converting string to date type
            until_dt = datetime.strptime(until_dt, '%Y-%m-%d') 
            
            date_filter = Q(week__lte = from_dt, week__gte = until_dt)
            
            # week >= '2017-12-31' AND week<= '2017-11-01'
            
        if field == 'so_week':
            from_dt = '%04d-%02d-%02d' % (int(data['from_year']), int(data['from_month']), from_days)
            until_dt = '%04d-%02d-01' % (int(data['to_year']), int(data['to_month']))
        
            from_dt = datetime.strptime(from_dt, '%Y-%m-%d') #23:59:59
            until_dt = datetime.strptime(until_dt, '%Y-%m-%d') # 00:00:00'
            
            date_filter = Q(so_week__lte = from_dt, so_week__gte = until_dt)
        
        return date_filter