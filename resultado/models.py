from django.db import models


class Noticia(models.Model):
    titulo = models.CharField(max_length=100)
    texto = models.TextField(max_length=1000)
    data_publi = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)
    foto = models.ImageField(upload_to='noticia/media', null=True)

    def __str__(self):
        return "%s noticia: %s" % (self.titulo, self.texto)
