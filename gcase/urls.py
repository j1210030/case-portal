from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from gcase import views

urlpatterns = [
    url(r'^', include('gcase.view_urls.partner_view_urls')),
    url(r'^', include('gcase.view_urls.product_view_urls')),
    url(r'^', include('gcase.view_urls.component_view_urls')),
    url(r'^', include('gcase.view_urls.dashboard_view_urls')),
    url(r'^', include('gcase.view_urls.case_view_urls')),
    url(r'^', include('gcase.view_urls.report_view_urls')),
    url(r'^', include('gcase.view_urls.review_request_view_urls')),
    url(r'^', include('gcase.view_urls.user_view_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)