# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from gcase.models import BacklogReport
from django.utils.functional import lazy
from gcase.forms import CaseAddEditForm
from gcase.views.dashboard_views import DashboardView
from django.db import DatabaseError
from itertools import chain
from datetime import timedelta
from django.db import connection
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


class YearlyReportView(View):
    
    template_name='gcase/yearly_report/index.html'
    context_dict = {}
    def get(self, request):
        self.context_dict = {}
        data=request.GET.copy()
        if 'year' not in data or len(data['year'])!=4:
            now = datetime.now()
            data['year'] = now.year
        data['year'] = 2017
        
        incoming_nonpartner  = self.get_incoming_by_product(data['year'], False)
        incoming_partner  = self.get_incoming_by_product(data['year'], True)
        
        so_nonpartner  = self.so_by_product(data['year'], False)
        so_partner  = self.so_by_product(data['year'], True)
        
        android_monthly = self.monthly_incoming_by_product(data['year'], 1)
        firebase_monthly = self.monthly_incoming_by_product(data['year'], 2)
        
        android_monthly_so = self.monthly_so_by_product(data['year'], 1)
        firebase_monthly_so = self.monthly_so_by_product(data['year'], 2)
        
        
        #-------------------Language -------------------------
        android_language_nonpartner = self.incoming_by_language(data['year'], 1, False)
        android_language_partner = self.incoming_by_language(data['year'], 1, True)
        firebase_language_nonpartner = self.incoming_by_language(data['year'], 2, False)
        firebase_language_partner = self.incoming_by_language(data['year'], 2, True)
        
        lang_dict = dict(settings.LANGUAGE_CHOICES)
        
        monthly_incoming_android = []
        monthly_incoming_firebase = []
         
        for key, value in lang_dict.iteritems():
            tmp_android = {}
            tmp_firebase = {}
            
            tmp_android['language'] = key
            tmp_android['incoming_list'] = self.monthly_incoming_by_language(data['year'],1,key)
            tmp_firebase['language'] = key
            tmp_firebase['incoming_list'] = self.monthly_incoming_by_language(data['year'],2,key)
            monthly_incoming_android.append(tmp_android)
            monthly_incoming_firebase.append(tmp_firebase)
            
        #log.info('------------------------------------------')
        #for item in monthly_incoming_android:
         #   log.info(item)
        
        #log.info('------------------------------------------')
        
        self.context_dict['monthly_incoming_android'] = monthly_incoming_android
        self.context_dict['monthly_incoming_firebase'] = monthly_incoming_firebase
        
        android_language_list = [];
        firebase_language_list = [];
        
        #----- Component --------------#
        self.context_dict['component_report'] = self.get_component_report(data['year'])
        self.context_dict['component_report_partner'] = self.get_component_report_partner(data['year'])

        #-----------Quality ------------#
        
        android_quality = {}
        firebase_quality = {}
        
        avg_data = self.get_average_ok(1, data['year'])
        
        android_quality['weekly_ok'] = avg_data[0]
        android_quality['monthly_ok'] = avg_data[1]
        android_quality['total_requested'] = self.get_toal_requested(1, data['year'])[0]
        android_quality['monthly_list'] = self.monthly_quality_by_product(1,data['year'])
         
        avg_data = self.get_average_ok(2, data['year'])
        
        firebase_quality['weekly_ok'] = avg_data[0]
        firebase_quality['monthly_ok'] = avg_data[1]
        firebase_quality['total_requested'] = self.get_toal_requested(2, data['year'])[0]
        firebase_quality['monthly_list'] = self.monthly_quality_by_product(2,data['year'])
        
        self.context_dict['android_quality'] = android_quality
        self.context_dict['firebase_quality'] =firebase_quality
        
        #-------------Top partner--------------                                     
        
        self.context_dict['android_top_partners'] = self.get_top_partner_case_count(data['year'],1)
        self.context_dict['firebase_top_partners'] = self.get_top_partner_case_count(data['year'],2)
        self.context_dict['min_count'] = 3
        
        for key, value in lang_dict.iteritems():
            android_lang = {}
            firebase_lang = {}
            
            
            android_lang['incoming_nonpartner'] = 0
            android_lang['incoming_partner'] = 0
            android_lang['percent'] = 0
            firebase_lang['incoming_nonpartner'] = 0
            firebase_lang['incoming_partner'] = 0
            firebase_lang['percent'] = 0
            
            for item in android_language_nonpartner:
                if item[0] == key:
                    log.info('Lang: %s ' % item[0] )
                    android_lang['language'] = key
                    android_lang['incoming_nonpartner'] = item[1]
                    
            for item in android_language_partner:
                if item[0] == key:
                    android_lang['incoming_partner'] = item[1]
                     
            total =   android_lang['incoming_nonpartner'] +  android_lang['incoming_partner']
            android_lang['total'] = total
            if android_lang['incoming_partner'] >= 0:
                percent = ( android_lang['incoming_partner']  / float(total)) * 100
                log.info(' Percent:  %s ' % percent)
                android_lang['percent'] =  '{0:.1f}'.format(percent)
            android_language_list.append(android_lang)
            
            total = 0
            percent = 0
            
            for item in firebase_language_nonpartner:
                if item[0] == key:
                    firebase_lang['language'] = key
                    firebase_lang['incoming_nonpartner'] = item[1]
                    
            for item in firebase_language_partner:
                if item[0] == key:
                    firebase_lang['incoming_partner'] = item[1]
                     
            total =   firebase_lang['incoming_nonpartner'] +  firebase_lang['incoming_partner']
            firebase_lang['total'] = total
            if firebase_lang['incoming_partner'] >= 0:
                percent = ( firebase_lang['incoming_partner']  / float(total)) * 100
                log.info(' Percent:  %s ' % percent)
                firebase_lang['percent'] =  '{0:.1f}'.format(percent)
            

            firebase_language_list.append(firebase_lang)
            
        log.info(firebase_language_list)
        
        self.context_dict['firebase_language_list'] = firebase_language_list
        self.context_dict['android_language_list'] = android_language_list
        
        #log.info(so_nonpartner)
        #log.info(so_partner)
        
        total_incoming = {}
        
        firebase_incoming_total = 0;
        android_incoming_total = 0;
        
        firebase_so_total = 0;
        android_so_total = 0;
        
        self.context_dict['view_name'] = 'yearly_report'
        self.context_dict['year'] = data['year']
        
        for item in incoming_nonpartner:
            if item[0] == 1:
                 android_incoming_total += item[1]
            if item[0] == 2:
                 firebase_incoming_total += item[1]
        
        for item in incoming_partner:
            if item[0] == 1:
                 android_incoming_total += item[1]
            if item[0] == 2:
                 firebase_incoming_total += item[1]
            
        for item in so_nonpartner:
            if item[0] == 1:
                 android_so_total += item[1]
            if item[0] == 2:
                 firebase_so_total += item[1]
        
        for item in so_partner:
            if item[0] == 1:
                 android_so_total += item[1]
            if item[0] == 2:
                 firebase_so_total += item[1]
            
        
        total_incoming['firebase_so'] = firebase_so_total
        total_incoming['android_so'] = android_so_total
        
        total_incoming['firebase'] = firebase_incoming_total
        total_incoming['android'] = android_incoming_total
       
        
        self.context_dict['total_incoming'] = total_incoming
        self.context_dict['incoming_nonpartner'] = incoming_nonpartner
        self.context_dict['incoming_partner'] = incoming_partner
        self.context_dict['so_nonpartner'] = so_nonpartner
        self.context_dict['so_partner'] = so_partner
        
        self.context_dict['android_monthly'] = android_monthly
        self.context_dict['firebase_monthly'] = firebase_monthly
        
        self.context_dict['android_monthly_so'] = android_monthly_so
        self.context_dict['firebase_monthly_so'] = firebase_monthly_so
        
        return render(request, self.template_name,self.context_dict) 
    
    
    def get_incoming_by_product(self,year, partner_only):
        incoming = None;
        sql = ''' SELECT product_id,count(id) FROM cases WHERE status!= %s AND YEAR(incoming_date) = %s '''
        if partner_only:
            sql = sql + ''' AND cases.partner_id is not null ''' 
        else:
            sql = sql + ''' AND cases.partner_id is null ''' 
        
        sql = sql + ''' GROUP BY product_id'''
         
        with connection.cursor() as cursor:
             cursor.execute(sql, ['duplicate', year])
             incoming = cursor.fetchall()
    
        return incoming
    
    def language_incoming(self,year, partner_only):
         incoming = None
         sql = ''' SELECT language,count(id) FROM cases WHERE status!= %s AND YEAR(incoming_date) = %s '''
         if partner_only:
            sql = sql + ''' AND cases.partner_id is not null ''' 
         else:
            sql = sql + ''' AND cases.partner_id is  null ''' 
        
         sql = sql + ''' GROUP BY language'''
         
         with connection.cursor() as cursor:
             cursor.execute(sql, ['duplicate', year])
             incoming = cursor.fetchall()
         return incoming
    
    def so_by_product(self,year, partner_only):
        so_list = None
        sql = ''' SELECT product_id,count(id) FROM cases WHERE status= %s AND YEAR(so_date) = %s '''
        if partner_only:
            sql = sql + ''' AND cases.partner_id is not null ''' 
        
        sql = sql + ''' GROUP BY product_id'''
         
        with connection.cursor() as cursor:
             cursor.execute(sql, ['solution_offered', year])
             so_list = cursor.fetchall()
        
        return so_list
    
    def so_by_language(self,year, partner_only):
        so_list = None
        sql = ''' SELECT language,count(id) FROM cases WHERE status= %s AND YEAR(so_date) = %s '''
        if partner_only:
            sql = sql + ''' AND cases.partner_id is not null ''' 
        
        sql = sql + ''' GROUP BY language'''
         
        with connection.cursor() as cursor:
             cursor.execute(sql, ['solution_offered', year])
             so_list = cursor.fetchall()
    
    def monthly_incoming_by_product(self,year, product_id):
        monthly_list = None
        sql = ''' SELECT MONTH(incoming_date),count(id) FROM cases WHERE cases.product_id=%s and status!=%s AND YEAR(incoming_date) = %s GROUP BY MONTH(incoming_date) ORDER BY MONTH(incoming_date)'''
        with connection.cursor() as cursor:
             #cursor.execute(sql, [product_id,'duplicate', year])
             cursor.execute(sql,[product_id,'duplicate',year])
             monthly_list = cursor.fetchall()
        
        return monthly_list
 
    def monthly_so_by_product(self,year, product_id):
        so_list = None
        sql = '''SELECT MONTH(so_date),count(id) FROM cases WHERE cases.product_id=%s and status=%s AND YEAR(so_date) = %s GROUP BY MONTH(so_date) ORDER BY MONTH(so_date)'''
        with connection.cursor() as cursor:
             #cursor.execute(sql, [product_id,'duplicate', year])
             cursor.execute(sql,[product_id,'solution_offered',year])
             so_list = cursor.fetchall()
        
        return so_list
    
    def incoming_by_language(self,year,product_id, partner_only):
         incoming = None;
         sql = ''' SELECT language,count(id) FROM cases WHERE status!= %s AND product_id=%s AND YEAR(incoming_date) = %s '''
         if partner_only:
            sql = sql + ''' AND cases.partner_id is not null ''' 
         else:
            sql = sql + ''' AND cases.partner_id is null ''' 
        
         sql = sql + ''' GROUP BY language'''
         
         with connection.cursor() as cursor:
             cursor.execute(sql, ['duplicate', product_id,year])
             incoming = cursor.fetchall()
    
         return incoming
        
    def monthly_incoming_by_language(self,year,product_id,language):
         language_list = None
         sql = ''' SELECT MONTH(incoming_date),count(id) FROM `cases` WHERE YEAR(incoming_date) = %s AND status!= %s AND language=%s AND product_id=%s GROUP BY MONTH(incoming_date) ORDER BY MONTH(incoming_date) ASC''' 
         
         with connection.cursor() as cursor:
             cursor.execute(sql, [year,'duplicate',language,product_id])
             language_list = cursor.fetchall()
        
         return language_list
    
    def get_component_report(self, year):
        component_report = [] 
        try:
             sql = ''' SELECT count(*) AS case_count ,components.name  FROM cases INNER JOIN components ON cases.component_id = components.id
                        WHERE YEAR(incoming_date) = %s AND cases.component_id IS NOT NULL AND cases.product_id = 2 GROUP BY components.id   
                        ORDER BY case_count DESC'''
            
            
             with connection.cursor() as cursor:
                 cursor.execute(sql, [year] )
                 component_report = cursor.fetchall()
            
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
         
        return component_report
    
    def get_component_report_partner(self, year):
        component_report = [] 
        try:
             sql = ''' SELECT count(*) AS case_count ,components.name  FROM cases INNER JOIN components ON cases.component_id = components.id
                        WHERE YEAR(incoming_date) = %s AND cases.component_id IS NOT NULL AND cases.product_id = 2 AND cases.partner_id IS NOT NULL GROUP BY components.id   
                        ORDER BY case_count DESC'''
            
             with connection.cursor() as cursor:
                 cursor.execute(sql, [year] )
                 component_report = cursor.fetchall()
            
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
         
        return component_report
    
    def get_average_ok(self, product_id, year):
        avg_report = None
        sql = ''' SELECT AVG(ok_ratio) , AVG(monthly_ratio) FROM review_request_report WHERE YEAR(week)=%s AND product_id=%s '''
        try:
             with connection.cursor() as cursor:
                 cursor.execute(sql, [year, product_id] )
                 avg_report = cursor.fetchone()
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
        return avg_report
    
    def get_toal_requested(self, product_id, year):
        total_requested = 0;
        sql = ''' SELECT SUM( total_requested) FROM review_request_report WHERE product_id=%s and YEAR(week) = %s '''
        try:
             with connection.cursor() as cursor:
                 cursor.execute(sql, [product_id,year] )
                 total_requested = cursor.fetchone()
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
            
        return total_requested
    
    
    def monthly_quality_by_product(self, product_id, year):
        monthly_quality = None
        sql = ''' SELECT month(week), AVG(ok_ratio), AVG(monthly_ratio) FROM `review_request_report` WHERE product_id=%s AND YEAR(week)=%s
                GROUP  BY MONTH(week) ORDER BY MONTH(week) ASC'''
        
        try:
             with connection.cursor() as cursor:
                 cursor.execute(sql, [product_id,year] )
                 monthly_quality = cursor.fetchall()
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
            
        return monthly_quality
    
    def get_top_partner_case_count(self, year, product_id):
         partner_case_list = None
         try:
           
            sql = ''' SELECT cases.partner_id AS partner_id, COUNT(`cases`.`id`) AS case_count, 
                                            partners.name_locale AS name_locale,partners.name_english AS name_english ,
                                            partners.geo_location AS geo_location FROM cases 
                                            INNER join partners ON cases.partner_id = partners.id 
                                            WHERE product_id = %s AND YEAR(cases.incoming_date) = %s
                                            AND `cases`.`partner_id` IS NOT NULL  
                                            '''
           
            sql = sql + ''' GROUP BY cases.partner_id ORDER BY case_count DESC'''
            
            with connection.cursor() as cursor:
                cursor.execute(sql, [product_id,year] )
                partner_case_list = cursor.fetchall()
               
                self.context_dict['partner_case_list'] = partner_case_list
            
         except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
        
         return partner_case_list