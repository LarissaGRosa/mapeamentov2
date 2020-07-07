from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters

from mysite.settings import EMAIL_HOST_USER
from perguntas.models import Pergunta, Alternativa, Perguntaresposta
from resultado.models import Noticia
from usuario.models import Formacao, Secretaria, Escola, Privateprofessor


@sensitive_post_parameters()
def noticia(request):
    noticias = Noticia.objects.last()
    if request.POST.get('action') == 'post':
        nome = str(request.POST.get('nome'))
        sobrenome = str(request.POST.get('sobrenome'))
        email = str(request.POST.get('email'))
        mensagem = str(request.POST.get('mensagem'))
        send_mail(nome+sobrenome,
                  mensagem, EMAIL_HOST_USER, [email], fail_silently=False)
        response_data = 'sucesso'
        return JsonResponse(response_data, safe=False)
    return render(request, 'resultado/index2.html', {'noticias': noticias})


def posts(request):
    noticias = Noticia.objects.all()
    return render(request, 'resultado/page52.html', {'noticias': noticias})


def estatisticas(request):
    from django.shortcuts import render
    import plotly.graph_objects as go
    from plotly.offline import plot
    import plotly.graph_objs as go1
    perguntas = Pergunta.objects.filter(isAlternativa=True)

    response = []
    for pergunta in perguntas:
        alternativas = Alternativa.objects.filter(id_questao=pergunta)
        x = []
        y = []
        for alternativa in alternativas:
            x.append(alternativa.alternativa)
            respostas = Perguntaresposta.objects.filter(alternativa=alternativa.id)
            y.append(len(respostas))
        fig = go.Figure(data=[go.Bar(x=x, y=y)],
                        layout_title_text=pergunta.questao)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        response.append(plot_div)

    secretarias = Secretaria.objects.all()
    a = []
    b = []
    c = []
    for secretaria in secretarias:
        escolas = Escola.objects.filter(secretaria=secretaria)
        professor = Privateprofessor.objects.filter(secretaria=secretaria)
        a.append(secretaria.municipio)
        b.append(len(escolas))
        c.append(len(professor))
    a.append('Total')
    b.append(len(Escola.objects.all()))
    fig1 = go.Figure(data=[go.Bar(x=a, y=b)],
                     layout_title_text='Relação de escolas por município')
    plot_div1 = plot(fig1, output_type='div', include_plotlyjs=False)
    rel1= plot_div1
    c.append(len(Privateprofessor.objects.all()))
    fig2 = go.Figure(data=[go.Bar(x=a, y=c)],
                     layout_title_text='Relação de professores por município')
    plot_div2 = plot(fig2, output_type='div', include_plotlyjs=False)
    rel2 = plot_div2

    professores = Privateprofessor.objects.all()
    d = []
    e = []
    g = 0
    for p in professores:
        forma = Formacao.objects.filter(professor=p, isGraduacao=True)
        for f in forma:
            z = 0
            if len(d) > 0:
                for xx in d:
                    if f == xx:
                        e[d.index[xx]] = e[d.index[xx]] + 1
                        z = z + 1
                if z == 0:
                    d.append(f.curso)
                    e.append(1)

            else:
                d.append(f.curso)
                e.append(1)
            g = g + 1
    fig3 = go.Figure(data=[go.Bar(x=d, y=e)],
                     layout_title_text='Relação de áreas de graduação dos professores')
    plot_div3 = plot(fig3, output_type='div', include_plotlyjs=False)
    rel3 = plot_div3

    h = []
    i = []
    pg = 0
    for p in professores:
        forma = Formacao.objects.filter(professor=p, isPosgraduacao=True)
        for f in forma:
            z = 0
            if len(h) > 0:
                for xx in h:
                    if f == xx:
                        i[h.index[xx]] = i[h.index[xx]] + 1
                        z = z + 1
                if z == 0:
                    h.append(f.curso)
                    i.append(1)

            else:
                h.append(f.curso)
                i.append(1)
            pg = pg + 1
    fig4 = go.Figure(data=[go.Bar(x=h, y=i)],
                     layout_title_text='Relação de áreas de pós-graduação dos professores')
    plot_div4 = plot(fig4, output_type='div', include_plotlyjs=False)
    rel4 = plot_div4

    return render(request, 'resultado/page42.html', {'resultados': response, 'r1': rel1, 'r2': rel2, 'r3': rel3,
                                                    'r4': rel4})


def get_noticias(request):
    response_data = {}

    if request.POST.get('action') == 'post':
        id1 = request.POST.get('id')
        news = Noticia.objects.get(id=id1)
        response_data['titulo'] = news.titulo
        response_data['texto'] = news.texto
        response_data['autor'] = news.autor
        response_data['data'] = news.data_publi
        return JsonResponse(response_data)

    return render(request, 'resultado/page5.html')


