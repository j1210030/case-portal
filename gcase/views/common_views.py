# -*- coding: utf-8 -*-
"""
This is the common view imports and functions
@File: common_views.py

"""
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import *
from django.http import HttpResponse
#from django.http import JsonResponse
from django.template import RequestContext
from django.conf import settings
from django.db import transaction
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.utils.html import *
from django.utils.encoding import *
from django.utils.functional import *
from django.utils.html import strip_tags
from django.db.models import Q
from django.http import QueryDict
#from django.utils.encoding import smart_unicode, smart_str
from django.utils import translation
from django.utils.html import strip_tags
#from easy_thumbnails.files import get_thumbnailer
from django.contrib import messages
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count,Avg,Max
#from wsgiref.util import FileWrapper
from django.views.generic import CreateView, UpdateView, \
        DeleteView, ListView, DetailView
from django.views.generic.detail import SingleObjectMixin

from django.views.generic import View
from calendar import monthrange
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta  
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.core.validators import validate_ipv46_address, RegexValidator
from django.core.exceptions import PermissionDenied,ValidationError, NON_FIELD_ERRORS
from django.http import HttpResponseForbidden
from gcase.models import Case,Product, Component, GcaseUser

#from urllib.parse import urlencode, quote
#from urlparse import urlparse,parse_qsl
from collections import OrderedDict


"""
http://labix.org/python-dateutil#head-2f49784d6b27bae60cde1cff6a535663cf87497b
"""
from dateutil.relativedelta import *
import os
import random
import errno
import sys
import json
import logging
import uuid
#import magic
import mimetypes
import urllib3
import string

log = logging.getLogger(__name__)

"""
Put Queryset items to log file
"""
def list2log(list_item):
    log.debug("\n--------------------START----------------------------\n")
    for item in list_item:
        log.debug("Item Data: %s ",item)
        log.debug("\n..................................................\n")
    log.debug("\n--------------------END----------------------------\n")
    
def queryset2log(query_set):
    log.debug("\n------------------------------------------------\n")
    for item in query_set:
        log.debug("Item Data: %s ",item.__dict__)
        #log.debug("Field: %s  and value : %s ", field, value)
    log.debug("\n------------------------------------------------\n")
    


class LazyEncoder(json.JSONEncoder):
    """Encodes django's lazy i18n strings.
    Used to serialize translated strings to JSON, because
    simplejson chokes on it otherwise.
    """
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj

"""
Check if a variable is a
correct interger type
"""
def is_integer(variable):
    intval=''
    try:
        intval = int(variable)
        return True
    except:
        return False   
        
def get_random_string(string_length=15):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert uuid format to python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the uuid '-'.
    return random[0:string_length] # Return the random string.


"""
Validate a ユーザーID
Alphanum, dot(.), underscore(_), Hyphen(-)
"""
def validate_username(value=None):
    if value:
        if not re.match('^[a-zA-Z0-9_.]+$',value):
            return False
        return True

        
"""
Add or Subtract Month from current date 
@param month2add:
    supply -2 if you want to get the date 2 month before
    supply 3 if you want to get the date after 3 month.
@return: 
    date in format 'YYYY-MM-DD' format 
"""
def add_month(months2add):
    now = datetime.now()
    result = None; 
    try:
        result =  now+relativedelta(months=months2add)
    except:
        log.exception("Error in date operation ")
    if result is not None:
        return result
    else:
        return None

"""
Add or Subtract Days from  current date.
@praram offset:
    Supply a positive integer if you want to add days to current date
    supply a negative integer if you want to subtract to current date.
@return:

"""
def addjust_days(offset):
    now = datetime.now()
    result = None
    try:
        result = now + relativedelta(days=offset)
    except:
        log.exception()
    return result

def get_sunday(date_str,dtFormat):
    dt = None
    if date_str is None:
        dt = datetime.datetime.now()
    else:
        try:
            if dtFormat is not None and dtFormat == 'YYYY-mm-dd':
                dt = datetime.strptime(date_str,'%Y-%m-%d')
            else:
                if len(date_str) == 17:  
                    dt = datetime.strptime(date_str,'%m/%d/%y %H:%M:%S')
                else:
                    dt = datetime.strptime(date_str,'%m/%d/%Y %H:%M:%S')
            
            sun = dt - timedelta((dt.weekday() + 1) % 7)
            return sun.strftime('%Y-%m-%d')
        except ValueError, ex:
            log.error( ' Date format error: ' + str(ex))
            return None


def get_sunday2(date_str,dtFormat):
    dt = None
    if dtFormat is not None:
        dtFormat = 'YYYY-mm-dd' 
    if date_str is None:
        dt = datetime.now()
	#Set date manually 	
	#dt = datetime(2018, 2, 4, 10, 41, 36, 920370)
	
    else:
        if not isinstance(date_str, datetime):
            dt = datetime.strptime(date_str,'%Y-%m-%d')
            if len(date_str) == 17:  
                dt = datetime.strptime(date_str,'%m/%d/%y %H:%M:%S')
            else:
                dt = datetime.strptime(date_str,'%m/%d/%Y %H:%M:%S')
        else:
            dt = date_str
        
        log.info("Dt is %s " % dt )
    try:
        sun = dt - timedelta((dt.weekday() + 1) % 7)
        return sun.strftime('%Y-%m-%d')
    except ValueError, ex:
        log.error( ' Date format error: ' + str(ex))
        return None

def format_dt2(date_str, time=True):
    try:
        size = 0
        dt = None
        dt_str = None
        if date_str is None:
           return None
        
        size = len(date_str)
        if time:
            if size == 17:
                dt_str = datetime.strptime(date_str,'%m/%d/%y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            else:
                dt_str = datetime.strptime(date_str,'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            return  datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        else:
            if size == 10 or size == 9:
                dt_str = datetime.strptime(date_str,'%m/%d/%Y').strftime('%Y-%m-%d')
            elif size == 8:
                dt_str = datetime.strptime(date_str,'%m/%d/%y').strftime('%Y-%m-%d')            
            return datetime.strptime(dt_str, '%Y-%m-%d')
        
    except ValueError, ex:
        log.error( ' Date format error: ' + str(ex))
        return None
    
def format_dt(date_str, time=True):
    try:
        if time:
            dt_str = datetime.strptime(date_str,'%m/%d/%y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        else:
            dt_str = datetime.strptime(date_str,'%m/%d/%y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        
        return dt
    except ValueError, ex:
        log.error( ' Date format error: ' + str(ex))
        return None

def date_to_str(dt,dtFormat):
    #9/27/2017 15:47:30
    
    return dt.strftime(dtFormat)

def get_month( date_val ):
    if date_val is None:
        return None
    else:
        dt = datetime.strptime(date_val, "%Y-%m-%d")
        return '%s-%s' % (dt.year, dt.month)

def get_date_diff(start,end):
    diff_str=''
    if start is None:
        start = datetime.datetime.today()
    diff = relativedelta.relativedelta(start, end)
    if diff.year > 0:
        diff_str='%dY ' % diff.year
    if diff.month >0:
        diff_str ='%s%sM ' % (diff_str,diff.month)
    if diff.days >0:
        diff_str ='%s%s%D ' % (diff_str,diff.days)
    if diff.hours >0:
        diff_str ='%s%s%H ' % (diff_str,diff.hours)
    return diff_str

def set_month_options():
    return range(1,13)

def set_year_options():
    currentYear = datetime.now().year
    return reversed(range(currentYear -2 , currentYear+1))
    

"""
Set Download Response for a Request.
This will send a file as attachment as HTTP Response.
@param:
    request: the http request
    filepath: Absolute Path of the file to be rendered as response.
@comment:
    At this moment it can't handle non ASCII filename.
@return: 
    The Http Header with attachment.
"""


def get_product_list():
    fields = ('id','name','active','logo_file')
    try:
        return  Product.objects.only(*fields).filter(active=True).order_by('name')
    except Exception, ex:
        log.exception("SQL Error encountered in client list.." + str(ex))
        return None
   
           

def get_days_in_month(year,month):
    return monthrange(year, month)[1]
    
def set_download_response(request,filepath):
    filepath = str(filepath)
    fullpath = os.path.join(settings.UPLOAD_PATH , filepath)
    file_name = os.path.basename(filepath)
    fp = open(fullpath, 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    type, encoding = mimetypes.guess_type(fullpath)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(fullpath).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % file_name.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(file_name.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response
