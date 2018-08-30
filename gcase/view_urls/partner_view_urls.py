from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from gcase.views import PartnerListView , PartnerAddView, PartnerUpdateView,PartnerListJsonView

urlpatterns = [
    url(r'^partner/$', PartnerListView.as_view(), name="partner"),
    url(r'^partner/add$', PartnerAddView.as_view(), name="partner_add"),
    url(r'^partner/edit$', PartnerUpdateView.as_view(), name="partner_update"),
    url(r'^partner/get_json$', PartnerListJsonView.as_view(), name="partner_json"),
    #url(r'^client/add/$', ClientAddView.as_view(), name="client_add"), 
    #url(r'^client/edit/$', ClientUpdateView.as_view(), name="client_edit"),
    #url(r'^client/ajax_detail/$', ClientDetailView.as_view(), name="client_ajax_detail"),
]
