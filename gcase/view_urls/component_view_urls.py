from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from gcase.views import ComponentListView , ComponentAddView, ComponentUpdateView, ComponentDeleteView, ComponentCheckNameView, GetByProductView

urlpatterns = [
    url(r'^components/$', ComponentListView.as_view(), name="component"),
    url(r'^component/add$', ComponentAddView.as_view(), name="component_add"),
    url(r'^component/edit$', ComponentUpdateView.as_view(), name="component_update"),
    url(r'^component/ajax_check_name$', ComponentCheckNameView.as_view(), name="component_check_name"),
    url(r'^component/delete$', ComponentDeleteView.as_view(), name="component_delete"),
    url(r'^component/getbyproduct$', GetByProductView.as_view(), name="component_by_product"),
   
    #url(r'^client/add/$', ClientAddView.as_view(), name="client_add"), 
    #url(r'^client/edit/$', ClientUpdateView.as_view(), name="client_edit"),
    #url(r'^client/ajax_detail/$', ClientDetailView.as_view(), name="client_ajax_detail"),
]