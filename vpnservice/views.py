from django.shortcuts import render, redirect


HOST = 'http://127.0.0.1:8000/'
USER_SITE_NAME = 'user-site-name/'
URL = 'https://www.ukr.net/'
site_name = URL.split('www.')


def index(request):
    return redirect(f'{HOST}{USER_SITE_NAME}{site_name[1]}')


def site_redirect(request, user_name=USER_SITE_NAME, site_name=URL):
    return redirect(f'{HOST}{user_name}{site_name[1]}')


def url_redirect(request):
    url = "http://%s%s" % ('localhost', request.path)
    return url

