from django.db.models import Manager




class CuentaManager(Manager):

    def get_cuentas_with_movimientos(self,movimientos,*args,**kargs):

        cuentas =  super(CuentaManager, self).get_queryset().all()
        return cuentas.filter(id__in=movimientos)






class MovimientoManager(Manager):

    def get_between_dates(self, initial_date=None, end_date=None):


        return super(MovimientoManager,self).get_queryset().filter(
                                            numeroAsiento__fecha__range=(
                                                                initial_date,
                                                                end_date)
                                            )
