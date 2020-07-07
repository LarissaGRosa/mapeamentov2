from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm
from django import forms
from resultado.models import Noticia


class NoticiaForm(ModelForm):
    foto = forms.ImageField()

    class Meta:
        model = Noticia
        fields = ['titulo', 'texto', 'data_publi', 'foto', 'autor']

        def save(self, commit=True):
            perfil = super(NoticiaForm, self).save(commit=False)
            if commit:
                perfil.save()
            return perfil