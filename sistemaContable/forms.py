from django import forms
from models import Movimiento, Asiento
from django.contrib.auth.models import User
import datetime


class DateInput(forms.DateInput):
    input_type = 'date'

class AsientoForm(forms.ModelForm):
    class Meta:
        model = Asiento
        fields = ['fecha',]
        widgets = {'fecha': DateInput(),}

    def clean_fecha(self):
        data = self.cleaned_data['fecha']

        if data > datetime.date.today():
            raise forms.ValidationError("La fecha no puede ser en el futuro")
        return data

class MovimientoForm(forms.ModelForm):
    class Meta:
        model =  Movimiento
        fields = ['cuenta','debe','haber' ]
        widgets = {
            'cuenta': forms.Select(attrs={'style':"width: 300px",
                                            'required':'True'
                                            }),
            }
