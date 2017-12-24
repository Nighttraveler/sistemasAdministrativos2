from django import forms



class BaseMovimientoFormSet(forms.BaseFormSet):
    def clean(self):
        super(BaseMovimientoFormSet, self).clean()

        if any(self.errors):
            return

        debe_total = 0
        haber_total = 0

        for form in self.forms:
                debe = form.cleaned_data['debe']
                haber = form.cleaned_data['haber']
                 
                if ((debe!=None and haber!=None)):

                    raise forms.ValidationError(
                            'Solo complete debe o haber en cada movimiento'
                            )
                else:
                    if debe:
                        debe_total += debe

                    if haber:
                        haber_total += haber


        if ( (debe_total !=  haber_total)    ) :
            raise forms.ValidationError(
                    'Respete la partida doble!!'
                )

        if (debe_total==0 and haber_total==0):
            raise forms.ValidationError(
                'No puedes guardar movimientos vacios!!'
            )
