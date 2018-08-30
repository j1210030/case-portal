from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from gcase.views import CaseListView , CaseAddView,CaseUpdateView, GetWeekByDateView, Csv2DbView,\
                            CaseIdCheck,CasePartnerSetView,CaseSetSoDateView,CaseSetBuganizerView

urlpatterns = [
    url(r'^cases/$', CaseListView.as_view(), name="case_list"),
    url(r'^case/add$', CaseAddView.as_view(), name="case_add"),
    url(r'^case/edit$', CaseUpdateView.as_view(), name="case_edit"),
    url(r'^case/set_partner$', CasePartnerSetView.as_view(), name="case_partner_set"),
    url(r'^case/set_so_date$', CaseSetSoDateView.as_view(), name="case_so_date_set"),
    url(r'^case/set_buganizer$', CaseSetBuganizerView.as_view(), name="case_buganizer_set"),
    url(r'^case/getweek$', GetWeekByDateView.as_view(), name="case_getweek"),
    url(r'^case/list$', CaseListView.as_view(), name="case_add"),
    url(r'^csv2db/insert$', Csv2DbView.as_view(), name="csv2_db"),
    url(r'^case/check_id$', CaseIdCheck.as_view(), name="case_id_check")
    
    
    #url(r'^partner/edit$', PartnerUpdateView.as_view(), name="partner_update"),
    #url(r'^client/add/$', ClientAddView.as_view(), name="client_add"), 
    #url(r'^client/edit/$', ClientUpdateView.as_view(), name="client_edit"),
    #url(r'^client/ajax_detail/$', ClientDetailView.as_view(), name="client_ajax_detail"),
]
