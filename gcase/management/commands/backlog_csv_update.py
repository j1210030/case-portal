# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from gcase.models import Case, Partner,Product ,GcaseUser, ReviewRequest
#from gcase.common_views import *
from django.conf import settings
from gcase.forms import ReviewRequestAddEditForm
from gcase.views.common_views import *
from Carbon.Events import app2Mask
import math
import csv
from datetime import timedelta
from gcase.models.backlog_report import BacklogReport

log = logging.getLogger(__name__)

class Command(BaseCommand):
  
    def handle(self, *args, **options):
        
        csvFile = '/Users/suhasg/Devel/python.proj/dev_support/csv/backlog_firebase.csv'
        
        with open(csvFile) as file:
            
            reader = csv.reader(file)
            loop = 0;
            log.info('---CSV Reading-------')
            
            for row in reader:
                log.info(row)
                data = {}
               
                if len(row) == 0:
                    continue
                
                if row[1] is None or row[1] == '': #or row[1] == '9-5410000011505':
                    break
                
                  
                
                data['week'] = format_dt2(row[0],False)
                data['assigned'] = row[1]
                data['needinfo'] = row[2]
                data['inconsult'] = row[3]
                data['blocked'] = row[4]
                data['review_requested'] = row[5]
                
                
                db_result = None
                
                try:
                    db_result = BacklogReport.objects.get(week=data['week'], product_id=2)
                except Exception, ex:
                        log.exception("SQL Error encountered in client list.." + str(ex))
                
                if db_result:
                    log.info(db_result)
                  
                    try:
                        db_result.assigned =  data['assigned']
                        db_result.needinfo = data['needinfo']
                        db_result.inconsult = data['inconsult']
                        db_result.blocked = data['blocked']
                        db_result.review_requested = data['review_requested']
                        db_result.save(update_fields=['assigned','needinfo','inconsult','blocked','review_requested'])
                
                    except Exception, ex:
                        log.exception("SQL Error encountered in client list.." + str(ex)) 
                 
