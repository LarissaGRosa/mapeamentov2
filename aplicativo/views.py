import json
from itertools import count

from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Create your views here.
from perguntas.models import Pergunta, Alternativa, Perguntaresposta
from resultado.models import Noticia
from resultado.serializers import NoticiaSerializer, PerguntaSerializer, ProfessorSerializer, PprofessorSerializer, \
    EscolaSerializer, EscolaperfilSerializer, UserSerializer, AlternativaSerializer
from usuario.models import Formacao, Secretaria, Privateprofessor, Professor, Escola, Perfil, Escolaperfil
from django.contrib.auth import authenticate


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        perfil = Perfil.objects.get(user=user)
        if user:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)

            return Response({"token": user.auth_token.key, "perfil": perfil.tipo})


class NoticiaList(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        noticias = Noticia.objects.all()[:20]
        data = NoticiaSerializer(noticias, many=True).data
        return Response(data)


class NoticiaDetail(APIView):
    def get(self, request, pk):
        noticia = get_object_or_404(Noticia, pk=pk)
        data = NoticiaSerializer(noticia).data
        return Response(data)


class Estatisticas(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        graduacao = Formacao.objects.filter(isGraduacao=True).count()
        posgraduacao = Formacao.objects.filter(isPosgraduacao=True).count()
        municipios = Secretaria.objects.all().count()
        professores = Privateprofessor.objects.all().count()
        cadastros = Professor.objects.all().count()
        escolas = Escola.objects.all().count()
        data = {
            "graduacao": graduacao,
            "posgraduacao": posgraduacao,
            "municipios": municipios,
            "professores": professores,
            "cadastros": cadastros,
            "escolas": escolas
        }
        return JsonResponse(data)


class PerguntasList(generics.ListCreateAPIView):
    perguntas = Pergunta.objects.all()
    data = PerguntaSerializer(perguntas, many=True).data


class Novaescola(APIView):

    def post(self, request, *args):
        perfil = Perfil.objects.get(user=request.user)
        secretaria1 = get_object_or_404(Secretaria, user=perfil)

        nome = request.data.get('nome')
        email = request.data.get('email')
        municipio = request.data.get('municipio')
        cod_municipio = request.data.get('cod_municipio')
        dependencia = request.data.get('dependencia')
        uf = request.data.get('uf')
        regiao = request.data.get('regiao')
        nomedeusuario = request.data.get('nomedeusuario')
        senha = request.data.get('senha')

        response_data = {
            "nome": nome,
            "email": email,
            "municipio": municipio,
            "cod_municipio": cod_municipio,
            "dependencia": dependencia,
            "uf": uf,
            "regiao": regiao,
            "nomedeusuario": nomedeusuario,
            "senha": senha,
            "sucesso": "Sucesso"
        }
        user = User.objects.create_user(
            username=nomedeusuario,
            email=email,
            password=senha,

        )
        user.save()

        user.perfil.tipo = 2
        user.save()
        escola = Escola.objects.create(
            user=user.perfil,
            secretaria=secretaria1,
            nome=nome,
            dependencia=dependencia,
            municipio=municipio,
            cod_municipio=cod_municipio,
            uf=uf,
            regiao=regiao,
        )
        escola.save()

        return JsonResponse(response_data)


class Novoprofessor(APIView):

    def post(self, request, *args):
        perfil = Perfil.objects.get(user=request.user)
        secretaria1 = get_object_or_404(Secretaria, user=perfil)
        nome = request.data.get('nome')
        ensinomedio = request.data.get('ensinomedio')
        instgrad = request.data.get('instgrad')
        cursograd = request.data.get('cursograd')
        periodograd = request.data.get('periodograd')
        select = request.data.get('selectedValue')
        iniciomagis = request.data.get('iniciomagis')
        try:
            professor = Privateprofessor.objects.create(
                nome=nome,
                ensinomedio=ensinomedio,
                secretaria=secretaria1,
                inimagisterio=iniciomagis,
            )
            professor.save()
            if select == "1":
                Formacao.objects.create(
                    instituicao=instgrad,
                    curso=cursograd,
                    periodo=periodograd,
                    professor=professor,
                    isGraduacao=True,
                    isPosgraduacao=False

                )
            if select == "2":
                Formacao.objects.create(
                    instituicao=instgrad,
                    curso=cursograd,
                    periodo=periodograd,
                    professor=professor,
                    isGraduacao=False,
                    isPosgraduacao=True

                )
            response = {
                "status": "1"
            }
            return JsonResponse(response)
        except:
            response = {
                "status": "2"
            }
            return JsonResponse(response)


class Listprofessores(APIView):
    def get(self, request, *args):
        perfil = Perfil.objects.get(user=request.user)
        secretaria1 = get_object_or_404(Secretaria, user=perfil)
        professores = Privateprofessor.objects.filter(secretaria=secretaria1)

        data = PprofessorSerializer(professores, many=
        True).data
        return Response(data)


class Listaescola(APIView):
    def get(self, request, *args):
        perfil = Perfil.objects.get(user=request.user)
        secretaria1 = get_object_or_404(Secretaria, user=perfil)
        escola = Escola.objects.filter(secretaria=secretaria1)

        data = EscolaSerializer(escola, many=True).data
        return Response(data)


class Desativarprofessor(APIView):
    def post(self, request, *args):
        perfil = Perfil.objects.get(user=request.user)
        secretaria1 = get_object_or_404(Secretaria, user=perfil)
        pk = request.data.get('pk')
        professor = Privateprofessor.objects.get(id=pk, secretaria=secretaria1)
        professor.isAtivo = False
        professor.save()
        resposta = {
            "status": "Sucesso"
        }
        return JsonResponse(resposta)


class Editarprofessor(APIView):
    def post(self, request, *args):
        perfil = Perfil.objects.get(user=request.user)
        secretaria1 = get_object_or_404(Secretaria, user=perfil)
        nome = request.data.get('nome')
        ensinomedio = request.data.get('ensinomedio')
        iniciomagis = request.data.get('inimagisterio')
        id1 = request.data.get('pk')
        response_data = {
            "status": "sucesso"
        }
        professor = Privateprofessor.objects.get(id=id1, secretaria=secretaria1)
        professor.nome = nome
        professor.ensinomedio = ensinomedio
        professor.inimagisterio = iniciomagis
        professor.save()
        return JsonResponse(response_data)


class Adicionarformacao(APIView):
    def post(self, request, *args):
        perfil = Perfil.objects.get(user=request.user)
        secretaria1 = get_object_or_404(Secretaria, user=perfil)
        instgrad = request.data.get('instgrad')
        cursograd = request.data.get('cursograd')
        periodograd = request.data.get('periodograd')
        select = request.data.get('selectedValue')
        pk = request.data.get('pk')
        professor = Privateprofessor.objects.get(pk=pk, secretaria=secretaria1)
        if select == "1":
            Formacao.objects.create(
                instituicao=instgrad,
                curso=cursograd,
                periodo=periodograd,
                professor=professor,
                isGraduacao=True,
                isPosgraduacao=False

            )
        if select == "2":
            Formacao.objects.create(
                instituicao=instgrad,
                curso=cursograd,
                periodo=periodograd,
                professor=professor,
                isGraduacao=False,
                isPosgraduacao=True

            )
        response = {
            "status": "1"
        }
        return JsonResponse(response)


class Editarescola(APIView):
    def post(self, request, *args):
        perfil = Perfil.objects.get(user=request.user)
        secretaria1 = get_object_or_404(Secretaria, user=perfil)
        nome = request.data.get('nome')
        id1 = request.data.get('pk')
        municipio = request.data.get('municipio')
        cod_municipio = request.data.get('cod_municipio')
        dependencia = request.data.get('dependencia')
        uf = request.data.get('uf')
        regiao = request.data.get('regiao')
        escola = Escola.objects.get(id=id1, secretaria=secretaria1)
        escola.regiao = regiao
        escola.uf = uf
        escola.dependencia = dependencia
        escola.cod_municipio = cod_municipio
        escola.nome = nome
        escola.municipio = municipio
        escola.save()
        resposta = {
            "status": "1"
        }
        return JsonResponse(resposta)


class Editarperfilescola(APIView):
    def post(self, request, *args):
        perfil = Perfil.objects.get(user=request.user)
        nome = request.data.get('nome')
        municipio = request.data.get('municipio')
        cod_municipio = request.data.get('cod_municipio')
        dependencia = request.data.get('dependencia')
        uf = request.data.get('uf')
        regiao = request.data.get('regiao')
        email = request.data.get('email')
        nomedeusuario = request.data.get('nomedeusuario')
        senha = request.data.get('senha')
        escola = Escola.objects.get(user=perfil)
        escola.regiao = regiao
        escola.uf = uf
        escola.dependencia = dependencia
        escola.cod_municipio = cod_municipio
        escola.nome = nome
        escola.municipio = municipio
        escola.save()
        user = User.objects.get(id=request.user.id)
        user.username = nomedeusuario
        user.password = senha
        user.email = email
        resposta = {
            "status": "1"
        }
        return JsonResponse(resposta)


class Escolaperfils(APIView):
    def get(self, request):
        data = []

        escolaperfil = Escolaperfil.objects.select_related('professor')
        for e in escolaperfil:
            record = {"name": e.professor.user.user.username, "id": str(e.id), "isvalido": str(e.isAceito)}
            data.append(record)

        return JsonResponse(data, safe=False)

    def post(self, request, *args):
        perfil = get_object_or_404(Perfil, user=request.user)
        escola1 = get_object_or_404(Escola, user=perfil)
        if escola1:
            id1 = request.data.get('id')
            escolaperfil = Escolaperfil.objects.get(id=id1)
            if escolaperfil.isAceito == False:
                escolaperfil.isAceito = True
                escolaperfil.save()
                response_data = {
                    "name": escolaperfil.professor.user.user.username,
                    "id": escolaperfil.id,
                    "isvalidado": escolaperfil.isAceito
                }
                return JsonResponse(response_data)
            else:
                response_data = {
                    "name": escolaperfil.professor.user.user.username,
                    "id": escolaperfil.id,
                    "isvalidado": escolaperfil.isAceito
                }
                return JsonResponse(response_data)


class EscolaList(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        escolas = Escola.objects.all()
        data = EscolaSerializer(escolas, many=True).data
        return Response(data)


class Createescolaperfil(APIView):

    def post(self, request):
        id1 = request.data.get('pk')
        perfil = Perfil.objects.get(user=request.user)
        professor = Professor.objects.get(user=perfil)
        escola = Escola.objects.get(id=id1)
        escolaperfil = Escolaperfil.objects.create(professor=professor, escola=escola, isAceito=False)
        escolaperfil.save()
        result = {
            "status": "sucesso"
        }
        return JsonResponse(result)


class Perguntasd(APIView):
    def get(self, request):
        perguntas = Pergunta.objects.filter(isDissertativa=True)
        data = PerguntaSerializer(perguntas, many=True).data
        return Response(data)


class Perguntasa(APIView):

    def get(self, request):
        perguntas = Pergunta.objects.filter(isAlternativa=True)
        data = []
        for p in perguntas:
            alternativa = Alternativa.objects.filter(id_questao=p)
            alternativa = AlternativaSerializer(alternativa, many=True).data
            result = {"questao": p.questao, "id": p.id, "alternativas": alternativa}
            data.append(result)

        return JsonResponse(data, safe=False)

    def post(self, request):
        id_questao = int(request.data.get('id_pergunta'))
        alternativa = str(request.data.get('alternativa'))
        questao = Pergunta.objects.get(id=id_questao)

        alternativa = Alternativa.objects.get(id_questao=id_questao, alternativa=alternativa)
        perguntaresposta = Perguntaresposta(
            id_usuario=request.user,
            id_questao=questao,
            alternativa=alternativa.id

        )
        perguntaresposta.save()
        response = {
            "status": "1"
        }
        return JsonResponse(response)


class Perguntasd(APIView):
    def get(self, request):
        perguntas = Pergunta.objects.filter(isAlternativa=False)
        data = PerguntaSerializer(perguntas, many=True).data
        return JsonResponse(data, safe=False)

    def post(self, request, *args):
        id_questao = request.data.get('id_pergunta')
        resposta = request.data.get('resposta')
        questao = Pergunta.objects.get(id=id_questao)
        perguntaresposta = Perguntaresposta(
            id_usuario=request.user,
            id_questao=questao,
            resposta=resposta

        )
        perguntaresposta.save()
        response = {
            "status": "1"
        }
        return JsonResponse(response)
