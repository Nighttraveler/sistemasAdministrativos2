# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

# Create your models here.
class TipoCuenta(models.Model):
    Tipo = models.CharField(max_length=30)

    def __str__(self):
        return self.Tipo



class Cuenta(models.Model):
    denominacion = models.CharField(max_length=30)
    Tipo = models.ForeignKey(TipoCuenta, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.denominacion +' -- '+str(self.Tipo)

    class Meta:
        ordering = ['Tipo']

class Asiento(models.Model):
    numeroAsiento = models.AutoField(primary_key=True)
    fecha = models.DateField(default=timezone.localtime(timezone.now()) )

    def __str__(self):
        return str(self.numeroAsiento)

class Movimiento(models.Model):
    cuenta = models.ForeignKey(Cuenta,on_delete=models.CASCADE)
    debe = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2)
    haber = models.DecimalField(blank=True,null=True,max_digits=10, decimal_places=2)
    numeroAsiento = models.ForeignKey(Asiento,on_delete=models.CASCADE)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)



    def __str__(self):
        return str(self.numeroAsiento)
