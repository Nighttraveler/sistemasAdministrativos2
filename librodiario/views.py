# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.views import generic, View
from django.shortcuts import render
from django.forms import formset_factory


from .models import Cuenta
from .forms import MovimientoForm , AsientoForm
from .formset import BaseMovimientoFormSet
import services

# Create your views here.

class Index(generic.TemplateView):
    template_name = 'librodiario/index.html'

class Home(generic.View):

    template_name = 'librodiario/home.html'
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

                asiento_form = asiento_form.save()
                for form in formset:

                    form.clean()
                    movimiento = form.save(commit=False)
                    movimiento.numeroAsiento = asiento_form
                    movimiento.usuario = request.user
                    movimiento.save()

                return HttpResponseRedirect(reverse_lazy('libro:librodiario'))


        context = { 'formset':formset,
                    'asiento_form': asiento_form,
                    }

        return render(request, self.template_name, context)






class LibroDiario(generic.View):

    template_name = "librodiario/libroDiario.html"



    def get(self,request):
        desde = request.GET.get('desde')
        hasta =  request.GET.get('hasta')


        context={}
        if desde and hasta:
            context['movimientos'] = services.get_movimientos_between_dates(desde,hasta)
        else:
            context['movimientos']= services.get_all_movimientos()
        context['asientos'] = services.get_all_asientos()

        return render(request, self.template_name, context)



class LibroMayor(generic.View):

    template_name = 'librodiario/libroMayor.html'


    def get(self,request):
        desde = request.GET.get('desde')
        hasta =  request.GET.get('hasta')

        context = {}
        if desde and hasta:
            context['cuentas'] =services.annotate_saldo_to_cuentas(
                                    services.get_movimientos_between_dates(desde,hasta).values('cuenta','cuenta__denominacion')
                                )
            context["movimientos"] = services.get_movimientos_between_dates(
                                                                desde,
                                                                hasta
                                                                )
            context['desde'] = desde
            context['hasta'] = hasta
        else:

            context['cuentas'] =services.annotate_saldo_to_cuentas(
                                    services.get_all_movimientos().values('cuenta','cuenta__denominacion')
                                    )
            context["movimientos"] = services.get_all_movimientos()


        print(context['cuentas'])

        return render(request, self.template_name, context)



class Cuentas(generic.edit.CreateView):

    template_name = 'librodiario/cuentas.html'
    model = Cuenta
    fields = ['denominacion','Tipo']
    success_url = reverse_lazy('libro:cuentas')

    def get_context_data(self, **kwargs):
        context = super(Cuentas, self).get_context_data(**kwargs)

        context["cuentas"] = services.get_all_cuentas()
        return context
