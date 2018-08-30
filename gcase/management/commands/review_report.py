# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from gcase.models import Case, ReviewRequestReport,ReviewRequest ,GcaseUser, Product,Partner,\
    review_request
#from gcase.common_views import *
from django.conf import settings
#from views.common_views import *
from gcase.views.common_views import *   #common_views import *
from Carbon.Events import app2Mask
import math
from datetime import timedelta

log = logging.getLogger(__name__)


class Command(BaseCommand):
    # help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
        #parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        
        # get current week
        # get previous week
        
        try:
            kwargs = {}
            args = ()
            review_request = {}
            date_str = '10/01/2017'
            dt = format_dt2(date_str,False)
            total_android = ReviewRequest.objects.filter(request_week=dt,case__product_id=1).values('request_week').annotate(request_count=Count('*')).order_by('-request_week')
            total_firebase = ReviewRequest.objects.filter(request_week=dt,case__product__id=2).values('request_week').annotate(request_count=Count('*')).order_by('-request_week')
            
            ok_android = ReviewRequest.objects.filter(received_week=dt,case__product__id=1,status='OK').values('received_week').annotate(ok_count=Count('*')).order_by('-received_week')
            ok_firebase = ReviewRequest.objects.filter(received_week=dt,case__product__id=2,status='OK').values('received_week').annotate(ok_count=Count('*')).order_by('-received_week')
         
            ng_android = ReviewRequest.objects.filter(received_week=dt,case__product__id=1,status='NG').values('received_week').annotate(ng_count=Count('*')).order_by('-received_week')
            ng_firebase = ReviewRequest.objects.filter(received_week=dt,case__product__id=2,status='NG').values('received_week').annotate(ng_count=Count('*')).order_by('-received_week')
        
            ok_ratio_android = None
            ok_ratio_firebase = None
            
            log.info(len(ok_android))
            log.info(len(ok_firebase))
            
            if len(ok_android) >0 and len(ng_android)>0:
                 total = ok_android[0]['ok_count'] + ng_android[0]['ng_count']  
                 ok_ratio_android = math.ceil( (ok_android[0]['ok_count']/total)*100 )
            elif ok_android is None:
                 ok_ratio_android = 0
            elif ng_android is None:
                ok_ratio_android = 100
        
            if len(ok_firebase)>0  and len(ng_firebase)>0:
                 total = ok_firebase[0]['ok_count'] + ng_firebase[0]['ng_count']  
                 ok_ratio_firebase = math.ceil( ( ok_firebase[0]['ok_count']/total)*100)
            elif len(ok_firebase)>0:
                 ok_ratio_firebase = 0
            elif len(ng_firebase)>0:
                 ok_ratio_firebase = 100

            data = self.create_data(dt, 1, total_android, ok_android, ng_android, ok_ratio_android)
            review_request_report = ReviewRequestReport.objects.create(**data)
            review_request_report.save()
            log.info(' Id is: %s ' % ( review_request_report.id))
         
         #data = self.create_data(dt, 2, total_firebase, ok_firebase, ng_firebase, ok_ratio_firebase)
         #review_request_report = ReviewRequestReport.objects.create(**data)
         #review_request_report.save() 
         
         
         
         #survey = get_object_or_404(Survey, created_by=request.user, pk=question_id)        
            
            
            
        #monthly = self.get_monthly(dt, 1)
            #log.info(monthly)     
                  
        except Exception, ex:
             log.exception("SQL Error Encountered in jd search. " + str(ex))

            
    def create_data(self,week, product_id, total, ok_info, ng_info, ok_ratio):
         review_request = {}
         review_request['week'] = week
         review_request['product_id'] = product_id
        
         if total is not None and len(total)>0:
             review_request['total_requested'] = total[0]['request_count']
         else:
            review_request['total_requested'] = 0
            
         if ok_info is not None and len(ok_info)>0:
             review_request['ok_count'] = ok_info[0]['ok_count']
         else:
            review_request['ok_count'] = 0
             
         if ng_info is not None and len(ng_info)>0:
             review_request['ng_count'] = ng_info[0]['ng_count']
         else:
            review_request['ng_count'] = 0
         
         review_request['ok_ratio'] = ok_ratio
         
         return review_request
    
    def get_monthly(self,week, product_id):
        
        try:
            kwargs = {}
            args = ()
            wks = timedelta(weeks = -4)
         
            until_dt = week + wks
            date_filter = Q(week__lte = week, week__gte = until_dt)
            kwargs['product_id'] = product_id
            monthly = ReviewRequestReport.objects.filter(date_filter,*args, **kwargs).aggregate(Avg('ok_ratio'))
            if monthly is not None:
                return monthly['ok_ratio__avg']
            else:
                return None
        except Exception, ex:
             log.exception("SQL Error Encountered in jd search. " + str(ex))
        
        