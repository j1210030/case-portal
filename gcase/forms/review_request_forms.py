# -*- coding: utf-8 -*-

"""
@Note: This is the form class for Component
@File: product_forms.py
"""
from .common_forms import *
from gcase.models import Case,ReviewRequest

from django.utils.translation import ugettext_lazy as _

log = logging.getLogger(__name__)

"""
Common Base Form will be inherited by
others
"""

class ReviewRequestBaseForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        super(ReviewRequestBaseForm,self).__init__(*args,**kwargs)
        
    def set_form_element(self):
        self.fields['email_title'].widget.attrs = {'class':'form-control'}
        self.fields['status'].widget.attrs = {'class':'form-control'}
        self.fields['requested_on'].widget.attrs = {'class':'form-control','placeholder':'Ex:08/24/2017'}
        self.fields['feedback_received_on'].widget.attrs = {'class':'form-control','placeholder':'Ex:08/24/2017'}
        self.fields['status'].choices = settings.CASE_REVIEW_STATUS_CHOICES
        self.fields['agent_remarks'].widget.attrs = {'class':'form-control','rows':'3','cols':'10'}
        self.fields['da_feedback'].widget.attrs = {'class':'form-control','rows':'3','cols':'10'}
        

"""
Partner Add/Edit Form 
"""        
class ReviewRequestAddEditForm(ReviewRequestBaseForm):
    
    def __init__(self,*args,**kwargs):
        super(ReviewRequestBaseForm,self).__init__(*args,**kwargs)
        self.set_form_element()
    class Meta:
        model = ReviewRequest
        exclude = ['modified','product']
        
