# -*- coding: utf-8 -*-
# - Individual report 
from django.core.management.base import BaseCommand, CommandError
from gcase.models import Case, IndividualReport,GcaseUser, individual_report

#from gcase.common_views import *
from django.conf import settings
#from views.common_views import *
from gcase.views.common_views import *   #common_views import *
#from Carbon.Events import app2Mask
import math
from datetime import timedelta

log = logging.getLogger(__name__)


class Command(BaseCommand):
 
    def handle(self, *args, **options):
    
        incoming = None
        incoming_partner = None
        so = None
        so_partner = None
      
            
        try:
            kwargs = {}
            args = ()
           
            sunday = get_sunday2(None, None);
            
            log.info('Sunday: %s ' % sunday)
            dt = datetime.strptime(sunday,'%Y-%m-%d') 
            dt = dt + relativedelta(days=-7)
            log.info(dt)
            #dt = format_dt2(date_str,False)
            status_filter = ~Q(status__in=['duplicate'])
             
            # -- Incoming ---- 
            incoming_data = Case.objects.filter(~Q(status__in=['duplicate','routed','forwarded']),week=dt).\
                                values('gcase_user_id').annotate(case_count=Count('*')).order_by('gcase_user_id')
                                
            # --- Incoming partner ----
            incoming_partner_data = Case.objects.filter(~Q(status__in=['duplicate','routed','forwarded']),week=dt,partner_id__isnull=False).\
                                values('gcase_user_id').annotate(case_count=Count('*')).order_by('gcase_user_id')
            
            # --- SO dara ----#
            so_data = Case.objects.filter(Q(status__in=['solution_offered']),so_week=dt).\
                                values('gcase_user_id').annotate(case_count=Count('*')).order_by('gcase_user_id')
                                
            so_partner_data = Case.objects.filter(Q(status__in=['solution_offered']),so_week=dt,partner_id__isnull=False).\
                                values('gcase_user_id').annotate(case_count=Count('*')).order_by('gcase_user_id')
            
            
            log.info('---------------------------------')
            log.info(incoming_data)
            log.info('---------------------------------')
            log.info(so_data)
            log.info('---------------------------------')
             
            fields = ('id','user.first_name', 'last_name','profile_pict')
            users = GcaseUser.objects.values_list('id','user__first_name', 'user__last_name','profile_pict').filter(user__is_active=True,case_handler=True).order_by('user__first_name')
            for user in users:
                guser_id = int(user[0])
                if guser_id == 2 or guser_id == 3 or guser_id == 5 or guser_id == 6 or guser_id == 7 or guser_id == 8 or guser_id == 9 or guser_id == 10 or guser_id == 17 or guser_id == 18 or guser_id == 25:
                    self.create_data(guser_id,dt,incoming_data,incoming_partner_data,so_data,so_partner_data) 
                    
        except Exception, ex:
             log.exception("SQL Error Encountered in jd search. " + str(ex))
        
    def create_data(self,user_id,week,incoming_data, incoming_partner_data, so_data, so_partner_data):
            
            incoming_count = 0
            incoming_count_partner = 0
            so_count = 0;
            so_count_partner = 0
            pw_backlog =  self.previous_week_backlog(week, user_id)
            
            individual_report = {}
           
            
            if incoming_data is not None and len(incoming_data) > 0:
                for item in incoming_data:
                    if item['gcase_user_id'] == user_id:
                        incoming_count = item['case_count']
                        break
                    
            if incoming_partner_data is not None and len(incoming_partner_data) > 0:
                for item in incoming_partner_data:
                    if item['gcase_user_id'] == user_id:
                        incoming_count_partner = item['case_count']
                        break
            
            if so_data is not None and len(so_data) > 0:
                for item in so_data:
                    if item['gcase_user_id'] == user_id:
                        so_count = item['case_count']
                        break
                    
            if so_partner_data is not None and len(so_partner_data) > 0:
                for item in so_partner_data:
                    if item['gcase_user_id'] == user_id:
                        so_count_partner = item['case_count']
                        break
            
            individual_report['gcase_user_id'] = user_id
            individual_report['week'] = week
            individual_report['pw_backlog'] = pw_backlog
            individual_report['incoming'] = incoming_count
            individual_report['incoming_partner'] = incoming_count_partner
            individual_report['so'] = so_count
            individual_report['so_partner'] = so_count_partner
            
            try:
               IndividualReport.objects.create(**individual_report)
            except Exception, ex:
                log.exception("SQL Error encountered in client list.." + str(ex))
            
    def previous_week_backlog(self,current_week, user_id):
        prev_week = current_week + relativedelta(days=-7)
        pw_backlog = 0
        try:
            data = IndividualReport.objects.get(week=prev_week, gcase_user_id=user_id)
            if data:
                pw_backlog =  ( data.pw_backlog + data.incoming) - data.so
            log.info('Data is %s ' %  pw_backlog)
        
        except Exception, ex:
            log.exception("SQL Error encountered in client list.." + str(ex))
        
        return  pw_backlog