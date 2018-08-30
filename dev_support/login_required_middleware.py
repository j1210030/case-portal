# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile

from django.core.urlresolvers import reverse
from django.utils.deprecation import MiddlewareMixin
import logging

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

#def get_login_url():
    #return reverse(settings.LOGIN_URL)


def get_exempts():
    exempts = [compile(settings.LOGIN_URL.lstrip('/'))]
    if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
        exempts += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]
    return exempts

log = logging.getLogger(__name__)
class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
      
        log.info('User is %s ' % request.user )
        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)