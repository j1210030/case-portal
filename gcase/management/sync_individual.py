# -*- coding: utf-8 -*-
# - Sync Backlog
from django.core.management.base import BaseCommand, CommandError
from gcase.models import Case, IndividualReport,GcaseUser, individual_report

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
    
              
        try:
            kwargs = {}
            args = ()
            
            date_str = '09/24/2017'
            dt = format_dt2(date_str,False)
            
            count = 0;
            while (count < 1 ):
                next_dt = None
                try:
                    next_dt = dt + relativedelta(days=7)
                    #log.info(next_dt)
                except:
                    log.exception()
            
                data = IndividualReport.objects.filter(week=dt).order_by('gcase_user_id')
                data_next = IndividualReport.objects.filter(week=next_dt).order_by('gcase_user_id')
                self.adjust_backlog(data, data_next)
                dt=next_dt      
                count = count +1
                           
            
            #log.info('---------------------------------')
            #log.info(data)
             
            
        except Exception, ex:
             log.exception("SQL Error Encountered in jd search. " + str(ex))
    
    def adjust_backlog(self, data, next_data):
        
        for item in data:    
            pw_backlog = item.pw_backlog
            user_id = item.gcase_user.id
            log.info('pw backlog: %s , user: %s' % (pw_backlog,user_id))
            self.update_next_backlog(pw_backlog,user_id,next_data)
            
    
        
    def update_next_backlog(self,pw_count,user_id,next_data):
         for item in next_data:
             if item.gcase_user.id == user_id:
                 pw_backlog = (item.incoming + pw_count) - item.so
                 try:
                     item.pw_backlog = pw_backlog
                     item.save(update_fields=["pw_backlog"])  
                 except Exception, ex:
                     log.exception("SQL Error Encountered in jd search. " + str(ex))
                 break