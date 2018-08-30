# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from gcase.models import Case, LanguageReport

#from gcase.common_views import *
from django.conf import settings
#from views.common_views import *
from gcase.views.common_views import *   #common_views import *
#from Carbon.Events import app2Mask
import math
from datetime import timedelta
log = logging.getLogger(__name__)

class Command(BaseCommand):
    
 
    def handle(self, *args, **options):
    
        incoming = None
        incoming_partner = None
        so = None
        so_partner = None
        android_status = None
        firebase_status = None
        
        try:
            kwargs = {}
            args = ()
            review_request = {}
           
            sunday = get_sunday2(None, None);
            
            log.info('Sunday: %s ' % sunday)
            dt = datetime.strptime(sunday,'%Y-%m-%d') 
            dt = dt + relativedelta(days=-7)
           
            status_filter = ~Q(status__in=['duplicate'])
            
            # --- Total incoming by product #
            
            incoming_android = Case.objects.filter(status_filter,week=dt,product_id=1).values('language').annotate(case_count=Count('*')).order_by('language')
            incoming_firebase = Case.objects.filter(status_filter,week=dt,product_id=2).values('language').annotate(case_count=Count('*')).order_by('language')
            
            # -- Incoming partner -----#
            incoming_partner_android = Case.objects.filter(status_filter,week=dt,product_id=1,partner_id__isnull=False).values('language').annotate(case_count=Count('*')).order_by('language')
            incoming_partner_firebase = Case.objects.filter(status_filter,week=dt,product_id=2,partner_id__isnull=False).values('language').annotate(case_count=Count('*')).order_by('language')
            # --- Total So  ---- # 
            so_list_android = Case.objects.filter(so_week=dt, status='solution_offered',product_id=1).\
                            values('language').annotate(case_count=Count('*')).order_by('language')
            
            so_list_firebase = Case.objects.filter(so_week=dt, status='solution_offered',product_id=2).\
                            values('language').annotate(case_count=Count('*')).order_by('language')
            
            
           
           # forwarded_list_android = Case.objects.filter(week=dt, status='forwarded',product_id=1).\
                           # values('language').annotate(case_count=Count('*')).order_by('language')
            
            #firebase_list_android = Case.objects.filter(week=dt, status='forwarded',product_id=2).\
                            #values('language').annotate(case_count=Count('*')).order_by('language')
            
            
            #log.info(so_list_android)
            #log.info('-------------------------------------------------------')
            #log.info(forwarded_list_android)
            #log.info('-------------------------------------------------------')
            #log.info(android_list_android)
            
            
            #self.set_so_data(dt, 1, so_list_android)
            #self.set_so_data(dt, 2, so_list_firebase)
            
            # --- So Partner ------ #
            #so_partner = Case.objects.filter(so_week=dt,partner_id__isnull=False).values('product_id').annotate(case_count=Count('*')).order_by('product_id')
            #log.info(incoming_android)
            #log.info(incoming_partner_android)
            self.create_data(dt, 1, incoming_android,incoming_partner_android,so_list_android)
            self.create_data(dt, 2, incoming_firebase,incoming_partner_firebase, so_list_firebase)
            
        except Exception, ex:
             log.exception("SQL Error Encountered in jd search. " + str(ex))
             
    def create_data(self,week, product_id, incoming_list,incoming_partner_list, so_list):
        
         language_report = {}
         language_choices = dict(settings.LANGUAGE_CHOICES)
         
         for key, value in language_choices.iteritems():
            language_report['week'] = week
            language_report['product_id'] = product_id
            incoming_count = 0;
            incoming_partner_count = 0
            so_count = 0
           
            language_report['language'] = key
            if len(incoming_list) > 0:
                for item in incoming_list:
                    if key == item['language']:
                        incoming_count = item['case_count']
                        break
                      
            if len(incoming_partner_list) > 0:
                for item in incoming_partner_list:
                    if key == item['language']:
                        incoming_partner_count = item['case_count']
                        break
            
            if len(so_list) > 0:
                for item in so_list:
                     if key == item['language']:
                        so_count = item['case_count']
                        break
            
            language_report['incoming'] = incoming_count
            language_report['incoming_partner'] = incoming_partner_count  
            language_report['so'] = so_count
            language_report['pw_backlog'] = 0
            
            log.info(language_report)
            
            try:
                LanguageReport.objects.create(**language_report)
            except Exception, ex:
                log.exception("SQL Error encountered in client list.." + str(ex))
   

    def set_so_data(self,week, product_id, so_list):
          language_choices = dict(settings.LANGUAGE_CHOICES)
          for key, value in language_choices.iteritems():
            try:
                if len(so_list) > 0:
                    for item in so_list:
                        if key == item['language']:
                            data =  LanguageReport.objects.get(week=week,language=key, product_id=product_id)
                            data.so  = item['case_count']
                            data.save(update_fields=['so'])
            except Exception, ex:
                log.exception("SQL Error encountered in client list.." + str(ex))
    
    #def set_forwarded_data(self,week, product_id, forwarded_list):
     #     language_choices = dict(settings.LANGUAGE_CHOICES)
      #    for key, value in language_choices.iteritems():
       #     try:
        #        if len(so_list) > 0:
         #           for item in forwarded_list:
          #              if key == item['language']:
           #                 data =  LanguageReport.objects.get(week=week,language=key, product_id=product_id)
            #                data.forwarded  = item['case_count']
             #               data.save(update_fields=['so'])
            #except Exception, ex:
             #   log.exception("SQL Error encountered in client list.." + str(ex))