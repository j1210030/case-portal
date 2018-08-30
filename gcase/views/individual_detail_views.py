# -*- coding: utf-8 -*-
from .common_views import *
from gcase.models import IndividualReport,GcaseUser, individual_report
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


class IndividualDetailReportView(PeriodSetView):
    
    template_name='gcase/report/individual_by_member.html'
    context_dict = {}
    
    def get(self, request):
        self.context_dict = {}
        data=request.GET.copy()
        
        self.context_dict = self.set_duration(data, self.context_dict, -1)
        date_filter = self.set_date_filter(data,'week')
        self.context_dict['period'] = '( %04s/%02s ~ %04s/%02s )' % (data['from_year'],data['from_month'],data['to_year'],data['to_month'])
         
        backlog_list = None
        total_list = None
        
        total_report = []
        
        self.context_dict['action'] = 'individual_by_member'
        self.context_dict['view_name'] = 'report'
        
        try:
            kwargs = {}
            args = ()
            
            user_list =  GcaseUser.objects.filter(user__is_active=1,case_handler=True).select_related('user').order_by('user__first_name')
            self.context_dict['user_list'] = user_list
            
            if 'uid' not in data or len(data['uid'])== 0:
                gcase_user = GcaseUser.objects.get(user__id=request.user.id)
                log.info(gcase_user)
                data['uid'] = gcase_user.id
                self.context_dict['user'] = '%s %s' % ( gcase_user.user.first_name,  gcase_user.user.last_name)
            else: 
                for item in user_list:
                    if int(item.id) == int(data['uid']):                     
                        self.context_dict['user'] = '%s %s ' % (item.user.first_name, item.user.last_name)
                        break
                    
            kwargs['gcase_user_id'] = data['uid']
            week_list = IndividualReport.objects.values('week').distinct().filter(date_filter, *args, **kwargs).order_by('-week')   
            report_list = IndividualReport.objects.filter(date_filter, *args, **kwargs).order_by('-week')
                
            self.context_dict['uid'] = int(data['uid'])           
            self.context_dict['week_list'] = week_list     
            self.context_dict['report_list'] = report_list
                    
        except Exception, ex:
            log.exception("SQL Error Encountered  " + str(ex))
        
        return render(request, self.template_name,self.context_dict)
    

    