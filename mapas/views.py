# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

import pandas as pd
import numpy as np
import json
import simplejson

def volcar(archivo, delimitador):
    datos = pd.read_csv(archivo,delimiter=delimitador,decimal=".",index_col=0)
    return datos

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):             return [obj.real, obj.imag]
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

# Create your views here.
def index(request):

    # MacOS
    ruta = "/Users/jgarcia/diplomado/analisis/static/analisis/"
    # Windows
    # ruta = "C:/Users/jgr70/Documents/diplomado/analisis/static/analisis/"

    area_selvatica = volcar(ruta + 'files/area_selvatica.csv', ',')
    poblacion_urbana = volcar(ruta + 'files/poblacion_urbana.csv', ',')
    gases_efecto_invernadero = volcar(ruta + 'files/gases_efecto_invernadero.csv', ',')

    list_idx_selvatica = area_selvatica.index.tolist()
    list_idx_poblacion = poblacion_urbana.index.tolist()
    list_idx_gases = gases_efecto_invernadero.index.tolist()

    json_paises_area_selvatica = json.dumps(list_idx_selvatica,
        separators=(',',':')
    )

    json_poblacion_urbana = simplejson.dumps(list_idx_poblacion,
        default=lambda a: "[%s,%s]" % (str(type(a)), a.pk)
    )

    json_gases_efecto_invernadero = simplejson.dumps(list_idx_gases,
        default=lambda a: "[%s,%s]" % (str(type(a)), a.pk)
    )

    return render(request, 'mapas/index.html', {
        'titulo': 'Dashboard - Selección de país',
        'json_paises_area_selvatica': json_paises_area_selvatica,
        'json_poblacion_urbana': json_poblacion_urbana,
        'json_gases_efecto_invernadero': json_gases_efecto_invernadero
    })