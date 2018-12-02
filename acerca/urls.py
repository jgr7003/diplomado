from django.conf.urls import url

from . import views

app_name = 'acerca'

urlpatterns = [
    url(r'tecnologias/$', views.tecnologias, name='tecnologias'),
    url(r'componentes/$', views.componentes, name='componentes'),
    url(r'negocio/$', views.negocio, name='negocio'),
]