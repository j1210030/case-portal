# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from gcase.models import Product
from django.utils.functional import lazy
from gcase.forms import ProductAddEditForm
from django.db import DatabaseError
from itertools import chain

log = logging.getLogger(__name__)


class ProductBaseView(View):
    
    pid = None
    context_dict = {}
    product = None
    
    def set_data(self):
        
        try:
            self.product = Product.objects.get(pk=self.pid)
            self.context_dict['product'] = self.product
        except Product.DoesNotExist:
            log.error("There is no product record with id: %s ", self.pid)
            messages.warning(self.request,'Product record could not be found!')
        except DatabaseError, dbEx:
            log.error("SQL error encountered: " + str(dbEx))
    
    def check_request(self, data,idCheck):
    
        if idCheck == True: 
            if 'id' not in data or not is_integer(data['id']):
                log.error("Invalid candidate id or parameter missing..")
                messages.warning(self.request,'Invalid request, required parameter missing or incorrect')
                self.valid_request = False
            else:
                self.pid = data['id']
            
        self.context_dict['id'] = self.pid
        self.context_dict['view_name'] = 'product'
        
               
    
"""
List Products 
@request pattern:
/products/
Order will be by name 

"""
class ProductListView(ProductBaseView):
    template_name='gcase/product/list.html'
    def get(self, request):
        data=request.GET.copy()
        self.check_request(data,False)
        fields = ('id','name','active','logo_file')
        products = None
        try:
             products = Product.objects.only(*fields).order_by('name')
             self.context_dict['product_list'] = products
        except Exception, ex:
            log.exception("SQL Error encountered in client list.." + str(ex))
            pass
        if not products:
            log.debug("No partner record exists....")
            messages.warning(self.request,'Product record could not be found!')
        
        self.context_dict['view_name'] = 'product'
        return render(request, self.template_name,self.context_dict)


"""
Product Delete Class Based View
It will not physically delete the data , rather just set the active column value
to False
"""
class ProductDeleteView(ProductBaseView):
    
    def get(self,request):
        data=request.GET.copy()
        self.check_request(data,True)
        try:
           Product.objects.get(pk=self.pid).delete()
           messages.success(request,'Product is successfully deleted.')
        except Exception, ex:
            log.exception("Sql error encountered.." +  str(ex))
            messages.error(request,'Failed to delete, server error has encountered') 
        return redirect('/products/')
        
"""
Class Based view for adding New Product Record
@access url: /product/add/
"""
class ProductAddView(ProductBaseView):                     
    template_name = 'gcase/product/input.html'
    form_class = ProductAddEditForm
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
        form = self.form_class(request.POST or None,request.FILES)
        if form.is_valid():
            try:
               instance = form.save(commit=False)
               instance.save()
               messages.success(request, 'New product is added successfully.')
            except:
                log.exception("Error encountered: ")
                messages.error(request, 'Server error, failed to add partner')
            return redirect('/products/')
        else:
            log.error("Partner Form validation has failed:(Add)-----");
            for error in form.errors.items():
                log.error("Error: %s ", error)
            messages.error(request, 'Error in input, please try again')
        self.context_dict['form'] = form
        self.context_dict['view_name'] = 'product'
        self.context_dict['action'] = 'add'
        
        return render(request,self.template_name,self.context)


"""
This is the class based view for Product data editing
@access url: /product/edit/?id=XXX
where XXX=> id of the product
"""
class ProductUpdateView(ProductBaseView):
    template_name = 'gcase/product/input.html'
    form_class = ProductAddEditForm
    error = False
    
    def get(self,request):
        data=request.GET.copy()
        self.check_request(data,True)
        self.set_data()
        if not self.product:
            return redirect('/products/')
      
        form = self.form_class(instance=self.product)
        self.context_dict['form'] = form
        self.context_dict['view_name'] = 'product'
        self.context_dict['action'] = 'edit'
        
        return render(request, self.template_name,self.context_dict)

    @transaction.atomic()
    def post(self,request): 
        post=request.POST.copy()    
        for key, value in post.items():
            log.debug("key is %s and value is : %s ",key,value)
        
        self.check_request(post,True)
       
        partner = None
        try:
           partner = Product.objects.get(pk=self.pid)
        except Exception, ex:
            log.exception("Sql error encountered.." +  str(ex))
        if not partner:
            log.error("No partner record for id: %s ", self.pid )
            messages.warning(request,'Product record could not be found')
            return redirect('/products/')
        
        form = self.form_class(post,request.FILES,instance=partner)  
        if form.is_valid():
            try: 
                instance = form.save(commit=False)
                instance.save() 
                messages.success(request,'Product is updated successfully.')
            except Exception, ex:
                log.exception("Error encountered: " + str(ex))
                messages.error(self.request, 'Error has encountered, failed to update record')

            return redirect('/products/')   
        else:
            log.error("Partner Form validation has failed(Edit) -----");
            for error in form.errors.items():
                log.error("Error: %s ", error)
            messages.error(request, 'Error in input, please try again')

        self.context_dict['view_name'] = 'product'
        self.context_dict['action'] = 'edit'
        self.context_dict['form'] = form 
         
        return render(request, self.template_name, self.context)



