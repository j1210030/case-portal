# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from django.db import connection
from gcase.models import PartnerReport, Product, Partner
from django.utils.functional import lazy
from gcase.forms import CaseAddEditForm
from gcase.views.period_set_views import PeriodSetView
from django.db import DatabaseError
from itertools import chain
from datetime import timedelta
from django.http import StreamingHttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Avg, Max, Min
from django.db.models.functions import TruncMonth,  TruncYear
#import unicodecsv as csv
import csv
from io import TextIOWrapper, StringIO
from io import BytesIO
import sys;
from django.template.defaultfilters import default
from django.db.models.query import prefetch_related_objects
log = logging.getLogger(__name__)


class PartnerReportMonthlyView(PeriodSetView):
    
    template_name='gcase/report/partner/monthly/index.html'
    context_dict = {}
    def get(self, request):
        data=request.GET.copy()
        self.context_dict = {}
        self.context_dict = self.set_duration(data, self.context_dict, -3)
       
        from_days = get_days_in_month( int(data['from_year']), int(data['from_month']))
        from_dt = '%04d-%02d-%02d 23:59:59' % (int(data['from_year']), int(data['from_month']), from_days)
        until_dt = '%04d-%02d-01 00:00:00' % (int(data['to_year']), int(data['to_month']))
        
        from_dt = datetime.strptime(from_dt, '%Y-%m-%d %H:%M:%S') #23:59:59
        until_dt = datetime.strptime(until_dt, '%Y-%m-%d %H:%M:%S') # 00:00:00'
        
        self.context_dict['view_name'] = 'report'
        self.context_dict['action'] = 'partner_monthly'
        self.context_dict['period'] = '%04d.%02d ~ %04d.%02d' % (self.context_dict['from_year'], self.context_dict['from_month'],
                                                                 self.context_dict['to_year'], self.context_dict['to_month'])
    
        try:
            monthly_case_list= []
            android_list= []
            firebase_list= []
            
            sql = '''SELECT YEAR(incoming_date) AS year ,MONTH(incoming_date) AS month , count(*) AS case_count FROM `cases` 
                    WHERE (`cases`.`incoming_date` <= %s AND `cases`.`incoming_date` >= %s 
                    AND `cases`.`partner_id` IS NOT NULL) '''
            
            
            group_order_sql = ''' GROUP BY YEAR(incoming_date) ,MONTH(incoming_date) ORDER BY 
                                    YEAR(incoming_date) DESC, MONTH(incoming_date) DESC '''
            
            product_sql = sql + ''' AND cases.product_id = %s ''' + group_order_sql
            
            sql = sql + group_order_sql
            
            with connection.cursor() as cursor_monthly:
                 cursor_monthly.execute(sql, [from_dt, until_dt] )
                 monthly_case_list = cursor_monthly.fetchall()
            
            with connection.cursor() as cursor_android:
                 cursor_android.execute(product_sql, [from_dt, until_dt, 1] )
                 android_list = cursor_android.fetchall()
                 
            with connection.cursor() as cursor_firebase:
                 cursor_firebase.execute(product_sql, [from_dt, until_dt, 2] )
                 firebase_list = cursor_firebase.fetchall()
            
            self.context_dict['monthly_case_list'] = monthly_case_list
            self.context_dict['android_list'] = android_list
            self.context_dict['firebase_list'] = firebase_list
            
             
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
       
        return render(request, self.template_name,self.context_dict)
        

class PartnerReportDetailView(PeriodSetView):
    
    template_name='gcase/report/partner/monthly/partner_report_modal.html'
    context_dict = {}
    def get(self, request):
        self.context_dict = {}
        data=request.GET.copy()
        date_filter = Q()
        self.context_dict['period'] = '%s/%s ~ %s/%s' % (data['from_year'], data['from_month'],data['to_year'], data['to_month'])
        try:
            kwargs = {}
            args = ()
            
            periods_jp =  Case.objects.filter(date_filter,product__id=data['product_id'],partner__geo_location='jp',*args, **kwargs).\
                        order_by('-year','-month').values('year','month').distinct()
            
            periods_ko =  PartnerReport.objects.filter(date_filter,product__id=data['product_id'],partner__geo_location='ko',*args, **kwargs).\
                        order_by('-year','-month').values('year','month').distinct()
            
            periods_zh =  PartnerReport.objects.filter(date_filter,product__id=data['product_id'],partner__geo_location='zh',*args, **kwargs).\
                        order_by('-year','-month').values('year','month').distinct()
            
           
            
            data = PartnerReport.objects.filter(date_filter,product__id=data['product_id'],*args, **kwargs).select_related('partner')\
                            .order_by('-year','-month')
        
            
            self.context_dict['total_list_jp'] = self.get_partners_4_locale('jp', periods_jp, data)
            self.context_dict['total_list_ko'] = self.get_partners_4_locale('ko', periods_ko, data)
            self.context_dict['total_list_zh'] = self.get_partners_4_locale('zh', periods_zh, data)
            
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
        #else:    
            #return backlog_list
        
        return render(request, self.template_name,self.context_dict)
    
    def get_partners_4_locale(self, locale, period_list, data):
         total_list = []
         for period in period_list:
                report = {}
                report['period'] = '%s/%s' % (period['year'], period['month'])
                locale_list = [] 
                for item in data:
                    if period['year'] == item.year and period['month'] == item.month and item.partner.geo_location==locale:
                         locale_list.append(item) 
                
                report['locale_list'] =   locale_list
                report['size'] = len(locale_list)
                
                total_list.append(report)
         return total_list
        
        
        
        
class PartnerReportTotalView(PeriodSetView):
    
    template_name='gcase/report/partner/total/index.html'
    context_dict = {}
    def get(self, request):
        data=request.GET.copy()
        self.context_dict = {}
        
        self.context_dict = self.set_duration(data, self.context_dict, -3)
        
        from_days = get_days_in_month( int(data['from_year']), int(data['from_month']))
        from_dt = '%04d-%02d-%02d 23:59:59' % (int(data['from_year']), int(data['from_month']), from_days)
        until_dt = '%04d-%02d-01 00:00:00' % (int(data['to_year']), int(data['to_month']))
        
        
        from_dt = datetime.strptime(from_dt, '%Y-%m-%d %H:%M:%S') #23:59:59
        until_dt = datetime.strptime(until_dt, '%Y-%m-%d %H:%M:%S') # 00:00:00'
            
        
        self.context_dict['view_name'] = 'report'
        self.context_dict['action'] = 'partner_by_partner'
        
        
        self.context_dict['period'] = '%04d.%02d ~ %04d.%02d' % (self.context_dict['from_year'], self.context_dict['from_month'],
                                                                 self.context_dict['to_year'], self.context_dict['to_month'])
        try:
           
            sql = ''' SELECT cases.partner_id AS partner_id, COUNT(`cases`.`partner_id`) AS case_count, 
                                            partners.name_locale AS name_locale,partners.name_english AS name_english ,
                                            partners.geo_location AS geo_location FROM cases 
                                            INNER join partners ON cases.partner_id = partners.id 
                                            WHERE cases.incoming_date <= %s AND cases.incoming_date >= %s 
                                            AND `cases`.`partner_id` IS NOT NULL  
                                            '''
            if 'product' in data and data['product'] != '':
                sql = sql + ' AND cases.product_id  = %s '
                self.context_dict['product'] = data['product']
                
            sql = sql + ' GROUP BY cases.partner_id ORDER BY case_count DESC'
            
            with connection.cursor() as cursor:
                if 'product' in data and data['product'] != '':
                    cursor.execute(sql, [from_dt, until_dt, data['product']] )
                else:    
                    cursor.execute(sql, [from_dt, until_dt] )
                
                partner_case_list = cursor.fetchall()
               
                self.context_dict['partner_case_list'] = partner_case_list
                self.context_dict['min_count'] = -1
            if 'csv' in data and  len(data['csv']):
                filename = 'partner_case_%s%02d_%s%02d.csv'   % (data['from_year'],int(data['from_month']),data['to_year'],int(data['to_month']))
                log.info('File name: %s ' % (filename))
                return self.csv_download(partner_case_list,filename) 
            
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
            
        return render(request, self.template_name,self.context_dict)
            
    
    def csv_download(self,partner_case_list,filename):
        column_names = ['Geo Location','Partner name (Eng)', 'Partner name (Locale)','Case Count']
        
        column_names = [unicode(i) for i in column_names]
        
    
        memory_file = BytesIO() 
      
        writer = csv.writer(memory_file)
        
        writer.writerow(column_names)
        count =0;
        for report in partner_case_list:
            row = []
            row.append(unicode(report[4]).encode('utf-8'))
            row.append(unicode(report[3]).encode('utf-8'))
            row.append(unicode(report[2]).encode('utf-8'))
            row.append(report[1])
            
 
            writer.writerow(row)
            count +=1
            
        response = HttpResponse( memory_file.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
        
        return response
        
        
        
        