# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from .period_set_views import *
from gcase.models import BacklogReport, Product, Partner
from django.utils.functional import lazy
from django.db import DatabaseError
from itertools import chain
from datetime import timedelta
from django.http import StreamingHttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Avg, Max, Min
import csv
from io import TextIOWrapper, StringIO
from io import BytesIO
import sys;
from django.template.defaultfilters import default
from django.db.models.query import prefetch_related_objects
log = logging.getLogger(__name__)


class PartnerNonPartnerReportView(PeriodSetView):
    
    template_name='gcase/report/partner_nonpartner.html'
    context_dict = {}
    def get(self, request):
        data=request.GET.copy()
        
        self.context_dict = self.set_duration(data, self.context_dict, -1)        
        date_filter = self.set_date_filter(data,'week')
        
    
        self.context_dict['view_name'] = 'report'
        self.context_dict['action'] = 'partner'
        self.context_dict['period'] = '( %04s/%02s ~ %04s/%02s )' % (data['from_year'],data['from_month'],data['to_year'],data['to_month'])
        
        
        log.info(self.context_dict)

        total_list = None
       
        
        try:
            kwargs = {}
            args = ()
            
            total_list = BacklogReport.objects.filter(date_filter, *args, **kwargs).values('week').\
                            annotate(total_incoming=Sum('incoming'),total_incoming_partner=Sum('incoming_partner'),\
                                      avg_incoming_percent=Avg('incoming_percent'),total_so=Sum('so'),\
                                      total_so_partner=Sum('so_partner'),avg_so_percent=Avg('so_percent')\
                                     ).order_by('-week')
                           
            
            incoming_so_list = BacklogReport.objects.filter(date_filter,*args, **kwargs).order_by('-week')
            
            log.info(incoming_so_list)
                           
            self.context_dict['total_list'] = total_list
            self.context_dict['incoming_so_list'] = incoming_so_list
            
        except Exception, ex:
            log.exception("SQL Error Encountered in jd search. " + str(ex))
        return render(request, self.template_name,self.context_dict)
        

       