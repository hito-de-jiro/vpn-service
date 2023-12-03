from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from .forms import LoginForm
from .views import (
    home,
    RegisterView,
    CustomLoginView,
    profile,

    user_site_list,
    create_user_site,
    site_delete,
    site_info_list,

    proxy_url,
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('profile/', profile, name='users-profile'),

    path('home/', user_site_list, name='user-home'),
    path('home/add/', create_user_site, name='add-site'),
    path('home/<int:pk>/delete', site_delete, name='delete-site'),
    path('home/site-info', site_info_list, name='site-info'),

    re_path(r'[^\s]+[\w]/', proxy_url, name='proxy_url'),
]
