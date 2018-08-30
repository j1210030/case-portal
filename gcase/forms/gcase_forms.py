# -*- coding: utf-8 -*-

"""
@Note: This is the form class for Case
@File: gcase_forms.py
"""
from .common_forms import *
from gcase.models import Component,Product,Case, Partner, GcaseUser

from django.utils.translation import ugettext_lazy as _
from gcase.apps import GcaseConfig

log = logging.getLogger(__name__)

"""
Common Base Form will be inherited by
others
"""

blank_choice = (('', 'Select'),)
class CaseBaseForm(forms.ModelForm):
    
    language = forms.ChoiceField(required=True)
    component = forms.ModelChoiceField(required=False,queryset=Component.objects.all())
    partner = forms.ModelChoiceField(required=False,queryset=Partner.objects.all())
    partner_geo = forms.ChoiceField(required=False,choices=blank_choice)
    difficulty_level = forms.ChoiceField(required=True)
    status = forms.ChoiceField(required=True)
    sub_product = forms.ChoiceField(required=False)
    case_date = forms.CharField(required = True)
    remarks = forms.CharField(required=False,max_length=1024,widget=forms.Textarea)
    
    def __init__(self,*args,**kwargs):
        super(CaseBaseForm,self).__init__(*args,**kwargs)
        
    def set_form_element(self):
        self.fields['status'].choices = settings.CASE_STATUS_CHOICES
        self.fields['sub_product'].choices = blank_choice + settings.SUB_PRODUCT_CHOICES
        self.fields['partner_geo'].choices = blank_choice + settings.GEO_LOCATION_CHOICES
        self.fields['difficulty_level'].choices = blank_choice + settings.CASE_DIFFICULTY_CHOICES
        self.fields['language'].choices = settings.LANGUAGE_CHOICES
        self.fields['week'].widget = forms.HiddenInput()
        self.fields['component'].empty_label="Select"
        self.fields['partner'].empty_label="Select"
        self.fields['sub_product'].empty_label="Select"
        
"""
Partner Add/Edit Form 
"""        
class CaseAddEditForm(CaseBaseForm):
    logo_file = forms.ImageField(widget=forms.FileInput,required=False)
 
    def __init__(self,*args,**kwargs):
        choices=None
        if 'choices' in kwargs:
            choices = kwargs.pop('choices')    
        super(CaseAddEditForm,self).__init__(*args,**kwargs)
        #updatable_field = list()
        #if choices is not None:
         #   self.fields['assignee'].queryset = choices['assignee_list']
            
        self.set_form_element()
        self.fields['id'].widget.attrs = {'class': 'form-control','data-parsley-maxlength':'100','placeholder':'Case id of gCase'}
        self.fields['case_date'].widget.attrs = {'class':'form-control','placeholder':'Ex:08/24/2017 20:34:56'}
        self.fields['so_date'].widget.attrs = {'class':'form-control','placeholder':''}
        self.fields['buganizer_number'].widget.attrs = {'class':'form-control','placeholder':'Enter id of buganizer'}
        self.fields['subject'].widget.attrs = {'class': 'form-control','data-parsley-maxlength':'100','data-parsley-trigger':'change','required':'required'}
        self.fields['component'].widget.attrs ={'class':'form-control'}
        self.fields['partner'].widget.attrs = {'class':'form-control'}
        self.fields['partner_geo'].widget.attrs = {'class':'form-control'}
        self.fields['difficulty_level'].widget.attrs = {'class':'form-control'}
        self.fields['status'].widget.attrs = {'class':'form-control'}
        self.fields['sub_product'].widget.attrs = {'class':'form-control'}
        self.fields['remarks'].widget.attrs = {'class':'form-control','rows':'3','cols':'10'}
    
    class Meta:
        model = Case
        exclude = ['modified']
        

class CaseSearchForm(CaseBaseForm):
    
    from_dt   = forms.ChoiceField(required=True,)
    until_dt   = forms.DateField(required=True)
    
    def __init__(self,*args,**kwargs):  
        choices=None
        if 'choices' in kwargs:
            choices = kwargs.pop('choices')   
        super(CaseSearchForm,self).__init__(*args,**kwargs)
        
        self.set_common_form_element()
        self.fields['from_dt'].widget.attrs = {'class':'datepicker', 'data-dateformat':'yy-mm-dd'}
        self.fields['until_dt'].widget.attrs = {'class':'datepicker', 'data-dateformat':'yy-mm-dd'}
        self.fields['client'].required=False
        self.fields['job_category'].required=False
        self.fields['incharge'].required=False
        self.fields['years_experience'].required=False
        self.fields['status'].required=False
        self.fields['job_type'].required=False
        self.fields['level'].widget.attrs={'multiple':'""', 'class':'custom-scroll','size':'3'}
        
    class Meta:
        model = Case
        exclude = ['modified' ]
