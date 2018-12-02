# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
def tecnologias(request):

    return render(request, 'acerca/tecnologias.html', {
        'titulo': 'Tecnologias utilizadas'
    })

def componentes(request):

    return render(request, 'acerca/componentes.html', {
        'titulo': 'Diagrama de componentes'
    })

def negocio(request):

    return render(request, 'acerca/negocio.html', {
        'titulo': 'Modelo de negocio CANVAS'
    })