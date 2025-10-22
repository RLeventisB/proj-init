from django import forms
from .models import Usuarios


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
        
class LoginForm(forms.Form):
    correo = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    contraseña = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))

    def clean(self):
        super().clean()
        correo = self.cleaned_data.get('correo')
        contraseña = self.cleaned_data.get('contraseña')
        if correo and contraseña:
            if not Usuarios.objects.filter(correo=correo, contraseña=contraseña).exists():
                raise forms.ValidationError('Correo o contraseña incorrectos.')
            
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['nombre']
    
        labels = {
            'nombre': 'Nuevo nombre de usuario',
        }
    
    def clean(self):
        super().clean()
        nombre = self.cleaned_data.get('nombre')
        if nombre and len(nombre) < 5:
            raise forms.ValidationError('El nombre de usuario debe tener al menos 5 caracteres.')

    