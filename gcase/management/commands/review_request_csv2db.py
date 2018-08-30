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

log = logging.getLogger(__name__)

class Command(BaseCommand):
  
    def handle(self, *args, **options):
        
        csvFile = '/Users/suhasg/Devel/python.proj/dev_support/csv/Review_Status_1111.csv'
        
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
                
                if int(row[0]) <= 485:
                    continue
                  
                # status : 9
                if row[12] == '01_OK':
                    data['status'] = 'OK'
                elif row[12] == '02_NG':
                    data['status'] = 'NG'
                elif row[9] == '03_Canceled':
                    data['status'] = 'Cancelled'
                else:
                    data['status'] = 'Open'
                
                data['case_id'] = row[1]
                db_result = None
                
                try:
                    db_result = ReviewRequest.objects.filter(case_id=row[1])
                except Exception, ex:
                        log.exception("SQL Error encountered in client list.." + str(ex))
                
                if db_result:
                    log.info(db_result)
                  
                data['case_id'] = row[1].strip()
                if data['case_id'] is None or data['case_id'] == '':
                    break
               
                dt = format_dt2(row[6], False) 
                
                log.info('request data: %s ' % dt)
                
                data['requested_on'] =  dt 
                data['request_week'] = get_sunday2(dt,None) 
                data['email_title'] = row[11]
                data['agent_remarks'] = row[15]
                
                try:
                    
                    data = ReviewRequest.objects.create(**data)
                    data.save()
                
                except Exception, ex:
                    log.exception("SQL Error encountered in client list.." + str(ex)) 
                 
                log.info("------------------------------------------------------------------Loop is %s" % loop)
                loop = loop +1
                log.info(data)
                
