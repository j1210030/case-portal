# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from gcase.models import Case,Product, Component, GcaseUser, gcase_user
from django.utils.functional import lazy
from gcase.forms import CaseAddEditForm
from django.db import DatabaseError
from itertools import chain
from datetime import timedelta
from django.shortcuts import get_object_or_404
import csv
import gcase


log = logging.getLogger(__name__)


class Csv2DbView(View):
    context_dict = {}
    template_name='gcase/case/tmp.html'
    form_class = CaseAddEditForm
    def get(self, request):
        csvFile = '/Users/suhasg/Devel/python.proj/dev_support/csv/Status1108.csv'
        fields = ('id','name','product_id')
        component_list = Component.objects.only(*fields).filter(active=True).order_by('name')
        case_list = []
        with open(csvFile) as file:
            reader = csv.reader(file)
            loop = 0;
            log.info('---CSV Reading-------')
            for row in reader:
                data = {}
                #data['no'] = row[0]
                
                #log.info('Sl: %s id : %s ' % (row[0], row[1]) )
                if int(row[0]) < 1415: #9-6881000019650
                    continue
                
                log.info(row)
                log.info('-----------------------------------------------------------------------------------------')
                
                if row[1] is None or row[1] == '':
                    break
                if int(row[0]) > 1416:
                    break
                 
                data = self.set_case_date(row, component_list)
                is_exist = True
                db_case = None
                try:
                    db_case = Case.objects.get(id=data['id'])
                except Case.DoesNotExist:
                     is_exist = False
                     pass
                
                if is_exist:
                    #log.info(db_case)
                    log.info(' Case with id: %s already exists.' % db_case.id)
                    self.update_case(db_case, data)
                else:    
                    #
                    self.add_case(data)
                    #log.info("------------------------------------------------------------------Loop is %s" % loop)
                    loop = loop +1
                    case_list.append(data)
               
            
        self.context_dict['case_list'] = case_list
                #log.debug(data)
        
                
        return render(request, self.template_name,self.context_dict)
    
    
    def set_case_date(self, row,component_list):
         data = {}
         data['id'] = row[1]
         if row[9] == '01/18/17 8:21:16':
            row[9] = '01/18/17 08:21:16'
                    
         dt = format_dt2(row[9], True) 
         data['incoming_date'] =  dt 
         data['week'] = get_sunday(row[9], None)
                
         if row[3] == '' or row[3] is None:
            data['subject'] = 'NA'
         else:
            data['subject'] = row[3]            
         
         product_id = None        
         if row[4] == 'Android' or row[4] == 'AndroidTV' or row[4] == 'Games' or row[4] ==  'Maps' or row[4] == 'OAuth':
            product_id =1
         elif row[4] == 'Firebase':
            product_id = 2
         elif row[4] == 'Chrome' or row[4] == 'Chromecast':
            product_id = 3;
         elif row[4].lower() == 'play store' or row[4] == 'Google Apps' or row[4] == 'Google Plus' or row[4] == 'Youtube':
            product_id = 3;
         else:
            product_id =1
                
         data['product'] = product_id
                
                #componentTxt = row[5]
         comp_id = None
         for item in component_list:
            if item.name.lower() == row[5].lower() and item.product_id == product_id:
                comp_id = item.id
                break
            if comp_id is None and row[5] == 'Firebase Analytics':
                comp_id=14
                    
         data['component'] = comp_id
         language = 'jp'       
         if  row[7] == 'Chinese':
            language = 'zh'
         elif row[7] == 'Korean':
            language = 'ko'
         elif row[7] == 'en':
            language = 'English'
                        
         data['language'] =  language
                        
         user = row[10].lower().strip()
         #user.encode('ascii', 'ignore')
         log.info('User: %s , len: %d ' % (user, len(user) ))
         
         if user == 'yuriko\xe2\x80\x8b':
             user = 'yuriko'
                  
         gcase_user_id = None
                
         if user == 'suhas':
            gcase_user_id = 1
         elif user == 'kei':
            gcase_user_id = 2
         elif user == 'tianhui':
             gcase_user_id = 3
         elif user == 'yuriko':
            gcase_user_id = 5
         elif user == 'minghao':
            gcase_user_id = 6
         elif user == 'y.lee':
            gcase_user_id = 7
         elif user == 'k.kim':
            gcase_user_id = 8
         elif user == 'taixi':
             gcase_user_id = 9
         elif user == 'wondu':
             gcase_user_id = 10
         elif user == 'nozomi':
             gcase_user_id = 11
         elif user == 'hyungyo':
            gcase_user_id = 12    
         elif user == 'maki':
            gcase_user_id = 13
         elif user == 'moonseok':
            gcase_user_id = 14
                    
         data['gcase_user'] = gcase_user_id        
         if data['id'] == '0-438800001801' and gcase_user_id is None:
            data['gcase_user_id'] = 5
                #data['gcase_user'] = user
         status = 'solution_offered'
                
         if row[14].lower() == 'solution offered':
            status = 'solution_offered'
         elif row[14].lower() == 'need info':
            status = 'needinfo'
         elif row[14].lower() == 'in consult':
            status = 'inconsult'
         elif row[14].lower() is not None or row[14].lower() == '':
            status = row[14].lower()
                    
         data['status'] = status
         partnerFlag = row[15]
               
         data['difficulty_level'] = 'moderate'
         partner_id = None
         if partnerFlag == '○':
             if data['language'] == 'jp':
                partner_id = 157
             elif data['language'] == 'ko':
                partner_id = 159
             elif data['language'] == 'zh':
                partner_id = 158
                
         data['partner'] = partner_id         
         data['sub_product'] = row[6].lower()
         data['remarks'] = row[19]
         
         return data
                
    def add_case(self,data):
        form = self.form_class(data or None)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.save()
            except Exception, ex:
                log.exception("SQL Error encountered in client list.." + str(ex))
                
        else:
            log.error("Case Form validation has failed:(Add)-----");
            for error in form.errors.items():
                log.error("Error: %s , %s ", error , data['id'])
        return data                
                        
                        
    def update_case(self,db_case, csv_data):
        update_flag = False
        try:
            if db_case.gcase_user.id != csv_data['gcase_user']:
                db_case.gcase_user_id =  csv_data['gcase_user']
                update_flag = True
            if db_case.status != csv_data['status']:
                db_case.status = csv_data['status']
                update_flag = True
        
            if update_flag:
                log.info ( ' Going to update: %s ' % (csv_data['id']) ) 
                db_case.save()
            else:
                log.info('-- No need update -----')
        except Exception, ex:
            log.exception("SQL Error encountered in client list.." + str(ex))
            
        except DatabaseError, dbEx:
            log.error("SQL error encountered: " + str(dbEx))
    
        
        

