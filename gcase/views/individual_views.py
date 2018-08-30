# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from gcase.models import IndividualReport,GcaseUser, individual_report
from django.utils.functional import lazy
from gcase.forms import CaseAddEditForm
from django.db import DatabaseError
from django.db import connection
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
from gcase.views.period_set_views import PeriodSetView
from cgi import log
log = logging.getLogger(__name__)


class IndividualReportView(PeriodSetView):
    
    template_name='gcase/report/individual.html'
    context_dict = {}
    def get(self, request):
        self.context_dict = {}
        data=request.GET.copy()
        
        self.context_dict = self.set_duration(data, self.context_dict, -1)
        date_filter = self.set_date_filter(data,'week')
        self.context_dict['period'] = '( %04d/%02d ~ %04d/%02d )' % (data['from_year'],data['from_month'],data['to_year'],data['to_month'])
         
        backlog_list = None
        total_list = None
        
        total_report = []
        try:
            kwargs = {}
            args = ()
            
            user_list =  GcaseUser.objects.filter(user__is_active=1,case_handler=True).select_related('user').order_by('id')
            week_list = IndividualReport.objects.values('week').distinct().filter(date_filter, *args, **kwargs).order_by('-week')
            
            total_list = IndividualReport.objects.filter(date_filter, *args, **kwargs).values('week','gcase_user_id','pw_backlog','incoming','so','so_partner').order_by('-week')
            
            log.info(total_list)
#             total_list = IndividualReport.objects.filter(date_filter, *args, **kwargs).values('week','gcase_user_id').\
#                             annotate(total_pw_backlog=Sum('pw_backlog'),total_incoming=Sum('incoming'),
#                                      total_so=Sum('so'),total_so_partner=Sum('so_partner')
#                                      ).order_by('-week')
                        
            
            for item in week_list:
                log.info('Week is %s' % item['week'])
                total = {}
                total['week'] = item['week']
                
                user_wise = []
                for user in user_list:
                    user_report = self.set_total_info(user,item['week'],total_list)
                    user_wise.append(user_report)
                
                total['user_wise'] = user_wise          
                total_report.append(total)

            for data in total_report:
                log.info(data['week'])
                log.info('---------------------------------------------')
                log.info(data['user_wise'])       
                self.context_dict['week_list'] = week_list     
            self.context_dict['user_list'] = user_list
            self.context_dict['user_count'] = len(user_list)
            self.context_dict['total_report'] = total_report

            
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
        #else:    
            #return backlog_list
        
#         components = None
#         try:
#              components = Component.objects.filter(product_id=2, active=True).order_by('name')
#         except Exception, ex:
#             log.exception("SQL Error encountered :" + str(ex))
#             return None
#         
#         self.context_dict['component_list'] = components
#         
#         self.context_dict['users_component_list'] = self.set_fb_component(self.context_dict['from_year'],self.context_dict['from_month'], \
#                               self.context_dict['to_year'],self.context_dict['to_month'],user_list, components)
        
        return render(request, self.template_name,self.context_dict)
    
    def set_total_info(self, user, week, total_list):
        for total in total_list:
            report_info = {}
            found = False
            if week == total['week'] and total['gcase_user_id'] == user.id:
                
                report_info['week'] = week
                report_info['user'] = user
                report_info['report'] = total
                #report_info['backlog'] = total['pw_backlog']
#               report_info['backlog'] = ( total['total_pw_backlog'] + total['total_incoming'] ) - total['total_so']
                found = True
                break
            
            if not found:
                report_info['week'] = week
                report_info['user'] = user
                total ={}
                total['total_pw_backlog'] = 0;
                total['total_incoming'] = 0;
                total['total_so'] = 0;
                total['total_so_partner'] = 0;
                report_info['report'] = total
                #report_info['backlog'] = 0

        return report_info
    
    def previous_week_backlog(self,current_week, user_id):
        prev_week = current_week + relativedelta(days=-7)
        pw_backlog = 0
        try:
            data = IndividualReport.objects.get(week=prev_week, gcase_user_id=user_id).values('pw_backlog')
            if data:
                pw_backlog = data.pw_backlog
            log.info('Data is %s ' %  pw_backlog)
        
        except Exception, ex:
            log.exception("SQL Error encountered in client list.." + str(ex))
        
        return  pw_backlog
#     def set_fb_component(self,from_year,from_month,to_year, to_month,user_list, components):
#         
#         from_days = get_days_in_month(from_year, from_month)
#         from_dt = '%04d-%02d-%02d 23:59:59' % (from_year, from_month, from_days)
#         until_dt = '%04d-%02d-01 00:00:00' % (to_year, to_month)
#         
#         from_dt = datetime.strptime(from_dt, '%Y-%m-%d %H:%M:%S') #23:59:59
#         until_dt = datetime.strptime(until_dt, '%Y-%m-%d %H:%M:%S') # 00:00:00'
#         
#         user_wise_component_list = []
#         sql = '''   SELECT gcase_user_id,Count(gcase_user_id) FROM `cases` WHERE product_id=2 AND component_id=%s 
#                     AND incoming_date <= %s AND incoming_date >= %s AND component_id is NOT NULL  GROUP BY gcase_user_id ORDER BY gcase_user_id'''
#         
#         
#         
#         
#         try:
#             for item in components:
#                 tmp = {}
#                 tmp['components_id'] = item.id
#                 
#                 log.info("**************")
#                 log.info(tmp['components_id'])
#                 log.info("**************")
#                 
#                 components_count = []
#                 data = None;
#                 with connection.cursor() as cursor:
#                     cursor.execute(sql, [tmp['components_id'],from_dt,until_dt])
#                     data = cursor.fetchall()
#                 
#                 for item in user_list:
#                     exists = False
#                     for report in data:
#                         if report[0] == item.id:
#                             components_count.append(report[1])
#                             exists = True
#                             break
#                     
#                     if not exists:
#                         components_count.append(0)
#                 tmp['component_count'] = components_count
#                 
#                 user_wise_component_list.append(tmp)
# 
#             log.info(user_wise_component_list)
#             return user_wise_component_list
#         except Exception, ex:
#             log.exception("SQL Error encountered in client list.." + str(ex))
#             return None
         