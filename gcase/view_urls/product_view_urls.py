from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from gcase.views import ProductListView , ProductAddView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    url(r'^products/$', ProductListView.as_view(), name="product"),
    url(r'^product/add$', ProductAddView.as_view(), name="product_add"),
    url(r'^product/edit$', ProductUpdateView.as_view(), name="product_update"),
     url(r'^product/delete$', ProductDeleteView.as_view(), name="product_delete"),
    #url(r'^client/add/$', ClientAddView.as_view(), name="client_add"), 
    #url(r'^client/edit/$', ClientUpdateView.as_view(), name="client_edit"),
    #url(r'^client/ajax_detail/$', ClientDetailView.as_view(), name="client_ajax_detail"),
]
