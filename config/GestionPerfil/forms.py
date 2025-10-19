from django import forms
from .models import Usuarios

class CuestionarioForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ('correo', 'nombre', 'contraseña', 'contraseña2')
        
    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get('contraseña')
        contraseña2 = cleaned_data.get('contraseña2')
        if contraseña != contraseña2:
            raise forms.ValidationError('Los campos deben ser iguales')