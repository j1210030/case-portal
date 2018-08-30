# -*- coding: utf-8 -*-
"""
@File: da_report_views.py 
"""
from .common_views import *
from gcase.models import BacklogReport, PartnerReport,LanguageReport, Partner,ReviewRequestReport
from gcase.views import BacklogReportView, LanguageReportView
from django.utils.functional import lazy
from django.db import DatabaseError
from itertools import chain
from datetime import timedelta
from django.http import StreamingHttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Avg, Max, Min
from django.db import connection
import csv
from io import TextIOWrapper, StringIO
from io import BytesIO
import sys;
from django.template.defaultfilters import default
from django.db.models.query import prefetch_related_objects
log = logging.getLogger(__name__)


class DaReportView(BacklogReportView,LanguageReportView):
    
    template_name='gcase/report/da_report/index.html'
    context_dict = {}
    
    def get(self, request):
        
        self.context_dict = {}
        data=request.GET.copy()
        
        self.context_dict['view_name'] = 'da_bi_weekly'
        self.context_dict['action'] = 'index'
        
        week_list = []
        table_data_list = []
        dt = None
        sunday = None
        
        if 'from' not in data or data['from'] == '':
            sunday = get_sunday2(None, None);
            #og.info(' Default Sunday: %s '  % sunday)
            dt = datetime.strptime(sunday,'%Y-%m-%d') 
            from_dt = dt + relativedelta(days=-7) 
           
        else:
             dt = format_dt2(data['from'],False)
             sunday = get_sunday2(dt, None);
             from_dt = datetime.strptime(sunday,'%Y-%m-%d') 
        
        
        log.info('From: %s '  % from_dt)
        
        
        week_list.append(from_dt.date())
        dt = from_dt + relativedelta(days=-7)
        
        self.context_dict['period'] = '( %02s/%02s ~ %02s/%02s )' % ( dt.month , (dt + relativedelta(days=-6)).day, from_dt.month, from_dt.day )
        log.info( ' period: %s ' % self.context_dict['period'] )
        week_list.append(dt.date())
        
        log.info(week_list)
        
        until_dt = from_dt + relativedelta(days=-28)
        log.info('Until: %s ' % until_dt)
        
        date_filter = Q(week__lte = from_dt, week__gte = until_dt)
        
        data = self.get_backlog_list(date_filter,'asc')
        
        total_assigned=0
        total_needinfo =0
        total_blocked =0
        total_review_requested =0
        total_backlog = 0
        total_incoming = 0
        total_incoming_partner = 0
        total_so = 0
        total_so_partner = 0 
        
        for week in week_list:
            for item in data:
                if week == item.week:
                    
                    total_assigned = total_assigned + item.assigned
                    total_needinfo = total_needinfo + item.needinfo
                    total_blocked = total_blocked + item.blocked
                    total_review_requested = total_review_requested + item.review_requested
                    total_backlog = total_backlog + item.get_backlog()
                    total_incoming =  total_incoming + item.incoming
                    total_incoming_partner =  total_incoming_partner + item.incoming_partner
                    total_so =  total_so + item.so
                    total_so_partner =  total_so_partner + item.so_partner
                     
                    table_data_list.append(item)
                    
                 
        bi_weekly_total = {}
        bi_weekly_total['assigned'] = total_assigned
        bi_weekly_total['needinfo'] = total_needinfo
        bi_weekly_total['blocked'] = total_blocked
        bi_weekly_total['review_requested'] = total_review_requested
        bi_weekly_total['total_backlog'] = total_backlog
        bi_weekly_total['total_incoming'] = total_incoming
        bi_weekly_total['total_incoming_partner'] = total_incoming_partner
        bi_weekly_total['total_so'] = total_so
        bi_weekly_total['total_so_partner'] = total_so_partner
         
        
        
        log.info(len(table_data_list))
            
        self.context_dict['bi_weekly_data_list'] = table_data_list
        self.context_dict['graph_list'] = data
        self.context_dict['biweekly_total'] =  bi_weekly_total
        self.context_dict['week_list'] = week_list
        self.context_dict['total_list'] = self.get_total_backlog(date_filter, 'asc')
        self.context_dict['backlog_list'] = data
        
        log.info(len(self.context_dict['backlog_list']))
        
        self.get_language_report(from_dt, until_dt)
        
        self.context_dict['component_report'] = self.get_firebase_component_report(from_dt, until_dt)
        self.context_dict['component_report_partner'] = self.get_firebase_component_partners_report(from_dt, until_dt)
        self.context_dict['review_list'] = self.get_review_request_report(from_dt, until_dt)
        
        log.info(self.context_dict['language_report_android'])
    
        return render(request, self.template_name,self.context_dict)
    
    
    
    def get_language_report(self, from_dt, until_dt):
         
         
         date_filter = Q(week__lte = from_dt, week__gte = until_dt)
        
         language_report_android = []
         language_report_firebase = []
         
         self.context_dict['language_total_report'] = self.get_language_total(date_filter, 'asc')    
         data = self.get_language_report_by_product(date_filter, 'asc')   
         
         for item in data:
            
                if item.product_id == 1:
                    language_report_android.append(item)    
                if item.product_id == 2:    
                    language_report_firebase.append(item)

         self.context_dict['language_report_android'] = language_report_android    
         self.context_dict['language_report_firebase'] = language_report_firebase  
        
         log.info(language_report_android )
        
    def get_firebase_component_report(self, from_dt, until_dt):
        component_report = [] 
        
         # Adjust until_dt one month to 2weeks
        until_dt = from_dt + relativedelta(days=-7)
        
        try:
             sql = ''' SELECT count(*) AS case_count ,components.name  FROM cases INNER JOIN components ON cases.component_id = components.id
                        WHERE week <= %s AND week >= %s AND cases.component_id IS NOT NULL AND cases.product_id = 2 GROUP BY components.id   
                        ORDER BY case_count DESC'''
            
            
             with connection.cursor() as cursor:
                 cursor.execute(sql, [from_dt, until_dt] )
                 component_report = cursor.fetchall()
            
             log.info(component_report)
            
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
         
        return component_report

    def get_firebase_component_partners_report(self, from_dt, until_dt):
        component_partners_report = [] 
        
         # Adjust until_dt one month to 2weeks
        until_dt = from_dt + relativedelta(days=-7)
        
        try:
             sql = ''' SELECT count(*) AS case_count ,components.name  FROM cases INNER JOIN components ON cases.component_id = components.id
                        WHERE week <= %s AND week >= %s AND cases.component_id IS NOT NULL AND cases.product_id = 2 AND cases.partner_id IS NOT NULL 
                        GROUP BY components.id   
                        ORDER BY case_count DESC'''
            
             with connection.cursor() as cursor:
                 cursor.execute(sql, [from_dt, until_dt] )
                 component_partners_report = cursor.fetchall()
            
             log.info(component_report)
            
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
         
        return component_partners_report

    def get_review_request_report(self, from_dt, until_dt):
        date_filter = Q(week__lte = from_dt, week__gte = until_dt)
        review_list = []
        try:
            kwargs = {}
            args = ()
            review_list = ReviewRequestReport.objects.filter(date_filter, *args, **kwargs).order_by('-week')
            
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
        
        return review_list