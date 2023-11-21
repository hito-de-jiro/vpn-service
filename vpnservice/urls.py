from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'(?P<user_path>/.*)', views.proxy_url),
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