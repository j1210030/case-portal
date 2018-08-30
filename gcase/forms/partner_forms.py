# -*- coding: utf-8 -*-

"""
@Note: This is the form class for Partner
@File: partner_forms.py
"""
from .common_forms import *
from gcase.models import Partner

from django.utils.translation import ugettext_lazy as _

log = logging.getLogger(__name__)

"""
Common Base Form will be inherited by
others
"""

class PartnerBaseForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        super(PartnerBaseForm,self).__init__(*args,**kwargs)
        
    def set_form_element(self):
        self.fields['is_active'].choices = settings.PARTNER_STATUS_CHOICES
        self.fields['geo_location'].choices = settings.GEO_LOCATION_CHOICES

"""
Partner Add/Edit Form 
"""        
class PartnerAddEditForm(PartnerBaseForm):
    def __init__(self,*args,**kwargs):
        super(PartnerAddEditForm,self).__init__(*args,**kwargs)
        self.set_form_element()
        self.fields['name_english'].widget.attrs = {'class': 'form-control col-md-7 col-xs-12','data-parsley-maxlength':'42','data-parsley-trigger':'change','required':'required'}
        self.fields['name_locale'].widget.attrs = {'class': 'form-control  col-md-7 col-xs-12','required':'required'}
        self.fields['company_url'].widget.attrs = {'class': 'form-control col-md-7 col-xs-12'}
        self.fields['created'].widget.attrs = {'class': 'form-control has-feedback-left'}
        self.fields['is_active'] =  forms.ChoiceField(choices=settings.PARTNER_STATUS_CHOICES, widget=forms.RadioSelect(),initial=False)
        self.fields['is_active'].widget.attrs ={'class':'flat'}
        self.fields['remarks'].widget.attrs = {'rows':'3','cols':'10'}
        
    class Meta:
        model = Partner
        exclude = ['modified']
        
