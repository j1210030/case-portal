from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from gcase.views import DashboardView

urlpatterns = [
    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard"),

]
