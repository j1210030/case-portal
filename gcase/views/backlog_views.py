# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from gcase.models import BacklogReport
from django.utils.functional import lazy
from gcase.forms import CaseAddEditForm
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


class BacklogReportView(PeriodSetView):
    
    template_name='gcase/report/backlog.html'
    context_dict = {}
    def get(self, request):
        
        data=request.GET.copy()
        self.context_dict = self.set_duration(data, self.context_dict, -1)
        log.info( self.context_dict)
        date_filter = self.set_date_filter(data,'week')
        self.context_dict['period'] = '( %04s/%02s ~ %04s/%02s )' % (data['from_year'],data['from_month'],data['to_year'],data['to_month'])

        self.context_dict['view_name'] = 'report' # templates/common/side_navogation.html
        self.context_dict['action'] = 'backlog' # templates/common/side_navogation.html
        
          
        self.context_dict['total_list'] = self.get_total_backlog(date_filter, 'desc')
        self.context_dict['backlog_list'] = self.get_backlog_list(date_filter, 'desc')
            
       
        return render(request, self.template_name,self.context_dict)
        
    # Total backlog group by week
    def get_total_backlog(self, date_filter, order):   
        total_list = None
       
        try:
            if order == 'asc':
                order = 'week'
            else:
                order = '-week'
                
            kwargs = {}
            args = ()
            
            total_list = BacklogReport.objects.filter(date_filter, *args, **kwargs).values('week').\
                            annotate(total_assigned=Sum('assigned'),total_needinfo=Sum('needinfo'),
                                     total_blocked=Sum('blocked'),total_inconsult=Sum('inconsult'),
                                     total_forwarded=Sum('forwarded'),total_review_requested=Sum('review_requested'),
                                     total_so = Sum('so'), total_so_partner = Sum('so_partner')
                                     ).order_by(order)     
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
        
        return total_list
    
    # Backlog detail group by week
    def get_backlog_list(self,date_filter, order):
         
         backlog_list = None
         try:
             if order == 'asc':
                order = 'week'
             else:
                order = '-week'
                
             kwargs = {}
             args = ()
             backlog_list = BacklogReport.objects.filter(date_filter, *args, **kwargs).order_by(order)
         except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
         return backlog_list