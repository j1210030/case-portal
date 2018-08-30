# -*- coding: utf-8 -*-
"""
This is the class based view for Dashboard view
@File: dashboard_views.py 
"""
from .common_views import *
from gcase.models import Case, GcaseUser
from django.utils.functional import lazy
from django.db.models import Sum, Avg, Max, Min
from itertools import chain
from Tkconstants import CURRENT

log = logging.getLogger(__name__)

"""

@request pattern:
/dashboard/

"""
class DashboardView(View):
    context_dict = {}
    template_name='gcase/dashboard/index.html'
    def get(self, request):

        this_week = get_sunday2(None,None)
        
        self.context_dict['overall'] = self.get_backlog(False)
        self.context_dict['partner'] = self.get_backlog(True)
        
        individual_list = self.get_individual(this_week)
        
        log.info(individual_list)
        
        self.context_dict['individual_list'] = individual_list
        
        
        self.context_dict['incoming'] = self.get_current_week(this_week,False,False)
        self.context_dict['incoming_partner'] = self.get_current_week(this_week,True,False)
        self.context_dict['so'] = self.get_current_week(this_week,False,True)
        self.context_dict['so_partner'] = self.get_current_week(this_week,True,True)
        
        #self.context_dict['period'] = '( %02s/%02s ~ %02s/%02s )' % ( dt.month , dt.day, from_dt.month, from_dt.day )
        dt = datetime.strptime(this_week,'%Y-%m-%d')
        self.context_dict['period'] = '( %02s/%02s ~  )' % ( dt.month , dt.day )
        
        return render(request, self.template_name,self.context_dict)
    
    def get_backlog(self, partner_only):
        
        total_info = {}
        android_info = {}
        firebase_info = {}
        
        partner_filter = Q()
        status_filter = ~Q(status__in=['solution_offered','duplicate','routed'])
        if partner_only:
             partner_filter = Q(partner__isnull=False)
             
        #select status, count(*) from cases where status NOT IN ( 'solution_offered' ,'routed', 'duplicate') group by status 
        status_dict = dict(settings.CASE_STATUS_CHOICES)
        total_list = None
        android_list = None
        firebase_list = None
        
        try:
            total_list = Case.objects.filter(status_filter,partner_filter).values('status').annotate(case_count=Count('*')).order_by('status')
            android_list = Case.objects.filter(status_filter,partner_filter,product_id=1).values('status').annotate(case_count=Count('*')).order_by('status')
            firebase_list = Case.objects.filter(status_filter,partner_filter,product_id=2).values('status').annotate(case_count=Count('*')).order_by('status')
        
        except Exception, ex:
            log.exception("SQL Error encountered in client list.." + str(ex))
            return None
    
        total_backlog = 0;
        total_android_backlog = 0;
        total_firebase_backlog = 0;
        
        for key, value in status_dict.iteritems():    
            
            count = 0
            android_count = 0
            firebase_count= 0
            
            if len(total_list) >0:
                for item in total_list:
                    if item['status'] == key:
                        count = item['case_count']
                        if key != 'routed' and key != 'forwarded' and key !='duplicate':
                            total_backlog = total_backlog + count
                        break
            total_info[key] = count
            
            if len(android_list) >0:
                for item in android_list:
                    if item['status'] == key:
                        android_count = item['case_count']
                        if key != 'routed' and key != 'forwarded' and key !='duplicate':
                            total_android_backlog = total_android_backlog + android_count
                        break
            android_info[key] = android_count
            
            if len(firebase_list) >0:
                for item in firebase_list:
                    if item['status'] == key:
                        firebase_count = item['case_count']
                        if key != 'routed' and key != 'forwarded' and key !='duplicate':
                            total_firebase_backlog = total_firebase_backlog + firebase_count
                        break
            firebase_info[key] = firebase_count
            
            
        data= {}    
        data['total'] = total_info
        data['android'] = android_info
        data['firebase'] = firebase_info
        
        log.info(total_info)
        log.info('Total Backlog: %d' % total_backlog)
        
        data['total_backlog'] = total_backlog
        data['android_backlog'] = total_android_backlog
        data['firebase_backlog'] = total_firebase_backlog
        
         
        return data
        
    def get_individual(self, current_week):
        #select gcase_user_id, status,count(status) from cases where status not in ('solution_offered','routed','forwarded','duplicate') group by status, gcase_user_id order by gcase_user_id ASC, status asc 
        individual_list = []
        individual_data = Case.objects.filter(~Q(status__in=['solution_offered','duplicate','routed','forwarded'])).\
                                values('gcase_user_id','status').annotate(case_count=Count('*')).order_by('gcase_user_id','status')
        log.info(individual_data)
        
        individual_so = Case.objects.filter(status='solution_offered',so_week=current_week).\
                                values('gcase_user_id').annotate(case_count=Count('*')).order_by('gcase_user_id')
        
        log.info(individual_so)
        
        users = GcaseUser.objects.values_list('id','user__first_name', 'user__last_name','profile_pict').filter(user__is_active=True,case_handler=True).order_by('user__first_name')
       
        log.debug(" Data %s " % users )
      
        for user in users:
            #log.debug(" Data %s " % item[1]  )
            data={}
            data['id'] = user[0] 
            data['name'] = "%s %s" % (user[1], user[2])
            assigned = 0  
            needinfo = 0
            inconsult = 0
            blocked = 0
            review_requested = 0
            forwarded = 0
            total_backlog = 0
            so_count = 0
            
            if len(individual_data) >0:
                for item in individual_data:
                    
                    if item['gcase_user_id'] == user[0]:
                        
                        if item['status'] == 'assigned':
                            assigned = item['case_count']
                        
                        elif item['status'] == 'needinfo':
                            needinfo = item['case_count']
                        
                        elif item['status'] == 'inconsult':
                            inconsult = item['case_count']
                            
                        elif item['status'] == 'blocked':
                            blocked = item['case_count']
                            
                        elif item['status'] == 'review_requested':
                            review_requested = item['case_count']
                        
                        elif item['status'] == 'forwarded':
                            forwarded = item['case_count']   
                        
                        if item['status'] != 'forwarded':
                            total_backlog = total_backlog + item['case_count']
            
            if len(individual_so) >0:
                for so in individual_so:
                    if so['gcase_user_id'] == user[0]:
                        so_count = so['case_count'] 
                        break
                    
            data['assigned'] = assigned  
            data['needinfo'] = needinfo
            data['inconsult'] = inconsult
            data['blocked'] = blocked
            data['review_requested'] = review_requested
            data['forwarded'] = forwarded
            data['backlog'] = total_backlog
            data['solution_offered'] = so_count
            
            individual_list.append(data)
        
        return individual_list

    def get_current_week(self, this_week,partner_only, so_count):
        current_week ={}
        
        #log.info("This week %s " %  this_week)
        partner_filter = Q()
        
        status_filter = ~Q(status__in=['duplicate','routed'])
        try:
            kwargs = {}
            args = ()
            
            if partner_only == True:
                partner_filter = Q(partner__isnull=False)
            
            if so_count == True:
                kwargs['status'] = 'solution_offered'
                kwargs['so_week'] = this_week
            else:
                kwargs['week'] = this_week
                
            total = 0
            android = 0
            firebase = 0
            if so_count == True:
                total = Case.objects.filter(partner_filter,*args, **kwargs).count()
                kwargs['product_id'] =1
                android = Case.objects.filter(partner_filter,*args, **kwargs).count()
                kwargs['product_id'] =2
                firebase = Case.objects.filter(partner_filter,*args, **kwargs).count()
            
            else:
                total = Case.objects.filter(status_filter,partner_filter,week= this_week).count()
                android = Case.objects.filter(status_filter,partner_filter,product_id=1,*args, **kwargs).count()
                firebase = Case.objects.filter(status_filter,partner_filter,product_id=2,*args, **kwargs).count()
            
            current_week['total'] = total
            current_week['android'] = android
            current_week['firebase'] = firebase
            
            return current_week
        
        except Exception, ex:
            log.exception("SQL Error encountered in client list.." + str(ex))
            return None