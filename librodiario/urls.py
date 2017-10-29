from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

from . import views

app_name ='libro'

urlpatterns = [

     
    url(r'^$', views.Index.as_view(), name='index'),

    url(r'^home/$', login_required(views.Home.as_view()), name='home'),

    url(r'^home/librodiario$', login_required(views.LibroDiario.as_view()), name='librodiario'),

    url(r'^home/libromayor$', login_required(views.LibroMayor.as_view()), name='libromayor'),

    url(r'^home/cuentas$', login_required(views.Cuentas.as_view()), name='cuentas'),




]
