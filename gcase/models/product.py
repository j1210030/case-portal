# -*- coding: utf-8 -*-
"""
@note: This is the model class for Products
@file: product.py
"""
from .common_models import *
from django.contrib import admin
from datetime import datetime
from django.utils import timezone

log = logging.getLogger(__name__)


"""
Logo file upload function
File will be uploaded in the following directory structure:-
Ex:
/product/yyyy/mm/filename_DD.etx
where:-
 DD is the current date
 filename is the filename of the uploaded file.   
"""
def logo_file_upload(instance,filename):
    log.debug(" Filename is: %s ", filename )
    now = timezone.now()
    extension=''
    tmp = os.path.splitext(filename)
    if len(tmp)==2:
        extension= tmp[1]
    #filename="%s_%s.%s" % (tmp[0],extension,now.strftime("%d"))
    path = "products/%s/%s/%s" % (now.strftime("%Y"),now.strftime("%m"),filename)
    log.debug("Upload path: %s ", path)   
    return path

class Product(models.Model):
    
    name= models.CharField(blank=False,max_length=50,verbose_name='Name')
    active = models.NullBooleanField(verbose_name='Active?')   
    logo_file = models.ImageField(max_length=256, blank=True,upload_to=logo_file_upload,verbose_name="Logo file")
    created  = models.DateTimeField(auto_now_add=True,blank=True,verbose_name='Added on')    
    modified  = models.DateTimeField(auto_now=True,null=True,blank=True,verbose_name='Modified')
    
    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        app_label = 'gcase'
        db_table = 'products'

"""
Partner Admin
"""
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','name','active')
    list_display_links = ('__unicode__',)
    search_fields = ['name']

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
