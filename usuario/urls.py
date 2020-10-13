from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from . import views

app_name = 'perfil'

urlpatterns = [
    path('secretaria', views.secretaria, name='secretaria'),
    path('addescola', views.cadastro_escola, name='addescola'),
    path('<int:pk>/get_professor', views.get_professor1, name='getprofessor'),

    path('desativarprofessor1', views.desativar_professor1, name='desativarprofessor1'),
    path('get_professor1', views.get_professor1, name='getprofessor1'),
    path('editar_professor', views.editar_professor, name='editarprofessor'),
    path('<int:pk>/desativarprofessor', views.desativar_professor, name='desativarprofessor'),
    path('escola', views.escola, name='escola'),
    path('validaescola', views.validaescola, name='mudarvinculo'),
    path('editescola', views.editar_escola, name='editescola'),
    path('editescolas', views.editarescolas, name='editescolas'),
    path('professor', views.professorpage, name='professor'),
    path('escolaperfil', views.escolaperfil, name='escolaperfil'),
    path('<int:pk>/responder', views.responderd, name='rd'),
    path('<int:pk>/respondera', views.respondera, name='ra'),
    path('perguntas', views.perguntas, name='perguntas'),
    path('logout', views.do_logout, name='do_logout'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.do_login, name='do_login'),
    path('mudarsenha', views.alterar_senha, name='mudarsenha'),
    path('adm', views.administrador, name='adm'),
    path('novapergunta', views.novapergunta, name='novapergunta'),
    path('novaalternatica', views.novaalternatica, name='novaalternativa'),
    path('desativarpergunta', views.desativar_pergunta, name='desativarpergunta'),
    path('postar', views.postar, name="postar"),
    path('desativarpostagem', views.desativar_postagem, name='desativarpostagem'),
    path('desativarescola', views.desativarescola, name='desativarescola'),
    path('getescola', views.get_escola, name='getescola'),
    path('testenome', views.teste_nome, name='testenome'),
    path('testeuser', views.teste_user, name='testeuser'),
    path('testeprof', views.teste_professor, name='testeprof'),
    path('<int:pk>/escolaprof', views.professores_escola, name='escolaprof'),
    path('ativaruso', views.ativaruso, name='ativaruso')



]
