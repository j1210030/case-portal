# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from gcase.models import Case, Component
from django.utils.functional import lazy
from django.db import DatabaseError
from itertools import chain
from datetime import timedelta
from django.http import StreamingHttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Avg, Max, Min
from django.db.models.functions import TruncMonth
#import unicodecsv as csv
import csv
from io import TextIOWrapper, StringIO
from io import BytesIO
import math
import sys;
from django.template.defaultfilters import default
from django.db.models.query import prefetch_related_objects
from gcase.views.period_set_views import PeriodSetView

log = logging.getLogger(__name__)


class ComponentReportView(PeriodSetView):
    
    template_name='gcase/report/component/index.html'
    context_dict = {}
    
    def get(self, request):
       
        data=request.GET.copy()
        
        self.context_dict = self.set_duration(data, self.context_dict, -2)
        
        from_days = get_days_in_month( int(data['from_year']), int(data['from_month']))
        from_dt = '%04d-%02d-%02d 23:59:59' % (int(data['from_year']), int(data['from_month']), from_days)
        until_dt = '%04d-%02d-01 00:00:00' % (int(data['to_year']), int(data['to_month']))
        
        from_dt = datetime.strptime(from_dt, '%Y-%m-%d %H:%M:%S') #23:59:59
        until_dt = datetime.strptime(until_dt, '%Y-%m-%d %H:%M:%S') # 00:00:00'
            
        
        self.context_dict['view_name'] = 'report'
        self.context_dict['action'] = 'component'
       
        log.info(' from data: %s , to date: %s ' % (from_dt, until_dt) )  
        
        component_report_list = []
        date_filter = Q(incoming_date__lte = from_dt, incoming_date__gte = until_dt)
        
        try:
            args = ()
            kwargs = {}
            kwargs['product_id'] = 2
            
            
            # -- Get distinct months
            month_list = Case.objects.filter(date_filter,component_id__isnull = False, *args, **kwargs).\
                            annotate(month=TruncMonth('incoming_date')).values('month').distinct().order_by('month')
                        
            #log.info(month_list)
                
            #---get the unique months Month
            data = Case.objects.filter(date_filter,component_id__isnull = False, *args, **kwargs).\
                            annotate(month=TruncMonth('incoming_date')).values('month').\
                            annotate(case_count=Count('*')).values('month', 'component_id','case_count').order_by('month')
           
    
            #  Get the component details
            components = Component.objects.filter(product_id=2,active=True).order_by('name')
            #log.info(components)
            
            
            # -- Total 
            #data = Case.objects.filter(date_filter,component_id__isnull = False, *args, **kwargs).values('component_id').\
                            #annotate(case_count=Count('*')).order_by('component_id')
            
            #log.info(monthly)
            
            for component in components:
               
                report = {}
                report['component'] = component.name
                report['id'] = component.id
                total = 0;
                
                monthly_count_list = []
                if month_list is not None and len(month_list)>0:
                    monthly_dict = {}
                    for month in month_list:
                        case_count = 0
                        if data is not None and len (data) > 0:
                            for item in data:
                                monthly_dict = {}
                                if item['component_id'] == component.id and  month['month'] == item['month']:
                                    log.info('Month: %s component: %s , count: %s ' %  (item['month'], component.id, item['case_count']))
                                    monthly_dict['month'] =  month['month']   
                                    case_count = item['case_count']
                                    total = total + case_count
                                    monthly_dict['case_count'] = case_count
                                    monthly_count_list.append( monthly_dict)
                        if case_count == 0:
                            monthly_dict['month'] = month['month']
                            monthly_dict['case_count'] = case_count
                            monthly_count_list.append( monthly_dict)
                        
                    report['monthly_count'] =   monthly_count_list
                    report['total'] = total
                    if total >0:
                        report['average'] = math.ceil(total/len(month_list))
                    else:
                        report['average'] = 0
                        
                component_report_list.append(report)
              
                
            #log.info(component_report_list)
            self.context_dict['month_list'] = month_list
            self.context_dict['component_report_list'] = component_report_list
            
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
        #else:    
            #return backlog_list
        component_report = self.get_component_case(from_dt, until_dt,'month')
        self.context_dict['month_list'] = component_report['month_list']
        self.context_dict['component_report_list'] = component_report['component_report_list']
            
            
        return render(request, self.template_name,self.context_dict)
    
    
    
    def get_component_case(self, from_dt, until_dt,by_week_month):    
        
        component_report = {}
        component_report_list = []
        if by_week_month == 'week':
            until_dt =  from_dt+relativedelta(months=-1)
            
        date_filter = Q(incoming_date__lte = from_dt, incoming_date__gte = until_dt)
        
        try:
            args = ()
            kwargs = {}
            kwargs['product_id'] = 2
            
            month_list = []
            week_list = []
            # -- Get distinct months
            if by_week_month == 'month':
                month_list = Case.objects.filter(date_filter,component_id__isnull = False, *args, **kwargs).\
                            annotate(month=TruncMonth('incoming_date')).values('month').distinct().order_by('month')
                component_report['month_list'] = month_list
            if by_week_month == 'week':
                week_list = Case.objects.values('week').distinct().filter(date_filter, *args, **kwargs).order_by('week')
                component_report['week_list'] = week_list            
                
            #---get the unique months Month
            #log.info(month_list)
            data = []
            if by_week_month == 'month':
                data = Case.objects.filter(date_filter,component_id__isnull = False, *args, **kwargs).\
                            annotate(month=TruncMonth('incoming_date')).values('month').\
                            annotate(case_count=Count('*')).values('month', 'component_id','case_count').order_by('month')
            
            if by_week_month == 'week':
                data = Case.objects.filter(date_filter,component_id__isnull = False, *args, **kwargs).\
                            annotate(case_count=Count('*')).values('week', 'component_id','case_count').order_by('week')

                
            #  Get the component details
            components = Component.objects.filter(product_id=2,active=True).order_by('name')
            #log.info(components)
            
            
            # -- Total 
            #data = Case.objects.filter(date_filter,component_id__isnull = False, *args, **kwargs).values('component_id').\
                            #annotate(case_count=Count('*')).order_by('component_id')
            
            #log.info(monthly)
            
            for component in components:
               
                report = {}
                report['component'] = component.name
                report['id'] = component.id
                total = 0;
                
                case_count_list = []
                
                if by_week_month == 'month' and month_list is not None and len(month_list)>0:
                    monthly_dict = {}
                    for month in month_list:
                        case_count = 0
                        if data is not None and len (data) > 0:
                            for item in data:
                                monthly_dict = {}
                                if item['component_id'] == component.id and  month['month'] == item['month']:
                                    log.info('Month: %s component: %s , count: %s ' %  (item['month'], component.id, item['case_count']))
                                    monthly_dict['month'] =  month['month']   
                                    case_count = item['case_count']
                                    total = total + case_count
                                    monthly_dict['case_count'] = case_count
                                    case_count_list.append( monthly_dict)
                        if case_count == 0:
                            monthly_dict['month'] = month['month']
                            monthly_dict['case_count'] = case_count
                            case_count_list.append( monthly_dict)
                        
                    report['monthly_count'] =   case_count_list
                    report['total'] = total
                    if total >0:
                        report['average'] = math.ceil(total/len(month_list))
                    else:
                        report['average'] = 0
                        
                    component_report_list.append(report)
                
                if by_week_month == 'week' and week_list is not None and len(week_list)>0:
                    for week in week_list:
                        case_count = 0
                        if data is not None and len (data) > 0:
                            for item in data:
                                weekly_dict = {}
                                if item['component_id'] == component.id and  week['week'] == item['week']:
                                    #log.info('Month: %s component: %s , count: %s ' %  (item['week'], component.id, item['case_count']))
                                    weekly_dict['week'] =  month['week']   
                                    case_count = item['case_count']
                                    total = total + case_count
                                    weekly_dict['case_count'] = case_count
                                    case_count_list.append( weekly_dict)
                        if case_count == 0:
                            weekly_dict['week'] = week['week']
                            monthly_dict['case_count'] = case_count
                            case_count_list.append( weekly_dict)
                        
                    report['weekly_count'] =   case_count_list
                    report['total'] = total
                    if total >0:
                        report['average'] = math.ceil(total/len(week_list))
                    else:
                        report['average'] = 0
                        
                    component_report_list.append(report)
                    
                component_report['component_report_list'] = component_report_list
                
            return component_report
        
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
               