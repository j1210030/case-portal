# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from gcase.models import Partner
from django.utils.functional import lazy
from gcase.forms import PartnerAddEditForm
from django.db import DatabaseError
from itertools import chain
from django.utils.translation import ugettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.core import serializers

log = logging.getLogger(__name__)


class PartnerBaseView(View):
    
    pid = None
    hl = 'jp'
    context_dict = {}
    partner = None
    valid_request = True
    
    def set_data(self):
        
        try:
            self.partner = Partner.objects.get(pk=self.pid, geo_location=self.hl)
            self.context_dict['partner'] = self.partner
        except Partner.DoesNotExist:
            log.error("There is no partner record with id: %s ", self.pid)
            messages.warning(self.request,'Partner record could not be found!')
        except DatabaseError, dbEx:
            log.error("SQL error encountered: " + str(dbEx))
    
    def check_request(self, data,idCheck):
    
        log.debug("hl: %s ", data['hl'])
        
        if idCheck == True: 
            if 'id' not in data or not is_integer(data['id']):
                log.error("Invalid candidate id or parameter missing..")
                messages.warning(self.request,'Invalid request, required parameter missing or incorrect')
                self.valid_request = False
            else:
                self.pid = data['id']
        
        if 'hl' not in data or data['hl'] not in ['jp', 'ko','zh']:
            messages.warning(self.request,'Invalid request, required parameter missing or incorrect')
            self.valid_request = False
        else:
            self.hl = data['hl']
        
        
            
        self.context_dict['id'] = self.pid
        self.context_dict['hl'] = self.hl
        self.context_dict['action'] = self.hl
        self.context_dict['view_name'] = 'partner'
        self.context_dict['geo_location'] = dict(settings.GEO_LOCATION_CHOICES).get(self.hl)
               
    
"""
List Partner Records
@request pattern:
/partners/
Order will be by name and filter by Branch.

"""
class PartnerListView(PartnerBaseView):
    template_name='gcase/partner/list.html'
    def get(self, request):
        data=request.GET.copy()
        self.check_request(data,False)
        fields = ('id','name_english','name_locale','company_url','geo_location','is_active')
        partners = None
        try:
            partners = Partner.objects.only(*fields).filter(geo_location=data['hl']).order_by('name_english')
            self.context_dict['partner_list'] = partners
        except Exception, ex:
            log.exception("SQL Error encountered in client list.." + str(ex))
            pass
        if not partners:
            log.debug("No partner record exists....")
            messages.warning(self.request,'Partner record could not be found!')
        
        return render(request, self.template_name,self.context_dict)


class PartnerListJsonView(PartnerBaseView):
   
    
    def get(self, request):
        data=request.GET.copy()
        self.check_request(data,False)
        self.context_dict = {}
         
        if not self.valid_request:
            self.error=True
            self.context_dict['status'] = 'ERROR'
        else:
            fields = ('id','name_english','name_locale','company_url','geo_location','is_active')
            partners = None
            try:
                partners = Partner.objects.values(*fields).filter(geo_location=data['hl'], is_active = True ).order_by('name_english')
            except Exception, ex:
                log.exception("SQL Error encountered in client list.." + str(ex))
                self.context_dict['status'] = 'ERROR'
                pass
        if not partners:
            self.context_dict['partner_list']=''
        else:
            log.debug(" Size is: %s " % len(partners))
            partner_list=[]
            for partner in partners:
                data={}
                data['id'] = partner['id']
                data['value'] = "%s(%s)" % (partner['name_english'], partner['name_locale'])
                partner_list.append(data)
                
            self.context_dict['partner_list'] = partner_list
        log.info(self.context_dict['partner_list'] )  
         
        if request.is_ajax():
            json_data = None
            try:
                #json_data = json.dumps(self.context_dict,cls = LazyEncoder,ensure_ascii="False")
               json_data = JsonResponse(self.context_dict,safe=False)
            except:
                log.exception("Json Error: ")
                pass
            return HttpResponse(json_data, content_type='application/json,encoding=utf-8')
        
        
        
"""
Class Based view for adding New Partner Record
@access url: /partner/add/?hl=XX
"""
class PartnerAddView(PartnerBaseView):                     
    template_name = 'gcase/partner/input.html'
    form_class = PartnerAddEditForm
    error = False
   
    def get(self,request):
        data=request.GET.copy()
        self.check_request(data,False)
           
        form = self.form_class()
        self.context_dict['form'] = form
        
        return render(request, self.template_name,self.context_dict)

    @transaction.atomic()
    def post(self,request):
        post=request.POST.copy()
        for key, value in post.iteritems():
            log.debug("key is %s and value is : %s ",key,value)
        form = self.form_class(request.POST or None, request.FILES)
        if form.is_valid():
            try:
               instance = form.save(commit=False)
               instance.save()
               messages.success(request, 'New partner is added successfully.')
            except:
                log.exception("Error encountered: ")
                messages.error(request, 'Server error, failed to add partner')
            return redirect('/partner/?hl=' + post['hl'])
        else:
            log.error("Partner Form validation has failed:(Add)-----");
            for error in form.errors.items():
                log.error("Error: %s ", error)
            messages.error(request, 'Error in input, please try again')
        self.context_dict['form'] = form
        self.context_dict['hl'] = post['hl']
        self.context['view_name'] = 'partner'
        self.context['action'] = post['hl']
        self.context['geo_location'] = dict(settings.GEO_LOCATION_CHOICES).get(post['hl'])
        return render(request,self.template_name,self.context)


"""
This is the class based view for Partner data editing
@access url: /partner/edit/?id=XXX&hl=XXX
where XXX=> id of the partner & hl is the geo location
"""
class PartnerUpdateView(PartnerBaseView):
    template_name = 'gcase/partner/input.html'
    form_class = PartnerAddEditForm
    error = False
    
    def get(self,request):
        data=request.GET.copy()
        self.check_request(data,True)
        self.set_data()
        partner = None
        try:
           partner = Partner.objects.get(pk=self.pid,geo_location=self.hl)
        except Exception, ex:
            log.exception("Sql error encountered.." +  str(ex))
        if not partner:
            log.error("No partner record for id: %s ", self.pid )
            messages.warning(request,'Partner record could not be found')
            return redirect('/partner/?hl='+self.hl)
        
              
        form = self.form_class(instance=partner)
        self.context_dict['form'] = form
       
        return render(request, self.template_name,self.context_dict)

    @transaction.atomic()
    def post(self,request): 
        post=request.POST.copy()    
        for key, value in post.items():
            log.debug("key is %s and value is : %s ",key,value)
        
        self.check_request(post,True)
       
        partner = None
        try:
           partner = Partner.objects.get(pk=self.pid,geo_location=self.hl)
        except Exception, ex:
            log.exception("Sql error encountered.." +  str(ex))
        if not partner:
            log.error("No partner record for id: %s ", self.pid )
            messages.warning(request,'Partner record could not be found')
            return redirect('/partner/?hl='+self.hl)
        
        form = self.form_class(post,request.FILES,instance=partner) 
         
        if form.is_valid():
            try: 
                form_instance = form.save(commit=False)
                form_instance.save()
                messages.success(request,'Record is updated successfully.')
            except Exception, ex:
                log.exception("Error encountered: " + str(ex))
                messages.error(self.request, 'Error has encountered, failed to update record')

            return redirect('/partner/?hl='+self.hl)   
        else:
            log.error("Partner Form validation has failed(Edit) -----");
            for error in form.errors.items():
                log.error("Error: %s ", error)
            messages.error(request, 'Error in input, please try again')

       
        self.context['form'] = form 
         
        return render(request, self.template_name, self.context)


class LazyEncoderDjango(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


