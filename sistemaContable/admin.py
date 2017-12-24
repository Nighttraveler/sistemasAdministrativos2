# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import Asiento,Cuenta,Movimiento
from django.contrib import admin

# Register your models here.

admin.site.register(Asiento)
admin.site.register(Cuenta)
admin.site.register(Movimiento)
