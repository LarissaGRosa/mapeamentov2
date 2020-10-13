import datetime

from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters

from resultado.form import NoticiaForm
from perguntas.models import Pergunta, Perguntaresposta, Alternativa
from resultado.models import Noticia
from usuario.form import EscolaForm, ProfessorForm
from usuario.models import Privateprofessor, Perfil, Secretaria, Formacao, Escola, Escolaperfil, Professorescola, \
    Professor, Ativar


@login_required()
@sensitive_post_parameters()
def cadastro(request):
    form = UserCreationForm(request.POST or None)
    form2 = ProfessorForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'form2': form2}
    if request.method == 'POST':
        if form.is_valid() and form2.is_valid():
            ativo = Ativar.objects.last()
            if ativo.ativo:
                save = form.save()
                save.refresh_from_db()
                save.perfil.tipo = 1
                save.save()
                perfil = Perfil.objects.get(user=save)
                professor = form2.save(commit=False)
                professor.user = perfil
                professor.save()
                context = {'msg': 'Cadastro efetuado com sucesso', 'form': form, 'form2': form2}
                return render(request, 'usuario/cadastro2.html', context)
            else:
                context = {'msg': 'O cadastro de professores não está habilitado', 'form': form, 'form2': form2}
                return render(request, 'usuario/cadastro2.html', context)

    return render(request, 'usuario/cadastro2.html', context)


@sensitive_post_parameters()
def do_login(request):
    ativo = Ativar.objects.last()
    if ativo.ativo:
        msg = "O login dos professores está ativo"
    else:
        msg = "O login dos professores está desativado"
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.perfil.tipo == 1:
                if ativo.ativo:
                    if user is not None:
                        login(request, user)
                        return redirect('noticias:home')
                else:
                    return render(request, 'usuario/login2.html', {'msg': msg})
            else:
                if user is not None:
                    login(request, user)
                    return redirect('noticias:home')
                else:
                    return render(request, 'usuario/login2.html',  {'msg': msg})
        else:

            msg = "Esse usuário não existe"
            return render(request, 'usuario/login2.html', {'msg': msg})


    else:
        return render(request, 'usuario/login2.html',  {'msg': msg})


def do_logout(request):
    logout(request)
    return redirect('noticias:home')


@login_required
@sensitive_post_parameters()
def alterar_senha(request):
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            return redirect('noticias:home')
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'usuario/alterar_senha2.html', {'form_senha': form_senha})


@login_required
@sensitive_post_parameters()
def secretaria(request):
    perfil = Perfil.objects.get(user=request.user)
    secretaria1 = get_object_or_404(Secretaria, user=perfil)
    escolas = Escola.objects.filter(secretaria=secretaria1)
    professores = Privateprofessor.objects.filter(secretaria=secretaria1, isAtivo=True)
    form = UserCreationForm
    from django.shortcuts import render
    import plotly.graph_objects as go
    from plotly.offline import plot

    x = []
    y = []

    g = 0

    for p in professores:
        forma = Formacao.objects.filter(professor=p, isGraduacao=True)
        for f in forma:
            z = 0
            if len(x) > 0:
                for xx in x:
                    if f == xx:
                        y[x.index[xx]] = y[x.index[xx]] + 1
                        z = z + 1
                if z == 0:
                    x.append(f.curso)
                    y.append(1)

            else:
                x.append(f.curso)
                y.append(1)
            g = g + 1

    fig = go.Figure(go.Bar(x=x, y=y))
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    response = plot_div
    li = []
    m = []
    pg = 0

    for p in professores:
        forma = Formacao.objects.filter(professor=p, isPosgraduacao=True)
        for f in forma:
            z = 0
            if len(li) > 0:
                for xx in li:
                    if f == xx:
                        m[li.index[xx]] = m[li.index[xx]] + 1
                        z = z + 1
                if z == 0:
                    li.append(f.curso)
                    m.append(1)

            else:
                li.append(f.curso)
                m.append(1)
            pg = pg + 1

    fig1 = go.Figure(go.Bar(x=li, y=m))
    plot_div1 = plot(fig1, output_type='div', include_plotlyjs=False)
    response1 = plot_div1

    fig2 = go.Figure(go.Bar(x=['total de professores', 'graduação no município', 'pós-graduação no município'],
                            y=[len(professores), g, pg]))
    plot_div2 = plot(fig2, output_type='div', include_plotlyjs=False)
    response2 = plot_div2
    response_data = {}
    if request.POST.get('action') == 'post':
        nome = request.POST.get('nome')
        instgrad = request.POST.get('instgrad')
        cursograd = request.POST.get('cursograd')
        periodograd = request.POST.get('periodograd')
        iniciomagis = request.POST.get('iniciomagis')
        idescola = request.POST.get('escola')
        escola = Escola.objects.get(id=idescola)

        response_data['nome'] = nome
        response_data['tempo'] = iniciomagis
        response_data['magis'] = iniciomagis
        response_data['forma'] = cursograd

        professor = Privateprofessor.objects.create(
            nome=nome,
            ensinomedio="x",
            secretaria=secretaria1,
            inimagisterio=iniciomagis,
            escola=escola,
        )
        professor.save()
        response_data['id'] = professor.id

        Formacao.objects.create(
            instituicao=instgrad,
            curso=cursograd,
            periodo=periodograd,
            professor=professor,
            isGraduacao=True,
            isPosgraduacao=False

        )

        return JsonResponse(response_data)

    return render(request, 'usuario/secretaria.html',
                  {'professores': professores, 'response': response, 'response1': response1,
                   'response2': response2, 'form': form, 'escolas': escolas, 'form': form})


@login_required
@sensitive_post_parameters()
def cadastro_escola(request):
    perfil = Perfil.objects.get(user=request.user)
    secretaria1 = get_object_or_404(Secretaria, user=perfil)
    response_data = {}
    if request.POST.get('action') == 'post':
        nome = request.POST.get('nome')
        dependencia = request.POST.get('dependencia')
        uf = request.POST.get('uf')
        regiao = request.POST.get('regiao')
        nomedeusuario = request.POST.get('nomedeusuario')
        senha = request.POST.get('senha')

        response_data['nome'] = nome
        response_data['email'] = nomedeusuario
        response_data['municipio'] = secretaria1.municipio
        response_data['dependencia'] = dependencia

        user = User.objects.create_user(
            username=nomedeusuario,
            email=nomedeusuario,
            password=senha,

        )

        user.perfil.tipo = 2
        user.save()

        escola = Escola.objects.create(
            user=user.perfil,
            secretaria=secretaria1,
            nome=nome,
            dependencia=dependencia,
            municipio="x",
            cod_municipio="x",
            uf=uf,
            regiao=regiao,
        )
        escola.save()
        response_data["id"] = escola.id

        return JsonResponse(response_data)

    return render(request, 'usuario/secretaria.html')


def teste_nome(request):
    perfil = Perfil.objects.get(user=request.user)
    secretaria1 = get_object_or_404(Secretaria, user=perfil)
    response_data = {}
    if request.POST.get('action') == 'post':
        nome = request.POST.get('nome')
        try:
            escola = Escola.objects.get(nome=nome, secretaria=secretaria1)
        except:
            escola = None
        if escola:
            response_data["result"] = "True"
            response_data["nome"] = escola.nome
            response_data["dependencia"] = escola.dependencia
        else:
            response_data["result"] = "False"
    return JsonResponse(response_data)


def teste_user(request):
    perfil = Perfil.objects.get(user=request.user)
    secretaria1 = get_object_or_404(Secretaria, user=perfil)
    response_data = {}
    if request.POST.get('action') == 'post':
        nome = request.POST.get('nome')
        try:
            usuario = User.objects.filter(username=nome)
        except:
            usuario = None
        if usuario:
            response_data["result"] = "True"
        else:
            response_data["result"] = "False"
    return JsonResponse(response_data)


def teste_professor(request):
    perfil = Perfil.objects.get(user=request.user)
    try:
        secretaria1 = get_object_or_404(Secretaria, user=perfil)
    except:
        secretaria1 = get_object_or_404(Escola, user=perfil)
    response_data = {}
    if request.POST.get('action') == 'post':
        nome = request.POST.get('nome')
        try:
            usuario = Privateprofessor.objects.filter(nome=nome)
        except:
            usuario = None
        if usuario:
            response_data["result"] = "True"
        else:
            response_data["result"] = "False"
    return JsonResponse(response_data)


@login_required
@sensitive_post_parameters()
def get_professor(request, pk):
    response_data = {}

    if request.POST.get('action') == 'post':
        perfil = Perfil.objects.get(user=request.user)
        secretaria = get_object_or_404(Secretaria, user=perfil)
        if secretaria:
            id1 = request.POST.get('id')
            prof = Privateprofessor.objects.get(id=id1)
            response_data['nome'] = prof.nome
            response_data['ensinomedio'] = prof.ensinomedio
            response_data['iniciomagis'] = prof.inimagisterio
            return JsonResponse(response_data)

    return render(request, 'usuario/secretaria.html')


@login_required
@sensitive_post_parameters()
def get_professor1(request):
    response_data = {}

    if request.POST.get('action') == 'post':
        perfil = Perfil.objects.get(user=request.user)
        escola= get_object_or_404(Escola, user=perfil)
        if escola:
            id1 = request.POST.get('id')
            prof = Privateprofessor.objects.get(id=id1)
            response_data['nome'] = prof.nome
            response_data['ensinomedio'] = prof.ensinomedio
            response_data['iniciomagis'] = prof.inimagisterio
            return JsonResponse(response_data)

    return render(request, 'usuario/secretaria.html')


@login_required
@sensitive_post_parameters()
def get_escola(request):
    response_data = {}
    perfil = Perfil.objects.get(user=request.user)
    secretaria2 = get_object_or_404(Secretaria, user=perfil)
    if request.POST.get('action') == 'post':

        if secretaria2:
            id1 = int(request.POST.get('id'))
            escola = Escola.objects.get(id=id1)
            response_data['nome'] = escola.nome
            response_data['municipio'] = escola.municipio
            response_data['dependencia'] = escola.dependencia
            response_data['uf'] = escola.uf
            response_data['cod_municipio'] = escola.cod_municipio
            response_data['regiao'] = escola.regiao
            return JsonResponse(response_data)

    return render(request, 'usuario/secretaria.html')


@login_required
@sensitive_post_parameters()
def editar_professor(request):
    response_data = {}
    perfil = Perfil.objects.get(user=request.user)
    try:
        secretaria1 = get_object_or_404(Secretaria, user=perfil)
    except:
        secretaria1 = get_object_or_404(Escola, user=perfil)

    if request.POST.get('action') == 'post':
        if secretaria1:
            nome = request.POST.get('nome')
            ensinomedio = request.POST.get('ensinomedio')
            iniciomagis = request.POST.get('iniciomagis')
            id1 = request.POST.get('id')

            response_data['nome'] = nome
            response_data['tempo'] = iniciomagis
            response_data['magis'] = iniciomagis
            response_data['forma'] = iniciomagis

            professor = Privateprofessor.objects.get(id=id1)
            professor.nome = nome
            professor.ensinomedio = ensinomedio
            professor.inimagisterio = iniciomagis
            professor.save()
            return JsonResponse(response_data)


@login_required
@sensitive_post_parameters()
def desativar_professor(request, pk):
    if request.POST.get('action') == 'post':
        perfil = Perfil.objects.get(user=request.user)
        secretaria1 = get_object_or_404(Secretaria, user=perfil)
        if secretaria1:
            id1 = request.POST.get('id')

            professor = Privateprofessor.objects.get(id=id1)
            professor.isAtivo = False
            professor.save()
            response_data = 'sucesso'
            return JsonResponse(response_data, safe=False)


@login_required
@sensitive_post_parameters()
def desativar_professor1(request):
    if request.POST.get('action') == 'post':
        perfil = Perfil.objects.get(user=request.user)
        secretaria1 = get_object_or_404(Escola, user=perfil)
        if secretaria1:
            id1 = request.POST.get('id')

            professor = Privateprofessor.objects.get(id=id1)
            professor.isAtivo = False
            professor.save()
            response_data = 'sucesso'
            return JsonResponse(response_data, safe=False)


@login_required
def escola(request):
    from django.shortcuts import render
    import plotly.graph_objects as go
    from plotly.offline import plot

    perfil = get_object_or_404(Perfil, user=request.user)
    escola1 = get_object_or_404(Escola, user=perfil)
    professor = Escolaperfil.objects.filter(escola=escola1)
    privateprofessor = Privateprofessor.objects.filter(escola=escola1)
    fig = go.Figure(go.Bar(x=['total de professores cadastrados pela Secretaria'],
                           y=[len(privateprofessor)]))
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    fig1 = go.Figure(go.Bar(x=['total de usuários'],
                            y=[len(professor)]))
    plot_div1 = plot(fig1, output_type='div', include_plotlyjs=False)
    if request.POST.get('action') == 'post':
        nome = request.POST.get('nome')
        instgrad = request.POST.get('instgrad')
        cursograd = request.POST.get('cursograd')
        periodograd = request.POST.get('periodograd')
        iniciomagis = request.POST.get('iniciomagis')
        response_data = {'nome': nome, 'tempo': iniciomagis, 'magis': iniciomagis, 'forma': cursograd}

        professor = Privateprofessor.objects.create(
            nome=nome,
            ensinomedio="x",
            secretaria=escola1.secretaria,
            inimagisterio=iniciomagis,
            escola=escola1,
        )
        professor.save()
        response_data['id'] = professor.id

        Formacao.objects.create(
            instituicao=instgrad,
            curso=cursograd,
            periodo=periodograd,
            professor=professor,
            isGraduacao=True,
            isPosgraduacao=False

        )

        return JsonResponse(response_data)

    return render(request, 'usuario/page22.html', {'professores': privateprofessor, 'g1': plot_div, 'g2': plot_div1,
                                                   'escola': escola1})


@login_required
@sensitive_post_parameters()
def validaescola(request):
    if request.POST.get('action') == 'post':
        perfil = get_object_or_404(Perfil, user=request.user)
        escola1 = get_object_or_404(Escola, user=perfil)
        if escola1:
            id1 = request.POST.get('id')
            escolaperfil = Escolaperfil.objects.get(id=id1)
            if escolaperfil.isAceito == False:
                escolaperfil.isAceito = True
                escolaperfil.save()
                response_data = 'sucesso'
                return JsonResponse(response_data, safe=False)
            else:
                escolaperfil.isAceito = False
                escolaperfil.save()
                response_data = 'sucesso'
                return JsonResponse(response_data, safe=False)
    return render(request)


@login_required
@sensitive_post_parameters()
def editar_escola(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    escola1 = get_object_or_404(Escola, user=perfil)
    response_data = {}
    if request.POST.get('action') == 'post':
        nome = request.POST.get('nome')
        municipio = request.POST.get('municipio')
        cod_municipio = request.POST.get('cod_municipio')
        dependencia = request.POST.get('dependencia')
        uf = request.POST.get('uf')
        regiao = request.POST.get('regiao')

        response_data['nome'] = nome
        response_data['municipio'] = municipio
        response_data['dependencia'] = dependencia
        escola1.nome = nome
        escola1.municipio = municipio
        escola1.cod_municipio = cod_municipio
        escola1.dependencia = dependencia
        escola1.uf = uf
        escola1.regiao = regiao
        escola1.save()

        return JsonResponse(response_data)

    return render(request, 'usuario/page2.html')


@login_required
@sensitive_post_parameters()
def editarescolas(request):
    response_data = {}
    if request.POST.get('action') == 'post':
        id1 = request.POST.get('id')
        nome = request.POST.get('nome')
        dependencia = request.POST.get('dependencia')
        uf = request.POST.get('uf')
        regiao = request.POST.get('regiao')
        escola1 = Escola.objects.get(id=id1)

        response_data['nome'] = nome
        response_data['dependencia'] = dependencia
        escola1.nome = nome

        escola1.dependencia = dependencia
        escola1.uf = uf
        escola1.regiao = regiao
        escola1.save()

        return JsonResponse(response_data)


@login_required
@sensitive_post_parameters()
def professores_escola(request, pk):
    escola = Escola.objects.get(id=pk)
    professores = Privateprofessor.objects.filter(escola=escola)
    return render(request, "usuario/table_prof.html", {'professores': professores, 'escola': escola})


@login_required
@sensitive_post_parameters()
def professorpage(request):
    user = request.user
    perfil = Perfil.objects.get(user=user)
    perfil_user = get_object_or_404(Professor, user=perfil)
    escolas = Escola.objects.all()
    minhas_escolas = Escolaperfil.objects.select_related('escola').filter(professor=perfil_user)
    perguntas = Pergunta.objects.all()
    form = ProfessorForm(request.POST or None, request.FILES or None, instance=perfil_user)
    if request.method == 'POST':

        if form.is_valid():
            save = form
            save.save()
            return render(request, 'usuario/page32.html', {'perfil': perfil_user, 'escolas': escolas,
                                                           'minhas_escolas': minhas_escolas,
                                                           'perguntas': perguntas, 'form': form})

    return render(request, 'usuario/page32.html', {'perfil': perfil_user, 'escolas': escolas,
                                                   'minhas_escolas': minhas_escolas,
                                                   'perguntas': perguntas, 'form': form})


@login_required
@sensitive_post_parameters()
def escolaperfil(request):
    if request.POST.get('action') == 'post':
        user = User.objects.get(id=request.user.id)
        perfil = Perfil.objects.get(user=user)
        professor = get_object_or_404(Professor, user=perfil)
        pk = request.POST.get('escola')
        escola1 = Escola.objects.get(id=pk)
        escolaperfil1 = Escolaperfil(professor=professor, escola=escola1, isAceito=False)
        escolaperfil1.save()
        response_data = 'sucesso'
        return JsonResponse(response_data, safe=False)


@login_required
def responderd(request, pk):
    pergunta = Pergunta.objects.get(id=pk)
    user = get_object_or_404(User, id=request.user.id)
    if request.method == "POST":
        pergunta = Pergunta.objects.get(id=pk)
        resposta = Perguntaresposta.objects.create(id_usuario=user, id_questao=pergunta, resposta=request.POST['resposta'])
        resposta.save()
        return redirect('perfil:perguntas')
    return render(request, 'usuario/responder2.html', {'pergunta': pergunta})


@login_required
@sensitive_post_parameters()
def respondera(request, pk):
    pergunta = Pergunta.objects.get(id=pk)
    user = get_object_or_404(User, id=request.user.id)
    alternativas = Alternativa.objects.filter(id_questao=pergunta)
    if request.method == "POST":
        resposta = Perguntaresposta.objects.create(id_usuario=user, id_questao=pergunta, alternativa=request.POST['alternativa'])
        resposta.save()
        return redirect('perfil:perguntas')
    return render(request, 'usuario/respondera2.html', {'pergunta': pergunta, 'alternativas': alternativas})


@login_required
def perguntas(request):
    user = User.objects.get(id = request.user.id)
    respondidas = Perguntaresposta.objects.select_related('id_questao').filter(id_usuario=user)
    aux = []
    for r in respondidas:
        aux.append(r.id_questao.pk)
    perguntas1 = Pergunta.objects.exclude(pk__in=aux)
    quantidade = len(perguntas1)
    return render(request, 'perguntas/perguntas2.html', {'perguntas': perguntas1, 'quantidade': quantidade})


@login_required
@sensitive_post_parameters()
def administrador(request):
    user = User.objects.get(id=request.user.id)
    perfil = Perfil.objects.get(user=user)
    ativo = Ativar.objects.last()
    if ativo.ativo:
        ativado = "Ativado"
    else:
        ativado = "Desativado"
    if user.is_superuser:
        perguntas = Pergunta.objects.all()
        form = NoticiaForm(request.POST or None, request.FILES or None)
        return render(request, 'usuario/adm.html', {'form': form, 'perguntas': perguntas, 'ativo': ativado})
    else:
        return render(request, 'usuario/404.html')


@login_required
@sensitive_post_parameters()
def novapergunta(request):
    response_data = {}
    user = User.objects.get(id=request.user.id)
    perfil = Perfil.objects.get(user=user)
    if user.is_superuser:
        if request.POST.get('action') == 'post':

            user = User.objects.get(id=request.user.id)
            nome = user.username
            perfil = Perfil.objects.get(user=user)
            questionario = request.POST.get('questionario')
            questao = request.POST.get('questao')
            tipo = request.POST.get('selectedValue')
            if tipo == "1":
                pergunta = Pergunta.objects.create(questionario=questionario, questao=questao, isDissertativa=True,
                                                   isAlternativa=False,
                                                   autor=nome)
                pergunta.save()
                response_data['tipo'] = tipo
                response_data['pergunta'] = questao
                response_data['id'] = pergunta.id
            if tipo == "2":
                pergunta = Pergunta.objects.create(questionario=questionario, questao=questao, isDissertativa=True,
                                                   isAlternativa=False,
                                                   autor=user.username)
                pergunta.save()
                response_data['tipo'] = tipo
                response_data['pergunta'] = questao
                response_data['id'] = pergunta.id
            return JsonResponse(response_data)
    else:
        return render(request, 'usuario/404.html')


@login_required
@sensitive_post_parameters()
def novaalternatica(request):
    response_data = {}
    user = User.objects.get(id=request.user.id)
    perfil = Perfil.objects.get(user=user)
    if user.is_superuser:

        if request.POST.get('action') == 'post':
            id1 = request.POST.get('pk')
            pergunta = Pergunta.objects.get(id=id1)
            texto = request.POST.get('texto')
            alternativa = Alternativa.objects.create(
                id_questao=pergunta,
                alternativa=texto,
                numero=1
            )
            alternativa.save()
            if alternativa:
                response_data['sucesso'] = True
            else:
                response_data['sucesso'] = False

            return JsonResponse(response_data)


@login_required
@sensitive_post_parameters()
def postar(request):
    user = User.objects.get(id=request.user.id)
    perfil = Perfil.objects.get(user=user)
    if user.is_superuser:
        noticias = Noticia.objects.all()
        if request.method == 'POST':
            form3 = NoticiaForm(request.POST or None, request.FILES or None)
            if form3.is_valid():
                form3.save(commit=True)

                return redirect('noticias:home')
        form3 = NoticiaForm()
        return render(request, 'usuario/adm1.html', {'form3': form3, 'noticias': noticias})


@login_required
@sensitive_post_parameters()
def desativar_pergunta(request):
    user = User.objects.get(id=request.user.id)
    perfil = Perfil.objects.get(user=user)
    if user.is_superuser:
        if request.POST.get('action') == 'post':
            id1 = request.POST.get('id')

            pergunta = Pergunta.objects.get(id=id1)
            pergunta.delete()
            response_data = 'sucesso'
            return JsonResponse(response_data, safe=False)


@login_required
@sensitive_post_parameters()
def desativar_postagem(request):
    user = User.objects.get(id=request.user.id)
    perfil = Perfil.objects.get(user=user)
    if user.is_superuser:
        if request.POST.get('action') == 'post':
            id1 = request.POST.get('id')

            noticia = Noticia.objects.get(id=id1)
            noticia.delete()
            response_data = 'sucesso'
            return JsonResponse(response_data, safe=False)


@login_required
@sensitive_post_parameters()
def desativarescola(request):
    user = User.objects.get(id=request.user.id)
    perfil = Perfil.objects.get(user=user)
    if user.is_superuser:
        if request.POST.get('action') == 'post':
            id1 = request.POST.get('id')
            escola = Escola.objects.get(id=id1)
            escola.delete()
            response_data = 'sucesso'
            return JsonResponse(response_data, safe=False)


@login_required
@sensitive_post_parameters()
def ativaruso(request):
    perfil = Perfil.objects.get(user=request.user)
    response_data = {}
    if request.POST.get('action') == 'post':
        tipo = request.POST.get('tipo')
        if tipo == "1":
            ativo = Ativar.objects.create(ativo=True)
        else:
            ativo = Ativar.objects.create(ativo=False)
        ativo.save()
        if ativo:
            response_data["result"] = "True"
        else:
            response_data["result"] = "False"
    return JsonResponse(response_data)

