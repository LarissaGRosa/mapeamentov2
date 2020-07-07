from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm
from django import forms

from usuario.models import Escola, Perfil, Professor, Privateprofessor


class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['tipo']

        def save(self, commit=True):
            perfil = super(PerfilForm, self).save(commit=False)
            if commit:
                perfil.save()
            return perfil

        @receiver(post_save, sender=User)
        def update_profile_signal(sender, instance, created, **kwargs):
            if created:
                Perfil.objects.create(user=instance)
            instance.perfil.save()

        post_save.connect(update_profile_signal, sender=User)


class EscolaForm(ModelForm):
    class Meta:
        model = Escola
        fields = ['cod_municipio', 'dependencia', 'municipio', 'nome', 'regiao', 'uf']

        def save(self, commit=True):
            escola = super(EscolaForm, self).save(commit=False)
            if commit:
                escola.save()
            return escola


class ProfessorForm(ModelForm):
    foto = forms.ImageField()

    class Meta:
        model = Professor
        fields = ['foto', 'formacao', 'leciona']

        def save(self, commit=True):
            perfil = super(ProfessorForm, self).save(commit=False)
            if commit:
                perfil.save()
            return perfil


