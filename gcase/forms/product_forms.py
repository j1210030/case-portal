# -*- coding: utf-8 -*-

"""
@Note: This is the form class for Product
@File: product_forms.py
"""
from .common_forms import *
from gcase.models import Product

from django.utils.translation import ugettext_lazy as _

log = logging.getLogger(__name__)

"""
Common Base Form will be inherited by
others
"""

class ProductBaseForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        super(ProductBaseForm,self).__init__(*args,**kwargs)
        
    def set_form_element(self):
        self.fields['active'].choices = settings.PARTNER_STATUS_CHOICES
        

"""
Partner Add/Edit Form 
"""        
class ProductAddEditForm(ProductBaseForm):
    logo_file = forms.ImageField(widget=forms.FileInput,required=False)
    def __init__(self,*args,**kwargs):
        super(ProductAddEditForm,self).__init__(*args,**kwargs)
        self.set_form_element()
        self.fields['name'].widget.attrs = {'class': 'form-control col-md-7 col-xs-12','data-parsley-maxlength':'42','data-parsley-trigger':'change','required':'required'}
        self.fields['active'] =  forms.ChoiceField(choices=settings.PARTNER_STATUS_CHOICES, widget=forms.RadioSelect(),initial=True)
        self.fields['active'].widget.attrs ={'class':'flat'}
        self.fields['logo_file'].widget.attrs = {'placeholder':'PNG, JPEG, GIF (3Mb)'}
    
    class Meta:
        model = Product
        exclude = ['modified']
        
