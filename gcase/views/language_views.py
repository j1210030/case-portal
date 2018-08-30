# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from gcase.models import LanguageReport
from django.utils.functional import lazy
from gcase.forms import CaseAddEditForm
from django.db import DatabaseError
from itertools import chain
from datetime import timedelta
from django.http import StreamingHttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Avg, Max, Min
#import unicodecsv as csv
import csv
from io import TextIOWrapper, StringIO
from io import BytesIO
import sys;
from django.template.defaultfilters import default
from django.db.models.query import prefetch_related_objects
log = logging.getLogger(__name__)
from gcase.views.period_set_views import PeriodSetView

class LanguageReportView(PeriodSetView):
    
    template_name='gcase/report/language.html'
    context_dict = {}
    
    def get(self, request):
        self. context_dict = {}
        data=request.GET.copy()
        self.context_dict = self.set_duration(data, self.context_dict, -1)
        date_filter = self.set_date_filter(data,'week')
        self.context_dict['period'] = '( %04s/%02s ~ %04s/%02s )' % (data['from_year'],data['from_month'],data['to_year'],data['to_month'])
        
        self.context_dict['view_name'] = 'report'
        self.context_dict['action'] = 'language'

       
        backlog_list = None
        total_list = None
        
        
        total_list = []
        language_report_android = []
        language_report_firebase = []
        
        try:
            kwargs = {}
            args = ()
            
            week_list = LanguageReport.objects.values('week').distinct().filter(date_filter, *args, **kwargs).order_by('-week')
                
            total_list = self.get_language_total(date_filter, 'desc')
        
            log.info(total_list)
            
            data = self.get_language_report_by_product(date_filter, 'desc')#LanguageReport.objects.filter(date_filter, *args, **kwargs).order_by('-week','language')

            self.context_dict['week_list'] = week_list
            #self.context_dict['languages'] = languages
            
            for item in data:
            
                if item.product_id == 1:
                    language_report_android.append(item)    
                if item.product_id == 2:    
                    language_report_firebase.append(item)

            self.context_dict['language_report_android'] = language_report_android    
            self.context_dict['language_report_firebase'] = language_report_firebase  
            self.context_dict['total_list'] = total_list 
            
            log.info(' Android len: %d ' % len(language_report_android))

        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
        #else:    
            #return backlog_list
        
        return render(request, self.template_name,self.context_dict)
    
    def get_language_report_by_product(self, date_filter, order):
        
         if order == 'asc':
            order = 'week'
         else:
             order = '-week'
         
         try:
            kwargs = {}
            args = ()
            data = LanguageReport.objects.filter(date_filter, *args, **kwargs).order_by(order,'language')
            return data
        
         except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
            return None
         

    def get_language_total(self, date_filter,order):
        
         if order == 'asc':
            order = 'week'
         else:
             order = '-week'
         
         try:
            kwargs = {}
            args = ()
        
            total_list = LanguageReport.objects.filter(date_filter, *args, **kwargs).values('week','language').\
                            annotate(total_incoming=Sum('incoming'),total_incoming_partner=Sum('incoming_partner'),
                                     total_so=Sum('so'), total_forwarded=Sum('forwarded')\
                                     ).order_by(order,'language')
            return total_list
        
         except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
            return None