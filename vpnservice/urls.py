from django.urls import path

from vpnservice import views

urlpatterns = [
    path('', views.index),
    path('<str:user_name>/<slug:site_name>', views.site_redirect),
    ]
