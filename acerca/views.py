# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
def tecnologias(request):

    return render(request, 'acerca/tecnologias.html', {
        'titulo': 'Tecnologias utilizadas'
    })

def despliegue(request):

    return render(request, 'acerca/despliegue.html', {
        'titulo': 'Despliegue'
    })

def negocio(request):

    return render(request, 'acerca/negocio.html', {
        'titulo': 'Modelo de negocio CANVAS'
    })