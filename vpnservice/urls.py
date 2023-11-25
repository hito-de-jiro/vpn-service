from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from .forms import LoginForm
from .views import (
    home,
    RegisterView,

    UserSiteListView,
    # UserSiteCreateView,
    SiteDeleteView, CustomLoginView,
)

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    path('user-name-home/', UserSiteListView.as_view(), name='home'),
    # path('add/', UserSiteCreateView.as_view(), name='add_site'),
    path('user-name-home/<int:pk>/delete', SiteDeleteView.as_view(), name='delete_site'),
    # re_path(r'(?P<user_path>/.*)', proxy_url, name='user_path'),
]
