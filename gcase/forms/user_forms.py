# -*- coding: utf-8 -*-

"""
@Note: This is the form class for Partner
@File: partner_forms.py
"""
from .common_forms import *
from gcase.models import GcaseUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

log = logging.getLogger(__name__)

"""
Common Base Form will be inherited by
others
"""

class UserBaseForm(forms.ModelForm):
    
    first_name = forms.CharField(required=False,max_length=50)
    last_name = forms.CharField(required=False,max_length=50)
    username = forms.CharField(required=False,max_length=15)
    password = forms.CharField(required=False,max_length=50)
    confirm_password = forms.CharField(required=False,max_length=50)
    joined_on = forms.CharField(required=False)
    released_on = forms.CharField(required=False)
    is_active = forms.BooleanField(required=True)
    is_superuser = forms.BooleanField(required=False)
     
    def __init__(self,*args,**kwargs):
        super(UserBaseForm,self).__init__(*args,**kwargs)
        
    def set_form_element(self):
        self.fields['is_active'].choices = settings.PARTNER_STATUS_CHOICES
        
     
class UserLoginForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(UserLoginForm,self).__init__(*args,**kwargs)
        
    class Meta:
        model = GcaseUser
        exclude = ['modified','gender']
        
class UserAddEditForm(UserBaseForm):
    def __init__(self,*args,**kwargs):
        super(UserAddEditForm,self).__init__(*args,**kwargs)
        self.set_form_element()
        self.fields['first_name'].widget.attrs = {'class': 'form-control col-md-7 col-xs-12'}
        self.fields['last_name'].widget.attrs = {'class': 'form-control  col-md-7 col-xs-12'}
        self.fields['username'].widget.attrs = {'class': 'form-control col-md-7 col-xs-12','placeholder':'(6~20) Characters','maxlength':'20'}
        self.fields['password'].widget.attrs = {'class': 'form-control col-md-7 col-xs-12','placeholder':'(6~20) Characters','maxlength':'20'}
        self.fields['confirm_password'].widget.attrs = {'class': 'form-control col-md-7 col-xs-12','placeholder':'(6~20) Characters','maxlength':'20'}
        
        self.fields['joined_on'].widget.attrs = {'class':'form-control','placeholder':'MM/DD/YYYY'}
        self.fields['released_on'].widget.attrs = {'class':'form-control','placeholder':'MM/DD/YYYY'}
        self.fields['is_active'] =  forms.ChoiceField(choices=settings.PARTNER_STATUS_CHOICES, widget=forms.RadioSelect(),initial=False)
        self.fields['is_active'].widget.attrs ={'class':'flat'}
        
        self.fields['gender'] =  forms.ChoiceField(choices=settings.GENDER_CHOICES, widget=forms.RadioSelect(),initial=False)
        self.fields['is_active'].widget.attrs ={'class':'flat'}
        
        self.fields['case_handler'].widget.attrs = {'class': 'form-control col-md-7 col-xs-12'}  
        
    class Meta:
        model = GcaseUser
        exclude = ['modified']
        
