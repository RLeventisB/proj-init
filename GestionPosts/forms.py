from PIL import Image, ImageOps
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

    def save(self, *args, **kwargs):
        if self['imagen']:
            size = (100, 150)
            # codigo de resizear imagen a un tamaño especifico, sacado de https://pillow.readthedocs.io/en/latest/handbook/tutorial.html
            # aunqeu seria mejor que el usuario pudiese elegir un rectangulo de la imagen asi que lo comente por eso :(
            # with Image.open("hopper.webp") as im:
            #     ImageOps.contain(im, size).save("imageops_contain.webp")
            #     ImageOps.cover(im, size).save("imageops_cover.webp")
            #     ImageOps.fit(im, size).save("imageops_fit.webp")
            #     ImageOps.pad(im, size, color="#f00").save("imageops_pad.webp")
            #
            #     # thumbnail() can also be used,
            #     # but will modify the image object in place
            #     im.thumbnail(size)
            #     im.save("image_thumbnail.webp")
            #     self.imagen = im

            # self.imagen = get_thumbnail(self.image, '500x600', quality=99, format='JPEG')
        return super().save(*args, **kwargs)


class CommentForm(forms.Form):
    body = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Deja un comentario!", "rows": 1}
        )
    )
