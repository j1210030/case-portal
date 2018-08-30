# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from gcase.models import Case, BacklogReport

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
            #dt = format_dt2(date_str,False)
            log.info(dt)
            
            #return 
            # --- Total incoming by product #
            
            incoming = Case.objects.filter(week=dt).values('product_id').annotate(case_count=Count('*')).order_by('product_id')
            log.info(incoming)
            
            
            # -- Incoming partner -----#
            incoming_partner = Case.objects.filter(week=dt,partner_id__isnull=False).values('product_id').annotate(case_count=Count('*')).order_by('product_id')
            
            # --- Total So  ---- # 
            so = Case.objects.filter(so_week=dt).values('product_id').annotate(case_count=Count('*')).order_by('product_id')
            
            # --- So Partner ------ #
            so_partner = Case.objects.filter(so_week=dt,partner_id__isnull=False).values('product_id').annotate(case_count=Count('*')).order_by('product_id')
            
        except Exception, ex:
             log.exception("SQL Error Encountered in jd search. " + str(ex))
             # --- Status wise count  #
        try:
            status_filter = ~Q(status__in=['solution_offered','duplicate','routed'])
            android_status = Case.objects.filter(status_filter,product_id=1).values('status').annotate(case_count=Count('status')).order_by('status')
            firebase_status = Case.objects.filter(status_filter,product_id=2).values('status').annotate(case_count=Count('status')).order_by('status')
             
            log.info('--incoming partner--')
            log.info(incoming_partner)
            
            log.info('--So--')
            log.info(so)
            log.info('--Status--')
            #log.info(android_status)
            #log.info(firebase_status)
            
            #log.info(android_incoming)
            #log.info(firebase_incoming)
            data = self.create_data(dt, 1, incoming, incoming_partner,so,so_partner,android_status)
            self.save_backlog(data)
            data = None
            log.info('-------------------------------------------------------')
            data = self.create_data(dt, 2, incoming, incoming_partner,so,so_partner,firebase_status)
            self.save_backlog(data)
            
        except Exception, ex:
             log.exception("SQL Error Encountered in jd search. " + str(ex))

            
    def create_data(self,week, product_id, incoming, incoming_partner,so,so_partner,product_status):
        
         backlog_report = {}
         backlog_report['week'] = week
         status_dict = dict(settings.CASE_STATUS_CHOICES)
         
         backlog_report['product_id'] = product_id
         backlog_report['incoming'] = 0
         backlog_report['incoming_partner'] = 0
         backlog_report['so'] = 0
         backlog_report['so_partner'] = 0
         
         backlog_report['forwarded'] = 0
         backlog_report['inconsult'] = 0
         backlog_report['assigned'] = 0
         backlog_report['blocked'] = 0 
         backlog_report['needinfo'] = 0
         backlog_report['review_requested'] = 0
         backlog_report['pw_backlog'] = 0
         
          
         if len(incoming) > 0:
             for item in incoming:
                 if item['product_id'] == product_id:
                     backlog_report['incoming'] = item['case_count']
                     break
             
         if len(incoming_partner) > 0:
             for item in incoming_partner:
                 if item['product_id'] == product_id:
                     backlog_report['incoming_partner'] = item['case_count']
                     break
                 
         if len(so) > 0:
             for item in so:
                 if item['product_id'] == product_id:
                     backlog_report['so'] = item['case_count']
                     break
             
         if len(so_partner) > 0:
             for item in so_partner:
                 if item['product_id'] == product_id:
                     backlog_report['so_partner'] = item['case_count']
                     break
        
         if backlog_report['incoming_partner'] > 0:
            total = backlog_report['incoming_partner'] + backlog_report['incoming'] 
            percent = ( backlog_report['incoming_partner']  / float(total)) * 100
            backlog_report['incoming_percent'] = '{0:.1f}'.format(percent)

         if backlog_report['so_partner'] > 0:
            total = backlog_report['so_partner'] + backlog_report['so'] 
            percent = ( backlog_report['so_partner']  / float(total)) * 100
            backlog_report['so_percent'] = '{0:.1f}'.format(percent)
            

        
         for key, value in status_dict.iteritems():   
             for item in product_status:
                 if key == item['status']:
                     backlog_report[key] = item['case_count']
        
         log.info(backlog_report)
         return backlog_report
    
    def save_backlog(self, data):
         try:
            backlog_data = BacklogReport.objects.create(**data)
            backlog_data.save()
            backlog_data = None
         except Exception, ex:
            log.exception("SQL Error encountered in client list.." + str(ex))