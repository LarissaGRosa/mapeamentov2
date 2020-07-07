from django.db import models

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, default=None, null=True, on_delete=models.CASCADE)
    tipo = models.IntegerField(default=None, null=True)


class Secretaria(models.Model):
    user = models.OneToOneField(Perfil, default=None, null=True, on_delete=models.CASCADE)
    municipio = models.CharField(max_length=100, null=True)
    cod = models.CharField(max_length=15, null=True)


class Escola(models.Model):
    user = models.OneToOneField(Perfil, default=None, null=True, on_delete=models.CASCADE)
    regiao = models.CharField(max_length=10)
    uf = models.CharField(max_length=2)
    municipio = models.CharField(max_length=50)
    cod_municipio = models.CharField(max_length=50)
    dependencia = models.CharField(max_length=50)
    nome = models.CharField(max_length=200)
    secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE, null=True)


class Privateprofessor(models.Model):
    nome = models.CharField(max_length=100, null=True)
    ensinomedio = models.CharField(max_length=30, null=True)
    inimagisterio = models.CharField(max_length=20, null=True)
    secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE)
    isAtivo = models.BooleanField(default=True)


class Formacao(models.Model):
    instituicao = models.CharField(max_length=150, null=True)
    periodo = models.CharField(max_length=150, null=True)
    curso = models.CharField(max_length=150, null=True)
    isGraduacao = models.BooleanField()
    isPosgraduacao = models.BooleanField()
    professor = models.ForeignKey(Privateprofessor, on_delete=models.CASCADE, null=True)


class Professorescola(models.Model):
    professor = models.ForeignKey(Privateprofessor, on_delete=models.CASCADE)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    ano_inicio = models.CharField(max_length=4)
    ano_fim = models.CharField(max_length=4, null=True)


class Professor(models.Model):
    user = models.OneToOneField(Perfil, default=None, null=True, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='usuarios/media', null=True)
    formacao = models.CharField(max_length=300)
    leciona = models.CharField(max_length=300)


class Escolaperfil(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    isAceito = models.BooleanField(default=False)

