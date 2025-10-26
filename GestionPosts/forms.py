import easymde.widgets
from django import forms

from .models import Publicaciones, Tags


class PostForm(forms.ModelForm):
    class Meta:
        model = Publicaciones
        fields = ('titulo', 'resumen', 'parrafo', 'imagen', 'tags')

        labels = {
            'titulo': 'Titulo',
            'resumen': 'Resumen del post',
            'parrafo': 'Texto',
            'imagen': 'Imagen',
            'tags': 'Tags',
        }

        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Titulo'}),
            'resumen': forms.TextInput(attrs={'placeholder': 'Resumen'}),
            'parrafo': easymde.widgets.EasyMDEEditor(),
            'imagen': forms.FileInput(attrs={'placeholder': 'Imagen'}),
        }

    tags = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def clean(self):
        super().clean()
