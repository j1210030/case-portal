# -*- coding: utf-8 -*-
"""
This is the class based report view for Review Request
"""
from .common_views import *
from gcase.models import ReviewRequestReport
from django.utils.functional import lazy
from django.db import DatabaseError
from itertools import chain
from datetime import timedelta
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
from gcase.views.period_set_views import PeriodSetView
log = logging.getLogger(__name__)


class ReviewRequestQualityReportView(PeriodSetView):
    
    template_name='gcase/report/review_request.html'
    context_dict = {}
    def get(self, request):
        
        data=request.GET.copy()
        self.context_dict = self.set_duration(data, self.context_dict, -2)  
        date_filter = self.set_date_filter(data, 'week')
        
        try:
            kwargs = {}
            args = ()
            
            week_list_android = ReviewRequestReport.objects.values('week').distinct().filter(date_filter, product_id=1).order_by('week')
            week_list_firebase = ReviewRequestReport.objects.values('week').distinct().filter(date_filter, product_id=2).order_by('week')
            
            total_list = ReviewRequestReport.objects.filter(date_filter, *args, **kwargs).values('week').\
                            annotate(total_ok=Sum('ok_count'),
                                     total_ng=Sum('ng_count'),avg_ok_ratio=Avg('ok_ratio'),
                                     avg_monthly_percent=Avg('monthly_ratio')
                                     ).order_by('-week')
                                     
            review_list = ReviewRequestReport.objects.filter(date_filter, *args, **kwargs).select_related('product').order_by('-week')
                            
            
            self.context_dict['week_list_android'] = week_list_android
            self.context_dict['week_list_firebase'] = week_list_firebase                   
            self.context_dict['total_list'] = total_list
            self.context_dict['review_list'] = review_list
            
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
        #else:    
            #return backlog_list
        
        return render(request, self.template_name,self.context_dict)
        
               