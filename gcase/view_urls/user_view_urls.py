from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from gcase.views import UserListView , UserRegisterView,UserUpdateView,UsernameCheck,\
                        UserLoginView,UserLogoutView,HomeView

urlpatterns = [
    url(r'^user/$', UserListView.as_view(), name="user_list"),
    url(r'^user/register$', UserRegisterView.as_view(), name="user_register"),
     url(r'^user/edit$', UserUpdateView.as_view(), name="user_edit"),
    url(r'^user/check_username', UsernameCheck.as_view(), name="check_username"),
    url(r'^user/login', UserLoginView.as_view(), name="user_login"),
    url(r'^user/logout', UserLogoutView.as_view(), name="user_logout"),
    url(r'^home/$', HomeView.as_view(), name="home"),
    url(r'^$', HomeView.as_view(), name="home")
]
