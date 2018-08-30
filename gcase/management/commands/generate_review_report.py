# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from gcase.models import Case, ReviewRequestReport, ReviewRequest , GcaseUser, Product, Partner
# from gcase.common_views import *
from django.conf import settings
# from views.common_views import *
from gcase.views.common_views import *  # common_views import *
#from Carbon.Events import app2Mask
import math
from datetime import timedelta
from django.db.models import Sum

log = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        try:
            kwargs = {}
            args = ()
            review_request = {}
            
            # date_str = '10/01/2017'
            # get request_week date
            sunday = get_sunday2(None, None);
            log.info('++ Sunday: %s ++' % sunday)
            batch_day_dt = datetime.strptime(sunday, '%Y-%m-%d') 
            dt = batch_day_dt + relativedelta(days=-7)
            log.info('++ Batch Day : %s ++' % batch_day_dt)
            
            # dt = format_dt2(date_str, False)
            # total_android = ReviewRequest.objects.filter(request_week=dt, case__product_id=1, (Q(status='OK') | Q(status='NG'))).values('request_week').annotate(request_count=Count('*')).order_by('-request_week')
            total_android = ReviewRequest.objects.filter(Q(request_week=dt) & Q(case__product_id=1) & (Q(status='OK') | Q(status='NG'))).values('request_week').annotate(request_count=Count('*')).order_by('-request_week')
            total_firebase = ReviewRequest.objects.filter(Q(request_week=dt) & Q(case__product_id=2) & (Q(status='OK') | Q(status='NG'))).values('request_week').annotate(request_count=Count('*')).order_by('-request_week')
            
            ok_android = ReviewRequest.objects.filter(request_week=dt, case__product_id=1, status='OK').values('request_week').annotate(ok_count=Count('*')).order_by('-request_week')
            ok_firebase = ReviewRequest.objects.filter(request_week=dt, case__product_id=2, status='OK').values('request_week').annotate(ok_count=Count('*')).order_by('-request_week')
         
            ng_android = ReviewRequest.objects.filter(request_week=dt, case__product_id=1, status='NG').values('request_week').annotate(ng_count=Count('*')).order_by('-request_week')
            ng_firebase = ReviewRequest.objects.filter(request_week=dt, case__product_id=2, status='NG').values('request_week').annotate(ng_count=Count('*')).order_by('-request_week')
        
            ok_ratio_monthly_android = self.get_monthly(batch_day_dt, 1, total_android, ok_android)
            ok_ratio_monthly_firebase = self.get_monthly(batch_day_dt, 2, total_firebase, ok_firebase)

            data = self.create_data(dt, 1, total_android, ok_android, ng_android, ok_ratio_monthly_android)
            review_request_report = ReviewRequestReport.objects.create(**data)
            review_request_report.save()
            log.info(' Id is: %s ' % (review_request_report.id))
            
            data = self.create_data(dt, 2, total_firebase, ok_firebase, ng_firebase, ok_ratio_monthly_firebase)
            review_request_report = ReviewRequestReport.objects.create(**data)
            review_request_report.save()
            log.info(' Id is: %s ' % (review_request_report.id))
         
        except Exception, ex:
             log.exception("SQL Error Encountered in jd search. " + str(ex))
            
    def create_data(self, week, product_id, total, ok_info, ng_info, monthly_ratio):
        review_request = {}
        review_request['week'] = week
        review_request['product_id'] = product_id
        
        if total is not None and len(total) > 0:
            review_request['total_requested'] = total[0]['request_count']
        else:
            review_request['total_requested'] = 0
            
        if len(ok_info) == 0:
            ok_count = 0
        else:
            ok_count = ok_info[0]['ok_count']
        
        if len(ng_info) == 0:
            ng_count = 0
        else:
            ng_count = ng_info[0]['ng_count']
        
        if ok_count == 0 and ng_count == 0:
            ok_ratio = None
        else:
            ok_ratio = math.ceil(ok_count / ((ok_count + ng_count) * 1.0) * 100)    
         
        review_request['ok_count'] = ok_count
        review_request['ng_count'] = ng_count
        review_request['ok_ratio'] = ok_ratio
        review_request['monthly_ratio'] = monthly_ratio
         
        return review_request
    
    # Getting monthly ok ratio in review-request
    def get_monthly(self, batch_day_dt, product_id, this_week_total_info, this_week_ok_info):
        
        try:
            kwargs = {}
            args = ()
         
            first_dt = batch_day_dt
            
            log.info("++ First day of the review report  ++")
            log.info(first_dt)
            
            last_dt = batch_day_dt + timedelta(weeks=-4)
            
            log.info("++ Last day of the review report  ++")
            log.info(last_dt)
            
            date_filter = Q(week__lte=first_dt, week__gte=last_dt)
            kwargs['product_id'] = product_id
            
            if this_week_total_info is not None and len(this_week_total_info) > 0:
                this_week_total_count = this_week_total_info[0]['request_count']
            else:
                this_week_total_count = 0
                
            if this_week_ok_info is not None and len(this_week_ok_info) > 0:
                this_week_ok_count = this_week_ok_info[0]['ok_count']
            else:
                this_week_ok_count = 0
            
            total_monthly = ReviewRequestReport.objects.filter(date_filter, *args, **kwargs).aggregate(Sum('total_requested'))
            ok_monthly = ReviewRequestReport.objects.filter(date_filter, *args, **kwargs).aggregate(Sum('ok_count'))

            if total_monthly is not None:
                before_three_weeks_total_count = total_monthly['total_requested__sum']
            else:
                before_three_weeks_total_count = 0
            
            if ok_monthly is not None:
                before_three_weeks_ok_count = ok_monthly['ok_count__sum']
            else:
                before_three_weeks_ok_count = 0
                
            total_monthly_count = before_three_weeks_total_count + this_week_total_count
            ok_monthly_count = before_three_weeks_ok_count + this_week_ok_count
            
            # monthly = ReviewRequestReport.objects.filter(date_filter, *args, **kwargs).aggregate(Avg('ok_ratio'))
            if (total_monthly_count == 0) & (ok_monthly_count == 0):
                return None
            else:
                return math.ceil((ok_monthly_count / (total_monthly_count * 1.0)) * 100)
        except Exception, ex:
             log.exception("SQL Error Encountered in jd search. " + str(ex))
        
