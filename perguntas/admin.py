from django.contrib import admin

from perguntas.models import Pergunta, Alternativa, Perguntaresposta

admin.site.register(Pergunta)
admin.site.register(Alternativa)
admin.site.register(Perguntaresposta)
