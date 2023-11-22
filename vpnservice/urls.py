from django.urls import path, re_path

from .views import (
    UserSiteListView,
    user_login,
    user_signup,
    user_logout,
    index,
)

urlpatterns = [
    # path('', index, name='home'),  # http://127.0.0.1:8000/
    path('', user_login, name='login'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('user-name/', UserSiteListView.as_view(), name='user_site_list'),  # http://127.0.0.1:8000/user-name/
    # re_path(r'(?P<user_path>/.*)', views.proxy_url, name='user_path),
]

# http://127.0.0.1:8000/user-site-name/ident.me/
# https://ident.me/
# http://127.0.0.1:8000/user-site-name/ukr.net/
# http://127.0.0.1:8000/user-site-name/meta.ua/
# https://www.ukr.net/
# //www.ukr.net/news/main.html
# https://www.yahoo.com/
# http://127.0.0.1:8000/user-site-name/google.com/
# http://127.0.0.1:8000/user-site-name/rozetka.com.ua/
# https://rozetka.com.ua/
# https://rozetka.com.ua
