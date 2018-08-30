# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from gcase.models import ReviewRequest,Case
from django.utils.functional import lazy
from gcase.forms import ReviewRequestAddEditForm
from django.db import DatabaseError
from itertools import chain

log = logging.getLogger(__name__)


class ReviewRequestBaseView(View):
    
    cid = None
    context_dict = {}
    review_request = None
    valid_request = True
    def check_request(self, data):
    
         if 'id' not in data and not is_integer(data['id']):
            self.valid_request = False
         if 'case' not in data:
            self.valid_request = False
            
         if not self.valid_request:
            log.error("Invalid component id or parameter missing..")
            messages.warning(self.request,'Invalid request, required parameter missing or incorrect')
            
         self.context_dict['id'] = data['id']
         self.context_dict['case'] = data['case']
         self.context_dict['view_name'] = 'review_request'
    
    def get_review_request(self,data):
        review = None
        try:
           review = ReviewRequest.objects.get(id=data['id'],case__id=data['case'])
           self.context_dict['review_request'] = review
        except ReviewRequest.DoesNotExist, dEx:
            log.error("Case with id: [ %s ] does not exists. ", data['id'] )
            messages.warning(self.request,'Case with id [ %s ]  could not be found' % data['id']) 
        except Exception, ex:
            log.exception("Sql error encountered.." +  str(ex))
            messages.warning(self.request,'Internal server error has encountered!!')  
        return review
"""
List Components 
@request pattern:
/products/
Order will be by name 

"""
class ReviewRequestListView(ReviewRequestBaseView):
    template_name='gcase/review_request/list.html'
    def get(self, request):
        data=request.GET.copy()
        fields = ('cid','email_title','status','requested_on','feedback_received_on')
        review_request = None
        
        from_year = None
        from_month = None
        to_year = None
        to_month = None
        
        self.context_dict['product_list'] = get_product_list()
        if 'from_year' not in data and 'to_year' not in data:
            now = datetime.now()
            from_year = now.year
            from_month = now.month
        
            toDt = add_month(-1)
            to_year = toDt.year;
            to_month = toDt.month
            
            data['from_year']= from_year
            data['from_month'] = from_month
            data['to_year'] = to_year
            data['to_month'] = to_month
        else:
            from_year = int(data['from_year'])
            from_month = int(data['from_month'])
            to_year = int(data['to_year'])
            to_month = int(data['to_month'])    
        
        self.context_dict['month_options'] = set_month_options()
        self.context_dict['from_year_options'] = set_year_options()
        self.context_dict['to_year_options'] = set_year_options()
        
        self.context_dict['from_year'] = from_year
        self.context_dict['from_month'] = from_month;
        
        self.context_dict['to_year'] = to_year
        self.context_dict['to_month'] = to_month;
        self.context_dict['status_choices'] = dict(settings.CASE_REVIEW_STATUS_CHOICES)


        self.context_dict['view_name'] = 'review_request'
        self.context_dict['action'] = 'list'
        self.context_dict['cond'] = data
        
        
        from_days = get_days_in_month( int(data['from_year']), int(data['from_month']))
        
        from_dt = '%04d-%02d-%02d' % (int(data['from_year']), int(data['from_month']),from_days)
        until_dt = '%04d-%02d-01' % (int(data['to_year']), int(data['to_month']))
        
        from_dt = datetime.strptime(from_dt, '%Y-%m-%d') #23:59:59
        until_dt = datetime.strptime(until_dt, '%Y-%m-%d') # 00:00:00'
        
        log.info(' from data: %s , to date: %s ' % (from_dt, until_dt) )  
        date_filter = Q(requested_on__lte = from_dt, requested_on__gte = until_dt)
        review_request_list = []
        try:
             kwargs = {}
             args = ()
             if 'cid' in data and len(data['cid']):
                kwargs['case'] = data['cid']
            
             if 'product' in data and len(data['product']):
                 kwargs['case__product'] = data['product']
                 
             if 'status' in data and len(data['status']):
                 kwargs['status'] = data['status']
                
             review_request_list = ReviewRequest.objects.filter(date_filter, *args, **kwargs).select_related('case','case__product','case__partner','case__gcase_user__user').order_by('-requested_on', '-id')
             self.context_dict['review_list'] = review_request_list
        except Exception, ex:
            log.exception("SQL Error encountered in client list.." + str(ex))
            pass
        if not review_request_list:
            log.debug("No product record exists....")
            messages.warning(self.request,'Review record could not be found!.')
            
            
        return render(request, self.template_name,self.context_dict)
    
    
"""
Class Based view for adding New Component Record
@access url: /review_request/add/
"""
class ReviewRequestAddView(ReviewRequestBaseView):                     
    error = False
    form_class = ReviewRequestAddEditForm
    template_name = 'gcase/review_request/input.html'
    error = False
   
    def get(self,request):
        
        data=request.GET.copy()
        
        if 'referer' not in data or data['referer'] =='':
            referer = '/review_request/'
            if 'HTTP_REFERER' in self.request.META:
                referer = self.request.META['HTTP_REFERER']
            self.context_dict['referer'] = referer; 
        
        form = self.form_class()
        
        self.context_dict['form'] = form
        self.context_dict['case'] = data['cid']
        self.context_dict['status'] = dict(settings.CASE_REVIEW_STATUS_CHOICES);
        self.context_dict['action'] = 'add'
        
        return render(request, self.template_name,self.context_dict)
    
    
    @transaction.atomic()
    def post(self,request):
        #For finding the bug
        log.info("############ Start review request")
        
        data=request.POST.copy() 
        log.info(data)
        request_week = get_sunday(data['requested_on'],'YYYY-mm-dd')
        
        #For finding the bug
        log.info("############ request_week: " + request_week)
            
        form = self.form_class(data or None)
        self.context_dict['form'] = form
        log.info('Case id: %s' % data['case'])
        
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.case_id = data['case']
                instance.request_week = request_week
                
                instance.save()
                
                case = Case.objects.get(pk=data['case'])
                case.status  = 'review_requested'   
                case.save(update_fields=['status'])
                messages.success(request, 'New review request is added successfully.')
                    
                return redirect(data['referer'])
            except:
                log.exception("Error encountered: ")
                messages.error(request, 'Server error, failed to add case')
        else:
            log.error("Component Form validation has failed(Edit) -----");
            for error in form.errors.items():
                log.error("Error: %s ", error)
            messages.error(request, 'Error in input, please try again')
            
        return redirect(data['referer'])


class ReviewRequestUpdateView(ReviewRequestBaseView):
    template_name = 'gcase/review_request/input.html'
    form_class = ReviewRequestAddEditForm
    error = False
    
    def get(self,request):
        data=request.GET.copy()
        if 'referer' not in data or data['referer'] =='':
            referer = '/case/list'
            if 'HTTP_REFERER' in self.request.META:
                referer = self.request.META['HTTP_REFERER']
            self.context_dict['referer'] = referer;    
        
        self.check_request(data)
        review = self.get_review_request(data)
    
        form = self.form_class(instance=review)
        self.context_dict['form'] = form
        self.context_dict['case'] = data['case']
        self.context_dict['id'] = data['id']
        self.context_dict['status'] = dict(settings.CASE_REVIEW_STATUS_CHOICES);
        self.context_dict['action'] = 'edit'
       
        return render(request, self.template_name,self.context_dict)
    
    @transaction.atomic()
    def post(self,request): 
        
        post=request.POST.copy()
        review = self.get_review_request(post)

        if review is None:    
            messages.warning(self.request,'Review record could not be found, it might be deleted.!')
            return redirect(post['referer'])
        
        #adjust request_week
        request_week = get_sunday(post['requested_on'],'YYYY-mm-dd')
            
        form = self.form_class(post,instance=review)
        if form.is_valid():
        
            try: 
                instance = form.save(commit=False)
                instance.request_week = request_week
                instance.save()
                
                messages.success(request,'Review request record is updated successfully.')
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
        