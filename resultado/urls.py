from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from . import views
app_name = 'noticias'

urlpatterns = [
    path('', views.noticia, name='home'),
    path('/estatisticas', views.estatisticas, name='estatisticas'),
    path('posts', views.posts, name='posts'),
    path('getn', views.get_noticias, name='getnoticias')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)