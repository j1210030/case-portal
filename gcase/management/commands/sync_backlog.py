# -*- coding: utf-8 -*-
# - Sync Backlog
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
    
              
        try:
            kwargs = {}
            args = ()
            
            date_str = '11/12/2017'
            dt = format_dt2(date_str,False)
            
            count = 0;
            #while (count < 1 ):
            next_dt = None
            try:
                data = BacklogReport.objects.get(week=dt,product_id=2)
                log.info(data.pw_backlog)
                
            except:
                log.exception()
            
                
                #data_next = IndividualReport.objects.filter(week=next_dt).order_by('gcase_user_id')
            self.update_next_backlog(data,dt)
                #dt=next_dt      
                #count = count +1
                           
            
            #log.info('---------------------------------')
            #log.info(data)
             
            
        except Exception, ex:
             log.exception("SQL Error Encountered in jd search. " + str(ex))
        
        
    def update_next_backlog(self,data,dt):
         
         next_dt = dt + relativedelta(days=7)
         try:
             pw_backlog = data.pw_backlog + (data.incoming - data.forwarded) - data.so
             log.info(' Backlog for next week: %s ' % pw_backlog)
             next_data = BacklogReport.objects.get(week=next_dt,product_id=2)
             if next_data is not None:
                 next_data.pw_backlog = pw_backlog
                 next_data.save(update_fields=["pw_backlog"])            
         except:
             log.exception()
         
        