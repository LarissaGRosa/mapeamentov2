from django.urls import path

from aplicativo.views import NoticiaList, NoticiaDetail, Estatisticas, LoginView, PerguntasList, Novaescola, \
    Novoprofessor, Listaescola, Listprofessores, Editarprofessor, Desativarprofessor, Adicionarformacao, Editarescola, \
    Editarperfilescola, Escolaperfil, Escolaperfils, EscolaList, Createescolaperfil, Perguntasa, Perguntasd

app_name = 'mobile'

urlpatterns = [
    path("noticiasapp/", NoticiaList.as_view(), name="noticias_list"),
    path("detalhes/<int:pk>/", NoticiaDetail.as_view(), name="noticia_detalhe"),
    path("dados", Estatisticas.as_view(), name="dados_aplicativo"),
    path("login", LoginView.as_view(), name="loginview"),
    path("perguntas", PerguntasList.as_view(), name="perguntas"),
    path("novaescola", Novaescola.as_view(), name="novaescola"),
    path("novoprofessor", Novoprofessor.as_view(), name="novoprofessor"),
    path("minhasescolas", Listaescola.as_view(), name="minhasescolas"),
    path("meusprofessores", Listprofessores.as_view(), name="meusprofessores"),
    path("editarprofessor", Editarprofessor.as_view(), name="editarprofessores"),
    path("desativarprofessor", Desativarprofessor.as_view(), name="desativarprofessores"),
    path("adicionarformacao", Adicionarformacao.as_view(), name="addformacao"),
    path("editarescola", Editarescola.as_view(), name="editarescola"),
    path("editarperfilescola", Editarperfilescola.as_view(), name="editarperfilescola"),
    path("escolaperfil", Escolaperfils.as_view(), name="escolaperfil"),
    path("escolas", EscolaList.as_view(), name="escolalista"),
    path("createrel", Createescolaperfil.as_view(), name="createescolaperfil"),
    path("perguntasa", Perguntasa.as_view(), name="perguntasa"),
    path("perguntasd", Perguntasd.as_view(), name="perguntasd")
]