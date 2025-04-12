from django import forms
from .models import Laudo, Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'data_nascimento']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

class LaudoUploadForm(forms.ModelForm):
    class Meta:
        model = Laudo
        fields = ['paciente', 'tipo_exame', 'data_exame', 'arquivo_pdf']
        widgets = {
            'data_exame': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].widget.attrs.update({'class': 'form-select'})
        self.fields['tipo_exame'].widget.attrs.update({'class': 'form-select'})
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 