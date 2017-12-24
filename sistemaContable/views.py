# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.views import generic, View
from django.shortcuts import render
from django.forms import formset_factory


from .models import Cuenta,Movimiento,Asiento
from .forms import MovimientoForm , AsientoForm
from .formset import BaseMovimientoFormSet
import services

# Create your views here.


class CargarAsientos(generic.View):

    template_name = 'sistemaContable/cargarAsientos.html'
    asiento_form = AsientoForm
    movimiento_form_set =  formset_factory(
                            MovimientoForm,
                            formset = BaseMovimientoFormSet,
                            extra=2
                            )

    def get(self, request):

        formset = self.movimiento_form_set()

        context = { 'formset':formset,
                    'asiento_form': self.asiento_form
                    }
        return render(request, self.template_name, context)


    def post(self,request):


        asiento_form = self.asiento_form(request.POST)
        formset = self.movimiento_form_set(request.POST)

        if asiento_form.is_valid():
            asiento_form.clean()

            if formset.is_valid():

                asiento =asiento_form.save(commit=False)
                asiento.usuario = request.user
                asiento.save()


                for form in formset:

                    form.clean()
                    movimiento = form.save(commit=False)
                    movimiento.numeroAsiento = asiento

                    movimiento.save()

                return HttpResponseRedirect(reverse_lazy('sistemaContable:librodiario'))


        context = { 'formset':formset,
                    'asiento_form': asiento_form,
                    }

        return render(request, self.template_name, context)






class LibroDiario(generic.View):

    template_name = "sistemaContable/libroDiario.html"



    def get(self,request):
        desde = request.GET.get('desde')
        hasta =  request.GET.get('hasta')


        context={}
        if desde and hasta:
            context['movimientos'] = Movimiento.objects.get_between_dates(desde,hasta)
        else:
            context['movimientos']= Movimiento.objects.all()


        context['desde']    = desde
        context['hasta']    = hasta
        

        return render(request, self.template_name, context)



class LibroMayor(generic.View):

    template_name = 'sistemaContable/libroMayor.html'


    def get(self,request):

        context = {}

        context['cuentas'] = Cuenta.objects.get_cuentas_with_movimientos(
                            Movimiento.objects.all().values('cuenta_id')
        )

        return render(request, self.template_name, context)



class Cuentas(generic.edit.CreateView):

    template_name = 'sistemaContable/cuentas.html'
    model = Cuenta
    fields = ['denominacion','Tipo','saldo_inicial']
    success_url = reverse_lazy('sistemaContable:cuentas')

    def get_context_data(self, **kwargs):

        context = super(Cuentas, self).get_context_data(**kwargs)
        context["cuentas"] = services.get_all_cuentas()

        return context
