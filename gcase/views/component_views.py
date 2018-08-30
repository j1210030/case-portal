# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from gcase.models import Component,Product
from django.utils.functional import lazy
from gcase.forms import ComponentAddEditForm
from django.db import DatabaseError
from itertools import chain
from django.core import serializers
from django.http import JsonResponse

log = logging.getLogger(__name__)


class ComponentBaseView(View):
    
    cid = None
    context_dict = {}
    component = None
    
    def check_request(self, data,idCheck):
    
        if idCheck == True: 
            if 'id' not in data or not is_integer(data['id']):
                log.error("Invalid component id or parameter missing..")
                messages.warning(self.request,'Invalid request, required parameter missing or incorrect')
                self.valid_request = False
            else:
                self.cid = data['id']
            
        self.context_dict['id'] = self.cid
        self.context_dict['view_name'] = 'component'
        
    """
    Check if name is already registered.
    """
    def is_name_registered(self,data):
        cm=None
        try:
            if data['cid'] != '':  
                cm = Component.objects.only('id').filter(product_id=data['pid'], name__iexact=data['cname']).exclude(pk=data['cid'])
            else:
                cm = Component.objects.only('id').filter(product_id=data['pid'], name__iexact=data['cname'])
        except:
            log.exception("SQL Error encountered")
        if cm is not None and len(cm)>0:
            log.debug("Email is already registered:")
            return True
        else:
            return False
    
"""
List Components 
@request pattern:
/products/
Order will be by name 

"""
class ComponentListView(ComponentBaseView):
    template_name='gcase/component/list.html'
    def get(self, request):
        data=request.GET.copy()
        fields = ('id','name','active')
        components = None
        pid = None
        
        try:
             products = Product.objects.order_by('name')
             
             if products:
                if 'pid' not in data or not is_integer(data['pid']):
                    pid = products[0].id
                else:
                    pid = data['pid']
            
             product = Product.objects.get(pk=pid)
             if not product:
                 messages.warning(self.request,'Product record could not be found!, add product first.')
                 return redirect('/components/')
                 
             log.debug(' pid: %s ', pid )
             self.context_dict['product_list'] = products
             self.context_dict['product'] = product
             self.context_dict['selectedProductId'] = pid
             components = Component.objects.only(*fields).filter(product_id=pid).order_by('name')
             self.context_dict['component_list'] = components
        except Exception, ex:
            log.exception("SQL Error encountered in client list.." + str(ex))
            pass
        if not products:
            log.debug("No product record exists....")
            messages.warning(self.request,'Product record could not be found!, add product first.')
            return redirect('/products/')
            
        if not components:
            log.debug("No component record exists....")
            messages.warning(self.request,'Component record could not be found!')
        
        self.context_dict['view_name'] = 'component'
        return render(request, self.template_name,self.context_dict)


"""
Component Delete Class Based View
It will not physically delete the data , rather just set the active column value
to False
"""
class ComponentDeleteView(ComponentBaseView):
    
    def get(self,request):
        data=request.GET.copy()
        self.check_request(data,True)
        try:
           Component.objects.get(pk=self.pid).delete()
           messages.success(request,'Component is successfully deleted.')
        except Exception, ex:
            log.exception("Sql error encountered.." +  str(ex))
            messages.error(request,'Failed to delete, server error has encountered') 
        return redirect('/components/')
        
"""
Class Based view for adding New Component Record
@access url: /component/add/
"""
class ComponentAddView(ComponentBaseView):                     
    error = False
    form_class = ComponentAddEditForm
    
    @transaction.atomic()
    def post(self,request):
        data=request.POST.copy()   
        form = self.form_class(data or None)
        self.context_dict['form'] = form
        
        if form.is_valid():
            try:
               instance = form.save(commit=False)
               instance.product_id = data['pid']
               instance.save()
               messages.success(request, 'New component is added successfully.')
            except:
                log.exception("Error encountered: ")
                messages.error(request, 'Server error, failed to add partner')
        else:
            log.error("Component Form validation has failed(Edit) -----");
            for error in form.errors.items():
                log.error("Error: %s ", error)
            messages.error(request, 'Error in input, please try again')
            
        return redirect('/components/?pid=%s' % data['pid'])
        
"""
This is the class based view for Component data editing
@access url: /component/edit/?id=XXX
where XXX=> id of the product
"""
class ComponentUpdateView(ComponentBaseView):
    
    form_class = ComponentAddEditForm
    error = False
    
    @transaction.atomic()
    def post(self,request):
        data=request.POST.copy()
        log.info(' id: ' + data['id'] + ' pid:' + data['pid'])
        self.check_request(data,True)
        self.component = Component.objects.get(pk=data['id'], product_id=data['pid'])
        form = self.form_class(data,instance=self.component)
        
        if form.is_valid():
            try: 
                instance = form.save(commit=False)
                instance.save() 
                messages.success(request,'Component is updated successfully.')
            except Exception, ex:
                log.exception("Error encountered: " + str(ex))
                messages.error(self.request, 'Error has encountered, failed to update record')   
        else:
            log.error("Component Form validation has failed(Edit) -----");
            for error in form.errors.items():
                log.error("Error: %s ", error)
            messages.error(request, 'Error in input, please try again')
        
        return redirect('/components/?pid=%s' % data['pid'])


"""
Check If Name is already registered or not
/component/ajax_check_name/?name=SSS&pid=ddd
Ajax Post Method
"""
class ComponentCheckNameView(ComponentBaseView):
    
    def get(self,request):
        json_context_dict = {}
        json_context_dict["status"]="SUCCESS"
        data = request.GET.copy()
        log.debug("Data is : %s ", data )
        if self.is_name_registered(data):
            json_context_dict["allowed"]="-1"
        else:
            json_context_dict["allowed"]="1"
        json_data=None
        try:
            json_data = json.dumps(json_context_dict)
        except:
            log.exception("Json Error: ")
            pass   
        return HttpResponse(json_data, content_type='application/json,encoding=utf-8')



"""
Reload Component by product View
@request parameter: pid ( id of the product) 
"""
class GetByProductView(ComponentBaseView):
    error=False;
    def get(self,request):
        self.context_dict ={}     
        data=request.GET.copy()
        log.debug(' pid is ' + data['pid'])
        
        if 'pid' not in data or not is_integer(data['pid']):
            log.error("invalid request, cid is not set or incorrect..")   
            self.error=True
            self.context_dict['status'] = 'ERROR'
        
        components = None    
        if not self.error:
            try:
                fields=('id','name')
                components = Component.objects.values(*fields).filter(product_id=data['pid'],active=True).order_by('name')
                self.context_dict['status'] = 'SUCCESS'
            except:
                log.exception("SQL Error encountered: ")
                self.context_dict['status'] = 'ERROR'
        
        if not components:
            self.context_dict['components']=''
        else:
            self.context_dict['components']=list(components)
           
        if request.is_ajax():
            
            json_data = None
            response_data=None
            try:
                #json_data = json.dumps(self.context_dict,cls = LazyEncoder,ensure_ascii="False")
                #response_data = serializers.serialize('json', self.context_dict)
                json_data = JsonResponse(self.context_dict,safe=False)
            except:
                log.exception("Json Error: ")
                pass
            return HttpResponse(json_data,content_type='application/json,encoding=utf-8')
            #return HttpResponse(JsonResponse(response_data), content_type="application/json,encoding=utf-8")
        else:
            if not components:
                messages.warning(request, "Component could not be found")
            return HttpResponse(json_data, content_type='application/json,encoding=utf-8')      
        