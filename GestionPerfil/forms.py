from django import forms
from .models import Usuarios
import hashlib


class SignupForm(forms.ModelForm):
    contraseña2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Repetir Contraseña'}))
    class Meta:
        model = Usuarios
        fields = ('correo', 'nombre', 'contraseña')
        
        labels = {
            'correo': 'Correo Electrónico',
            'nombre': 'Nombre de Usuario',
            'contraseña': 'Contraseña',
        }
        
        widgets = {
            'correo': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico'}),
            'nombre': forms.TextInput(attrs={'minlength': 5, 'placeholder': 'Nombre'}),
            'contraseña': forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        }

    def set_contraseña_encriptada(self, valor):
        self.contraseña = hashlib.sha256(valor.encode()).hexdigest()
        self.contraseña2 = hashlib.sha256(valor.encode()).hexdigest()
    
    def get_contraseña_encriptada(self):
        return self.contraseña, self.contraseña2

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
        widgets = {
            'nombre': forms.TextInput(attrs={'minlength': 5})
        }    

