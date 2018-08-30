# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from gcase.models import Case,ReviewRequest, GcaseUser
from django.utils.functional import lazy
from gcase.forms import ReviewRequestAddEditForm
from django.db import DatabaseError
from itertools import chain
from datetime import timedelta
from django.shortcuts import get_object_or_404
import csv
import gcase

log = logging.getLogger(__name__)


class ReviewRequestCsv2DbView(View):
    context_dict = {}
    template_name='gcase/review_request/tmp.html'
    form_class = ReviewRequestAddEditForm
    def get(self, request):
        csvFile = '/Users/suhasg/Devel/python.proj/dev_support/csv/ReviewRequest.csv'
        fields = ('case_id','email_title','requested_on','status','requested_on','agent_remarks')
        #data_list = ReviewRequest.objects.only(*fields).order_by('name')
        review_list = []
        with open(csvFile) as file:
            reader = csv.reader(file)
            loop = 0;
            log.info('---CSV Reading-------')
            for row in reader:
                #log.info(row)
                
                data = {}
                #data['no'] = row[0]
                if len(row) == 0:
                    continue
                
                if row[1] is None or row[1] == '': #or row[1] == '9-5410000011505':
                  break
              
                # status : 9
                if row[12] == '01_OK':
                    data['status'] = 'OK'
                elif row[12] == '02_NG':
                    data['status'] = 'NG'
                elif row[9] == '03_Canceled':
                    data['status'] = 'Cancelled'
                else:
                    data['status'] = 'Open'
                
                data['case'] = row[1]
                result = None
                try:
                    result = ReviewRequest.objects.filter(case_id=row[1])
                except Exception, ex:
                        log.exception("SQL Error encountered in client list.." + str(ex))
                
                #if result:
                    #log.info(' Case with id: %s already exists , omitting!!!' % row[1] )
                    #if data['status']  == result['status']:
                     #   continue
                
                data['case'] = row[1]
                if data['case'] is None or data['case'] == '':
                    break
                #if data['case'] ==  '5-9579000010001': #'7-5660000009854':
                 #   break
                    
                dt = format_dt2(row[6], False) 
                log.info('request data: %s ' % dt)
                data['requested_on'] =  dt 
                data['request_week'] = format_dt2(row[7], False) 
                data['email_title'] = row[11]
                data['agent_remarks'] = row[15]
                    
                form = self.form_class(data or None)
                if form.is_valid():
                    try:
                        instance = form.save(commit=False)
                        instance.save()
                    except Exception, ex:
                        log.exception("SQL Error encountered in client list.." + str(ex))
                
                else:
                    log.error("Case Form validation has failed:(Add)-----");
                    for error in form.errors.items():
                        log.error("Error: %s , %s ", error , data['case'])
                
                #data['created'] = 
                #log.info(data)
                log.info("------------------------------------------------------------------Loop is %s" % loop)
                loop = loop +1
                log.info(data)
                review_list.append(data)
            
        self.context_dict['review_list'] = review_list
                #log.debug(data)
        return render(request, self.template_name,self.context_dict)


