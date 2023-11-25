from django.urls import path, re_path
from .views import (
    home,
    RegisterView,

    UserSiteListView,
    UserSiteCreateView,
    SiteDeleteView,
)

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),

    path('user-name-home/', UserSiteListView.as_view(), name='home'),
    path('add/', UserSiteCreateView.as_view(), name='add_site'),
    path('user-name-home/<int:pk>/delete', SiteDeleteView.as_view(), name='delete_site'),
    # re_path(r'(?P<user_path>/.*)', proxy_url, name='user_path'),
]
