from django import forms
from martor.fields import MartorFormField
from martor.widgets import MartorWidget, AdminMartorWidget

from .models import Publicaciones, Tags


class PostForm(forms.ModelForm):
    # tuve el 0% de encontrar un post de medium que no me fuerza apagar para verlo
    # esto de abajo salio de https://medium.com/swlh/django-forms-for-many-to-many-fields-d977dec4b024 !!!
    tags = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Publicaciones
        fields = ('titulo', 'resumen', 'parrafo', 'imagen')

        labels = {
            'titulo': 'Titulo',
            'resumen': 'Resumen del post',
            'parrafo': 'Texto',
            'imagen': 'Imagen'
        }

        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Titulo'}),
            'resumen': forms.TextInput(attrs={'placeholder': 'Resumen'}),
            'parrafo': MartorFormField(),
            'imagen': forms.FileInput(attrs={'placeholder': 'Imagen'}),
        }

    def clean(self):
        super().clean()
