
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.i18n import javascript_catalog

#admin.autodiscover()

urlpatterns = [

    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^admin/jsi18n/$', javascript_catalog, name="django.views.i18n.javascript_catalog"),
    #url(r'^intsft/', include('intsft.urls'))
    url(r'^', include('gcase.urls'))
]
