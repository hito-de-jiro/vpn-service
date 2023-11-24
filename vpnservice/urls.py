from django.urls import path, re_path

from .views import (
    UserSiteListView,
    UserSiteCreateView,
    SiteDeleteView,
    user_login,
    user_signup,
    user_logout,
)

urlpatterns = [
    path('', user_login, name='login'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('user-name-home/', UserSiteListView.as_view(), name='home'),
    path('add/', UserSiteCreateView.as_view(), name='add_site'),
    path('user-name-home/<int:pk>/delete', SiteDeleteView.as_view(), name='delete_site'),
    # re_path(r'(?P<user_path>/.*)', proxy_url, name='user_path'),
]
