from django.conf.urls import url

from . import views

app_name = 'acerca'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'tecnologias/$', views.resultados, name='tecnologias'),
    url(r'despliegue/$', views.resultados, name='despliegue'),
    url(r'negocio/$', views.resultados, name='negocio'),
]