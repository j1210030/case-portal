# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from gcase.models import Case,Product, Component, GcaseUser, Partner
from django.utils.functional import lazy
from gcase.forms import CaseAddEditForm
from django.db import DatabaseError
from itertools import chain
from datetime import timedelta
from django.http import StreamingHttpResponse
from django.core.exceptions import ObjectDoesNotExist
import csv
from io import TextIOWrapper, StringIO
from io import BytesIO
import sys;
from django.template.defaultfilters import default
from django.db.models.query import prefetch_related_objects
from re import search
from gcase.views.period_set_views import PeriodSetView
log = logging.getLogger(__name__)


class CaseBaseView(View):
    
    cid = None
    hl = None;
    context_dict = {}
    choice_list={}
    case = None
    
    def check_request(self, data,idCheck):
    
        if 'hl' not in data and data['hl'] not in ['jp', 'ko','zh']:
            self.hl = 'jp'
        if idCheck == True: 
            if 'id' not in data or not is_integer(data['id']):
                log.error("Invalid case id or parameter missing..")
                messages.warning(self.request,'Invalid request, required parameter missing or incorrect')
                self.valid_request = False
            else:
                self.cid = data['id']
            
        self.context_dict['id'] = self.cid
        self.context_dict['view_name'] = 'gcase'
    
    def set_assignee_choices(self):
        fields = ('id','user.first_name', 'last_name','profile_pict')
        users = GcaseUser.objects.values_list('id','user__first_name', 'user__last_name','profile_pict').filter(user__is_active=True,case_handler=True).order_by('user__first_name')
       
        assignee_list=[]
        log.debug(" Data %s " % users )
      
        for item in users:
            #log.debug(" Data %s " % item[1]  )
            data={}
            data['id'] = item[0] 
            data['name'] = "%s %s" % (item[1], item[2])
            #data['name'] =
            #name =  "%s %s" % (item[1], item[2])
            assignee_list.append(data)
            
        log.debug(" List %s " , assignee_list )
        self.choice_list['assignee_list'] = assignee_list
        self.context_dict['assignee_list'] = assignee_list
        
    
    def set_product_choices(self):
        fields = ('id','name','active','logo_file')
        product_list = None
        try:
             product_list = Product.objects.only(*fields).filter(active=True).order_by('name')
             self.context_dict['product_list'] =product_list
        except Exception, ex:
            log.exception("SQL Error encountered in client list.." + str(ex))
            pass
        if not product_list:
            log.debug("No partner record exists....")
    
    def set_partner_choices(self):
        fields = ('id','name_english','name_locale','geo_location')
        partner_list = None
        try:
             partner_list = Partner.objects.only(*fields).order_by('name_english')
             self.context_dict['partner_list'] = partner_list
             return partner_list
        except Exception, ex:
            log.exception("SQL Error encountered in client list.." + str(ex))
            pass
        if not partner_list:
            log.debug("No partner record exists....")
    
    def get_case(self,data):
        case = None
        try:
           case = Case.objects.get(id=data['id'],language=data['language'])
        except Case.DoesNotExist, dEx:
            log.error("Case with id: [ %s ] does not exists. ", data['id'] )
            messages.warning(self.request,'Case with id [ %s ]  could not be found' % data['id']) 
        except Exception, ex:
            log.exception("Sql error encountered.." +  str(ex))
            messages.warning(self.request,'Internal server error has encountered!!')
            
        return case 
       
"""
List Components 
@request pattern:
/cases/
Order will be by name 

"""
class CaseListView(CaseBaseView, PeriodSetView):
    
    template_name='gcase/case/list_tab.html'
    
    def get(self, request):
        data=request.GET.copy()
        
        page =1
        if 'page' in data and is_integer(data['page']):
            page = data['page']
        
        
        self.context_dict = self.set_duration(data, self.context_dict, -2)
        
        search_result = self.filter(data)      
          
        case_list = search_result['case_list']
        count_list = search_result['count_info']
        
        self.set_product_choices()
        self.set_assignee_choices()
        
        self.context_dict['month_options'] = set_month_options()
        self.context_dict['from_year_options'] = set_year_options()
        self.context_dict['to_year_options'] = set_year_options()
        
       
        self.context_dict['language_choices'] = dict(settings.LANGUAGE_CHOICES)
        self.context_dict['status_choices'] = dict(settings.CASE_STATUS_CHOICES)
        self.context_dict['case_list'] = case_list;
        
        if 'cid' in data and len(data['cid'])>0:
            data['so'] = '1'
        
        self.context_dict['cond'] = data
        
        
        if 'csv' in data and  len(data['csv']):
            filename = 'case_%s%02d_%s%02d.csv'   % (data['from_year'],int(data['from_month']),data['to_year'],int(data['to_month']))
            log.info('File name: %s ' % (filename))
            return self.csv_download(case_list,filename) 
        else:   
            count_info = {}
            for key, value in self.context_dict['status_choices'].iteritems():
                count = 0;
                if count_list:
                    for data in count_list:
                        if key == data['status']:
                            count = data['total']
                            break
            
                count_info[key] = count
                 
            log.info(count_info)
            self.context_dict['count_info'] = count_info;
            
            return render(request, self.template_name,self.context_dict)
        
    """
    Perform Search
    """
    def filter(self,data):
        kwargs = {}
        args = ()
       
        from_days = get_days_in_month( int(data['from_year']), int(data['from_month']))
        
        from_dt = '%04d-%02d-%02d 23:59:59' % (int(data['from_year']), int(data['from_month']), from_days)
        until_dt = '%04d-%02d-01 00:00:00' % (int(data['to_year']), int(data['to_month']))
        
         
        from_dt = datetime.strptime(from_dt, '%Y-%m-%d %H:%M:%S') #23:59:59
        until_dt = datetime.strptime(until_dt, '%Y-%m-%d %H:%M:%S') # 00:00:00'
        
        log.info(' from data: %s , to date: %s ' % (from_dt, until_dt) )  
        
        case_list = None
        date_filter = Q(incoming_date__lte = from_dt, incoming_date__gte = until_dt)
        display_filter = Q()
        status_filter = Q();
        
        if 'component' in data and len(data['component']):
            kwargs['component'] = data['component']
            
        if 'language' in data and len(data['language']):
            kwargs['language'] = data['language']            
        
        if 'product' in data and len(data['product']):
            kwargs['product'] = data['product']
            
        if 'assignee' in data and len(data['assignee']):
            kwargs['gcase_user'] = data['assignee']
            
        if 'status' in data and len(data['status']):
            kwargs['status'] = data['status']
            
        if 'cid' in data and len(data['cid']):
            kwargs['id'] = data['cid']
            
        if 'display' in data and len(data['display']):
            if data['display'] == 'p':
                display_filter = Q(partner__isnull=False)
            if data['display'] == 'np':
                display_filter = Q(partner__isnull=True)
        
        if 'so' not in data:
            if 'cid' not in data or len(data['cid']) == 0:
                status_filter = ~Q(status='solution_offered')
            else:
                data['so'] = 1 
            
        word_filter = ~Q()
        if 'keyword' in data and len(data['keyword'])>1:
            word_filter = Q(subject__search=strip_tags(data['keyword'])) | Q(remarks__search=strip_tags(data['keyword'])) 
        search_results = {}
        try:            
            fields = ['id','subject','incoming_date', 'product','sub_product','component',
                      'partner','status','so_date','buganizer_number','language','week','gcase_user','difficulty_level','remarks']
                
            
            if 'cid' in data and len(data['cid']):
                search_results['case_list'] = Case.objects.filter(id=data['cid']).select_related('product','component','partner','gcase_user__user').order_by('-incoming_date')
                search_results['count_info'] = Case.objects.filter(id=data['cid']).values('status').\
                                annotate(total=Count('id')).order_by('status')
            
            else:    
                search_results['case_list'] = Case.objects.filter(date_filter,display_filter,status_filter, word_filter, *args, **kwargs).select_related('product','component','partner','gcase_user__user').order_by('-incoming_date')
                search_results['count_info'] = Case.objects.filter(date_filter,display_filter,status_filter, word_filter, *args, **kwargs).values('status').\
                                annotate(total=Count('id')).order_by('status')
            
           
            size = len(search_results['case_list'])
            log.info ( ' Size is: %d ' %  size)
            if size == 0:
                messages.warning(self.request,'Sorry, Case record could not be found!')
            if size == 1:
                if  search_results['case_list'][0].status == 'duplicate':
                    messages.warning(self.request,'Duplicate case!')
                    
                
            
            return search_results              
        except:
            log.exception("SQL Error Encountered in jd search.")
       

    
    def csv_download(self,case_list,filename):
        column_names = ['ID','Subject', 'Product', 'Sub product','Component','Incoming date',
                        'Week','Assignee','Partner','Status','So date']
        
        column_names = [unicode(i) for i in column_names]
        
    
        memory_file = BytesIO() 
      
        writer = csv.writer(memory_file)
        
        writer.writerow(column_names)
        count =0;
        for case in case_list:
            
            
            row = []
            row.append(case.id)
            row.append(unicode(case.subject).encode('utf-8'))
            row.append(case.product)
            row.append(unicode(case.sub_product).encode('utf-8'))
            row.append(case.component)
            row.append(unicode(case.incoming_date).encode('utf-8'))
            row.append(unicode(case.week).encode('utf'))
            row.append(case.gcase_user)
            row.append(case.partner)
            row.append(unicode(case.status).encode('utf-8'))
            row.append(unicode(case.so_date).encode('utf-8'))
 
            writer.writerow(row)
            count +=1
            
        response = HttpResponse( memory_file.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
        
        return response
        
    
"""
Component Delete Class Based View
It will physically delete the data
"""
class CaseDeleteView(CaseBaseView):
    
    def get(self,request):
        data=request.GET.copy()
        self.check_request(data,True)
        try:
           Case.objects.get(pk=self.cid, hl=self.hl).delete()
           messages.success(request,'Case record is successfully deleted.')
        except Exception, ex:
            log.exception("Sql error encountered.." +  str(ex))
            messages.error(request,'Failed to delete, server error has encountered') 
        return redirect('/components/')
    
    
class CasePartnerSetView(CaseBaseView):
    
    def get(self, request):
        data=request.GET.copy()   
        log.info(data)
        json_response = {} 
        try:
           case = Case.objects.get(pk=data['cid'], language=data['hl'])
           case.partner_id = data['partner_id']
           case.save(update_fields=['partner'])
           json_response['status'] = 'ok'
        except Exception, ex:
            log.exception("Sql error encountered.." +  str(ex))
            json_response['status'] = 'error'
        
        if request.is_ajax():
            json_data = None
            try:
                json_data = json.dumps(json_response,ensure_ascii="False")
            except:
                log.exception("Json Error: ")
                pass
            return HttpResponse(json_data, content_type='application/json,encoding=utf-8')
 
     
class CaseSetSoDateView(CaseBaseView):
    
    def get(self, request):
        data=request.GET.copy()   
        log.info(data['so_date'])
        json_response = {} 
    
        try:
            so_date = format_dt2(data['so_date'], False)
            if so_date is not None:
                so_week = get_sunday2(so_date,'YYYY-mm-dd')
                if so_week:
                   log.info(so_week)
                   case = Case.objects.get(pk=data['cid'], language=data['hl'])
                   case.so_date = so_date
                   case.so_week = so_week
                   case.save(update_fields=['so_date','so_week'])
                   json_response['status'] = 'ok'
                else:
                    json_response['status'] = 'invalid_date'
            else:
                json_response['status'] = 'invalid_date'
                
        except Exception, ex:
            log.exception("Sql error encountered.." +  str(ex))
            json_response['status'] = 'error'
        
        if request.is_ajax():
            json_data = None
            try:
                json_data = json.dumps(json_response,ensure_ascii="False")
            except:
                log.exception("Json Error: ")
                pass
            return HttpResponse(json_data, content_type='application/json,encoding=utf-8')       
        

class CaseSetBuganizerView(CaseBaseView):
    
    def get(self, request):
        data=request.GET.copy()   
        log.info(data)
        json_response = {} 
    
        try:
            case = Case.objects.get(pk=data['cid'], language=data['hl'])
            case.buganizer_number = data['buganizer']
            case.save(update_fields=['buganizer_number'])
            json_response['status'] = 'ok'
                
        except Exception, ex:
            log.exception("Sql error encountered.." +  str(ex))
            json_response['status'] = 'error'
        
        if request.is_ajax():
            json_data = None
            try:
                json_data = json.dumps(json_response,ensure_ascii="False")
            except:
                log.exception("Json Error: ")
                pass
            return HttpResponse(json_data, content_type='application/json,encoding=utf-8')   


       
"""
Class Based view for adding New Component Record
@access url: /case/add/?hl=XX
"""
class CaseAddView(CaseBaseView):                     
    error = False
    form_class = CaseAddEditForm
    
    template_name = 'gcase/case/input_modal.html'
    error = False
   
    def get(self,request):
        data=request.GET.copy()
        
        
        if 'referer' not in data or data['referer'] =='':
            referer = '/case/list'
            if 'HTTP_REFERER' in self.request.META:
                referer = self.request.META['HTTP_REFERER']
            self.context_dict['referer'] = referer;    
        
        fields = ('id','name','active','logo_file')
        product_list = None
        try:
             product_list = Product.objects.only(*fields).filter(active=True).order_by('name')
             self.context_dict['product_list'] =product_list
        except Exception, ex:
            log.exception("SQL Error encountered in client list.." + str(ex))
            pass
        if not product_list:
            log.debug("No partner record exists....")
            messages.warning(self.request,'Product record could not be found!')
        
        self.set_assignee_choices()
        form = self.form_class(choices=self.choice_list)
        self.context_dict['form'] = form
        self.context_dict['language_choices'] = dict(settings.LANGUAGE_CHOICES)
        self.context_dict['geo_location_choices'] = dict(settings.GEO_LOCATION_CHOICES);
        self.context_dict['assignee_list'] = self.choice_list['assignee_list']
        self.context_dict['action'] = 'add'
        
        return render(request, self.template_name,self.context_dict)
    
    @transaction.atomic()
    def post(self,request):
        
        data=request.POST.copy() 
        
        dt = None
        if data['case_date']:
            dt = format_dt2(data['case_date'], True)
            data['incoming_date'] = dt
           
        so_week = None
        if data['status'] == 'solution_offered' and data['so_date'] != '' and data['so_date'] is not None:
            so_week = get_sunday(data['so_date'],'YYYY-mm-dd')
            
        form = self.form_class(data or None)
        self.context_dict['form'] = form
        
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.product_id = data['product']
                instance.component_id = data['component']
                instance.gcase_user_id = data['gcase_user']
                instance.so_week = so_week
                
                instance.save()
                messages.success(request, 'New case is added successfully.')
                return redirect(data['referer'])
            except:
                log.exception("Error encountered: ")
                messages.error(request, 'Server error, failed to add case')
        else:
            log.error("Component Form validation has failed(Edit) -----");
            for error in form.errors.items():
                log.error("Error: %s ", error)
            messages.error(request, 'Error in input, please try again')
            
            return render(request, self.template_name,self.context_dict)
        

"""
This is the class based view for Partner data editing
@access url: /partner/edit/?id=XXX&hl=XXX
where XXX=> id of the partner & hl is the geo location
"""
class CaseUpdateView(CaseBaseView):
    template_name = 'gcase/case/input_modal.html'
    form_class = CaseAddEditForm
    error = False
    
    def get(self,request):
        data=request.GET.copy()
        case = None
        
        if 'referer' not in data or data['referer'] =='':
            referer = '/case/list'
            if 'HTTP_REFERER' in self.request.META:
                referer = self.request.META['HTTP_REFERER']
            self.context_dict['referer'] = referer;    
        
        
        if 'id' not in data and not len(data['id']) or 'language' not in data and not len(data['language']):
            log.error(' Invalid request, required parameter is missing!!')
            messages.warning(self.request,'Request is invalid, required parameter missing!!!')
            return redirect(self.context_dict['referer'])
        
        fields = ('id','name','active','logo_file')
        product_list = None
        try:
             product_list = Product.objects.only(*fields).filter(active=True).order_by('name')
             self.context_dict['product_list'] =product_list
        except Exception, ex:
            log.exception("SQL Error encountered in client list.." + str(ex))
            pass
        if not product_list:
            log.debug("No partner record exists....")
            messages.warning(self.request,'Case record could not be found!')
        
        self.set_assignee_choices()
        
        self.context_dict['language_choices'] = dict(settings.LANGUAGE_CHOICES)
        self.context_dict['geo_location_choices'] = dict(settings.GEO_LOCATION_CHOICES);
        self.context_dict['assignee_list'] = self.choice_list['assignee_list']
        self.context_dict['action'] = 'edit'
        
        case = self.get_case(data);
        if case is None:    
            return redirect(self.context_dict['referer'])
             
        form = self.form_class(choices=self.choice_list,instance=case)
        #form.case_date.value = '09/27/2017 14:23:17'
        form.fields["case_date"].initial = date_to_str(case.incoming_date, '%m/%d/%Y %H:%M:%S')
        self.context_dict['form'] = form
       
        return render(request, self.template_name,self.context_dict)

    @transaction.atomic()
    def post(self,request): 
        
        post=request.POST.copy()
        log.info(' id is %s ' % post['id'] )    
        
        #case = self.get_case(post);
        #if case is None:    
         #   messages.warning(self.request,'Case record could not be found, it might be deleted.!')
        
        try:
           case = Case.objects.get(id=post['id'])
        except Case.DoesNotExist, dEx:
            log.error("Case with id: [ %s ] does not exists. ", post['id'] )
            messages.warning(self.request,'Case with id [ %s ]  could not be found' % post['id']) 
            return redirect(post['referer'])
        except Exception, ex:
            log.exception("Sql error encountered.." +  str(ex))
            messages.warning(self.request,'Internal server error has encountered!!')
            return redirect(post['referer'])
        
        if post['case_date'] != date_to_str(case.incoming_date, '%m/%d/%Y %H:%M:%S'):
            post['incoming_date'] = format_dt2(post['case_date'], True)
        else:
            post['incoming_date'] = case.incoming_date
        
        so_week = None
        if post['status'] == 'solution_offered' and post['so_date'] != '' and post['so_date'] is not None:
            so_week = get_sunday(post['so_date'],'YYYY-mm-dd')
        else:
            so_week = case.so_week
            
        form = self.form_class(post,instance=case)  
        if form.is_valid():
            
            so_week = None
            if post['status'] == 'solution_offered' and post['so_date'] != '' and post['so_date'] is not None:
                so_week = get_sunday(post['so_date'],'YYYY-mm-dd')
            try: 
                instance = form.save(commit=False)
                #instance.id = post['id'] 
                instance.product_id = post['product']
                instance.component_id = post['component']
                instance.gcase_user_id = post['gcase_user']
                if so_week is not None:
                    instance.so_week = so_week
                    
                instance.save()
                messages.success(request,'Case record is updated successfully.')
            except Exception, ex:
                log.exception("Error encountered: " + str(ex))
                messages.error(self.request, 'Server error has encountered, failed to update record')

            return redirect(post['referer'])   
        else:
            log.error("Case Form validation has failed(Edit) -----");
            for error in form.errors.items():
                log.error("Error: %s ", error)
            messages.error(request, 'Error in input, please try again')

       
        self.context_dict['form'] = form 
         
        return render(request, self.template_name, self.context)
  
       

"""
Check and set week( Sunday of that date) from incoming date
@request parameter: incoming_dt  
"""
class GetWeekByDateView(CaseBaseView):
    error=False;
    json_response = {}
    def get(self,request):     
        data=request.GET.copy()
        log.debug(' incoming date is %s: ' % data['incoming_dt'])
        
        if 'incoming_dt' not in data:
            log.error("invalid request, incoming_dt is not set or incorrect..")   
            self.error=True
            self.json_response['status'] = 'ERROR'
            self.json_response['message'] = 'Invalid request.'
        
        week = None    
        if not self.error:
            week = get_sunday(data['incoming_dt'],None)
            log.debug(' Week is: %s ' % week )
            if week is None: 
                self.json_response['status'] = 'ERROR'
                self.json_response['message'] = 'Incorrect date, please input date in correct format.'
            else:
                self.json_response['status'] = 'SUCCESS'
                self.json_response['week'] = week
               
        if request.is_ajax():
            json_data = None
            try:
                json_data = json.dumps(self.json_response,ensure_ascii="False")
            except:
                log.exception("Json Error: ")
                pass
            return HttpResponse(json_data, content_type='application/json,encoding=utf-8')
        
# Check if case id already exixts or not        
class CaseIdCheck(CaseBaseView):
    error=False;
    json_response = {}
    def get(self,request):     
        data=request.GET.copy()
        log.debug(' id to check %s: ' % data['case_id'])
        
        if 'case_id' not in data:
            log.error("invalid request, incoming_dt is not set or incorrect..")   
            self.error=True
            self.json_response['status'] = 'ERROR'
            self.json_response['message'] = 'Invalid request.'
        
            
        if not self.error:
            case = None
            try:
                case = Case.objects.get(id=data['case_id'])
            
            except Case.DoesNotExist, dEx:
                 log.error("Case with id: [ %s ] does not exixts. ", data['case_id'] )
                 self.json_response['status'] = 'OK'
            except Exception, ex:
                log.exception("Sql error encountered.." +  str(ex))
            if case:
                log.error("Case with id: [ %s ] already exixts. ", data['case_id'] )
                self.json_response['status'] = 'EXISTS'     
               
        if request.is_ajax():
            json_data = None
            try:
                json_data = json.dumps(self.json_response,ensure_ascii="False")
            except:
                log.exception("Json Error: ")
                pass
            return HttpResponse(json_data, content_type='application/json,encoding=utf-8')