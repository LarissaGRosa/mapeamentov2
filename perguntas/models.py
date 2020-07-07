from django.contrib.auth.models import User
from django.db import models


class Pergunta(models.Model):
    questionario = models.IntegerField()
    questao = models.CharField(max_length=300)
    isAlternativa = models.BooleanField()
    isDissertativa = models.BooleanField()
    autor = models.CharField(max_length=30)

    def __str__(self):
        return "%s noticia: %s" % (self.questionario, self.questao)


class Alternativa(models.Model):
    id_questao = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    numero = models.IntegerField()
    alternativa = models.CharField(max_length=300)

    def __str__(self):
        return "%s alternatica: %s" % (self.numero, self.alternativa)


class Perguntaresposta(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_questao = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    alternativa = models.IntegerField(null=True)
    resposta = models.TextField(null=True)


