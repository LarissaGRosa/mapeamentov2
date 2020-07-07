from django.contrib.auth.models import User
from rest_framework import serializers

from perguntas.models import Pergunta, Alternativa
from usuario.models import Secretaria, Escola, Privateprofessor, Professor, Perfil, Escolaperfil
from .models import Noticia


class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = '__all__'


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'


class SecretariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secretaria
        fields = '__all__'


class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = ['regiao', 'uf', 'municipio', 'cod_municipio', 'dependencia', 'nome', 'pk']


class PprofessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Privateprofessor
        fields = ['pk', 'inimagisterio', 'nome', 'ensinomedio']


class PerguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pergunta
        fields = ['questao', 'id']


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'


class AlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class EscolaperfilSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer()

    class Meta:
        model = Escolaperfil
        fields = ['professor', 'id', 'isAceito']


