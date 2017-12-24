from .models import Asiento, Movimiento, Cuenta
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce

## functions Movimiento services
def get_all_movimientos():

    return Movimiento.objects.all()

def get_movimientos_between_dates(initial_date,end_date):

    return Movimiento.objects.filter(
                                        numeroAsiento__fecha__range=(
                                                initial_date,
                                                end_date)
                                    )

## Asiento services
def get_all_asientos():

    return Asiento.objects.all()

## Cuenta services

def get_all_cuentas():

    return Cuenta.objects.all()

def get_all_cuentas_order_by(element):

    return Cuenta.objects.all().order_by(element) 


def annotate_saldo_to_cuentas(queryset):
    """ for each object in queryset anotate the sum of (debe-haber)"""
    return queryset.annotate(
                saldo=Coalesce(Sum('debe'),0)
                     -
                      Coalesce(Sum('haber'),0)
                 )
