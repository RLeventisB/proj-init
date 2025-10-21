from django import forms

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100)
