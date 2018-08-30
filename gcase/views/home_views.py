# -*- coding: utf-8 -*-

from common_views import *
from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as _


log = logging.getLogger(__name__)



class HomeView(View):                     
    template_name = 'gcase/common/home.html'
    error = False
    context_dict = {}
    
    def get(self,request):
        self.context_dict['view_name'] = 'home'
        return render(request, self.template_name,self.context_dict)
    