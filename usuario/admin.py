from django.contrib import admin

from usuario.models import Privateprofessor, Perfil, Escola, Secretaria, Formacao, Professor, Escolaperfil, \
    Professorescola

admin.site.register(Perfil)
admin.site.register(Escola)
admin.site.register(Secretaria)
admin.site.register(Privateprofessor)
admin.site.register(Formacao)
admin.site.register(Professor)
admin.site.register(Escolaperfil)
admin.site.register(Professorescola)
