from django import forms
from .models import Usuarios
from django.core.validators import MinLengthValidator

class CuestionarioForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ('correo', 'nombre', 'contraseña', 'contraseña2')
        
        labels = {
            'correo': 'Correo Electrónico',
            'nombre': 'Nombre de Usuario',
            'contraseña': 'Contraseña',
            'contraseña2': 'Repetir Contraseña',
        }

        help_texts = {
            'contraseña': '<strong>Máximo 10 caracteres.</strong>',
        }
        
        widgets = {
            'nombre': forms.TextInput(attrs={'minlength': 5}),
            'contraseña': forms.PasswordInput(),
            'contraseña2': forms.PasswordInput(),
        }

    def clean(self):
        super().clean()
        contraseña = self.cleaned_data.get('contraseña')
        contraseña2 = self.cleaned_data.get('contraseña2')

        if contraseña and contraseña2 and contraseña != contraseña2:
            raise forms.ValidationError('Las contraseñas deben coincidir.')