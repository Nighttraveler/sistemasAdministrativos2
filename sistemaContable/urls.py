from django.conf.urls import url,include
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

from . import views

app_name ='sistemaContable'

urlpatterns = [


    url(r'^cargar-asientos/$', login_required(views.CargarAsientos.as_view()), name='cargarasientos'),

    url(r'^home/librodiario$', login_required(views.LibroDiario.as_view()), name='librodiario'),

    url(r'^home/libromayor$', login_required(views.LibroMayor.as_view()), name='libromayor'),

    url(r'^home/cuentas$', login_required(views.Cuentas.as_view()), name='cuentas'),




]
