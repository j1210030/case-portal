# -*- coding: utf-8 -*-
"""
This is the class based view for Partner.
@File: client_views.py 
"""
from .common_views import *
from gcase.models import Partner
from gcase.forms import UserAddEditForm,UserLoginForm
from django.utils.functional import lazy
from django.db import DatabaseError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from difflib import context_diff

log = logging.getLogger(__name__)



class UserLoginView(View):
    template_name='gcase/user/login.html'
    context_dict = {}
    form_class = UserLoginForm
    
    def get(self, request):
        if request.user.is_authenticated():
            log.debug("User is already logged in ");
            return HttpResponseRedirect("/")
        
        return render(request, self.template_name,self.context_dict)
    
    def post(self, request):
       
        post=request.POST.copy()
        context_dict = {}
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            
            user = authenticate(request, username=post['username'], password=post['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/")    
            messages.error(request, 'Incorrect login credential , please provide correct input')
        
        else:
            log.error("LoginForm validation has failed for profile-----");
            for error in form.errors.items():
                log.error("Error: %s ", error)
            messages.error(request, 'Please provide input correctly')
        

        return render(request, self.template_name, self.context_dict)  


class UserLogoutView(View):   
    
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/user/login/")
    
    
class UserListView(View):
    template_name='gcase/user/list.html'
    context_dict = {}
    
    context_dict['view_name'] = 'user'
    context_dict['action'] = 'list'

    def get(self, request):
        user_list = []
        try:
            
            user_list = GcaseUser.objects.values_list('id','case_handler','user__first_name','user__date_joined','date_released' ,'user__last_name','user__is_active','user__username','gender').\
                            order_by('user__first_name')
            
            user_list = GcaseUser.objects.select_related('user').order_by('-user__is_active','user__first_name')
            self.context_dict['user_list'] = user_list
            log.info(user_list)
            
        except Exception, ex:
            log.exception("Sql error encountered.." +  str(ex))
            messages.warning(self.request,'Internal server error has encountered!!')
        return render(request, self.template_name,self.context_dict)
        

class UserRegisterView(View):                     
    template_name = 'gcase/user/input.html'
    form_class = UserAddEditForm
    error = False
    context_dict = {}
    
    def get(self,request):
        self.context_dict = {}
        form = self.form_class(initial={'is_active': True,'case_handler':True,'is_superuser': False,'gender':'M'})
        self.context_dict['form'] = form
        self.context_dict['view_name'] = 'user'
        self.context_dict['action'] = 'list'
        return render(request, self.template_name,self.context_dict)

    @transaction.atomic()
    def post(self,request):
        post=request.POST.copy()
        context_dict = {}
        for key, value in post.iteritems():
            log.debug("key is %s and value is : %s ",key,value)
            
        form = self.form_class(request.POST or None, request.FILES)
        if form.is_valid():
            try:
                
                user = User.objects.create_user(post['username'], 'lennon@thebeatles.com', post['password'])
                user.first_name = post['first_name']
                user.last_name = post['last_name']
                user.is_active = post['is_active']
                user.is_staff = 1
                if post['is_superuser']:
                    user.is_superuser = 1
                user.date_joined = format_dt2(post['joined_on'], False)
                if post['released_on']:
                    user.date_released = format_dt2(post['released_on'], False)
                    
                user.save()
                
                gcase_user = {}
                gcase_user['user_id'] = user.id
                gcase_user['gender'] = post['gender']
                gcase_user['case_handler'] = post['case_handler']
                
                GcaseUser.objects.create(**gcase_user)
                
                messages.success(request, 'New user is created successfully.')
            except:
                log.exception("Error encountered: ")
                messages.error(request, 'Server error, failed to add partner')
            return redirect('/user/')
        else:
            log.error("Partner Form validation has failed:(Add)-----");
            for error in form.errors.items():
                log.error("Error: %s ", error)
            messages.error(request, 'Error in input, please try again')
        self.context_dict['form'] = form
        
        self.context_dict['view_name'] = 'user'
        self.context_dict['action'] = 'register'
        
        return render(request,self.template_name,self.context_dict)

class UserUpdateView(View):
    template_name = 'gcase/user/input.html'
    form_class = UserAddEditForm
    error = False
    context_dict = {}
     
    def get(self,request):
        data=request.GET.copy()
        self.context_dict = {}
        
        gcase_user = None
        log.info(' id %s ' % data['id'])
        try:
           gcase_user = GcaseUser.objects.get(pk=data['id'])
            
        except GcaseUser.DoesNotExist, dEx:
            log.error("No user record for id: %s ", data['id'] )
            messages.warning(request,'User record could not be found.')
            return redirect('/user/')
        except Exception, ex:
            messages.error(request,'Server error has encountered.')
            log.exception("Sql error encountered.." +  str(ex))
        
        user_dict = {}
        user_dict['first_name'] = gcase_user.user.first_name
        user_dict['last_name'] = gcase_user.user.last_name
        user_dict['gender'] = gcase_user.gender
        user_dict['username'] = gcase_user.user.username
        user_dict['joined_on'] = date_to_str(gcase_user.user.date_joined, '%m/%d/%Y')
        user_dict['is_active'] = gcase_user.user.is_active
        user_dict['case_handler'] = gcase_user.case_handler
        user_dict['is_superuser'] = gcase_user.user.is_superuser 
         
        if gcase_user.date_released is not None:
            user_dict['date_released'] = date_to_str(gcase_user.date_released.date_joined, '%m/%d/%Y')
        
        log.info(user_dict)
         
        self.context_dict['user'] = gcase_user
        form = self.form_class(instance=gcase_user,initial=user_dict)
        #log.info(form)
        
        self.context_dict['form'] = form
        self.context_dict['action'] = 'edit'
        self.context_dict['id'] = data['id']
       
        return render(request, self.template_name,self.context_dict)

    @transaction.atomic()
    def post(self,request): 
        post=request.POST.copy()    
        for key, value in post.items():
            log.debug("key is %s and value is : %s ",key,value)
       
        user = None
        try:
           user = GcaseUser.objects.get(pk=post['id'])
        except Exception, ex:
            log.exception("Sql error encountered.." +  str(ex))
        if not user:
            log.error("No partner record for id: %s ", self.pid )
            messages.warning(request,'User record could not be found')
            return redirect('/user/')
        
        form = self.form_class(post,request.FILES,instance=user)  
        if form.is_valid():
            try: 
                instance = form.save(commit=False)
                instance.save()
                messages.success(request,'Record is updated successfully.')
            except Exception, ex:
                log.exception("Error encountered: " + str(ex))
                messages.error(self.request, 'Error has encountered, failed to update record')

            return redirect('/user/')   
        else:
            log.error("user Form validation has failed(Edit) -----");
            for error in form.errors.items():
                log.error("Error: %s ", error)
            messages.error(request, 'Error in input, please try again')
        self.context['form'] = form 
        
        return render(request, self.template_name, self.context)
    
      
class UsernameCheck(View):
    error=False;
    json_response = {}
    context_dict = {}
    
    def get(self,request):     
        self.context_dict = {}
        data=request.GET.copy()
        log.info(data)
        log.debug(' username to check %s: ' % data['username'])
        
        if 'username' not in data or 'uid' not in data:
            log.error("invalid request..")   
            self.error=True
            self.json_response['status'] = 'ERROR'
            self.json_response['message'] = 'Invalid request.'
        
            
        if not self.error:
            user = None
            try:
               # user = GcaseUser.objects.get(user__username=data['username'])
                if data['uid'] is not None and len(data['uid'])>0:
                   user = User.objects.exclude(pk=data['uid']).get(username=data['username'])
                else:
                    user = User.objects.get(username=data['username'])
                    
            except User.DoesNotExist, dEx:
                 log.error("User with username: [ %s ] does not exists. ", data['username'] )
                 self.json_response['status'] = 'OK'
            except Exception, ex:
                log.exception("Sql error encountered.." +  str(ex))
            if user:
                log.error("Case with id: [ %s ] already exists. ", data['username'] )
                self.json_response['status'] = 'EXISTS'     
               
        if request.is_ajax():
            json_data = None
            try:
                json_data = json.dumps(self.json_response,ensure_ascii="False")
            except:
                log.exception("Json Error: ")
                pass
            return HttpResponse(json_data, content_type='application/json,encoding=utf-8')
