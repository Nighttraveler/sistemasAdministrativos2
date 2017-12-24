# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

from .model_managers import MovimientoManager, CuentaManager
# Create your models here.



class Cuenta(models.Model):

    TIPOS_CUENTA = (
        ('A','Activo'),
        ('P','Pasivo'),
        ('P.N','Patrimonio Neto'),
        ('R.N','Resultado Negativo'),
        ('R.P','Resultado Positivo'),
    )


    denominacion  = models.CharField(max_length=30)

    Tipo          = models.CharField(
                        max_length=3,
                        choices=TIPOS_CUENTA,
    )

    saldo_inicial = models.DecimalField(
                                max_digits=50,
                                decimal_places=2,
                                default=0
    )

    saldo_actual  = models.DecimalField(
                                max_digits=50,
                                decimal_places=2,
                                null=True,
                                blank=True,
    )

    def save(self,*args,**kwargs):

        if (not self.saldo_actual):
            self.saldo_actual = self.saldo_inicial

        super(Cuenta, self).save(*args,**kwargs)

    objects = CuentaManager()

    def __str__(self):
        return "%s -- %s" %(self.denominacion,str(self.Tipo))

    class Meta:
        ordering = ['Tipo']



class Asiento(models.Model):


    numeroAsiento = models.AutoField(primary_key=True)
    fecha         = models.DateField(default=timezone.now)
    usuario       = models.ForeignKey(User,on_delete=models.CASCADE)



    def __str__(self):
        return str(self.numeroAsiento)

class Movimiento(models.Model):

    numeroAsiento = models.ForeignKey(Asiento,on_delete=models.CASCADE)
    cuenta        = models.ForeignKey(Cuenta,on_delete=models.CASCADE)
    debe          = models.DecimalField(blank=True,
                                        null=True,
                                        max_digits=50,
                                        decimal_places=2)
    haber         = models.DecimalField(blank=True,
                                        null=True,
                                        max_digits=50,
                                        decimal_places=2)

    def save(self,*args,**kwargs):
        super(Movimiento, self).save(*args,**kwargs)

        cuenta = self.cuenta

        d  = self.debe  or 0
        h  = self.haber or 0

        if cuenta.Tipo == 'A' or cuenta.Tipo=='R.N':
            cuenta.saldo_actual = cuenta.saldo_actual+(d-h)
            cuenta.save(update_fields=['saldo_actual'])

        elif cuenta.Tipo == 'P' or cuenta.Tipo=='R.P':
            cuenta.saldo_actual = cuenta.saldo_actual+(h-d)
            cuenta.save(update_fields=['saldo_actual'])

    objects = MovimientoManager()

    def __str__(self):
        return str(self.cuenta)
