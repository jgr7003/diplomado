# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

import pandas as pd

def volcar(archivo, delimitador):
    datos = pd.read_csv(archivo,delimiter=delimitador,decimal=".",index_col=0)
    return datos

# Create your views here.
def index(request):
    # return HttpResponse("You're looking at question %s.")
    if request.POST['Pais'] == '':
        return HttpResponseRedirect(reverse('mapas:index'))

    area_selvatica = volcar('C:/Users/jgr70/Documents/diplomado/analisis/static/analisis/files/area_selvatica.csv', ',')
    pobliacion_urbana = volcar('C:/Users/jgr70/Documents/diplomado/analisis/static/analisis/files/poblacion_urbana.csv', ',')
    gases_efecto_invernadero = volcar('C:/Users/jgr70/Documents/diplomado/analisis/static/analisis/files/gases_efecto_invernadero.csv', ',')

    area_selvatica_pais = area_selvatica.loc[request.POST['Pais'], '1990':'2017']
    datos_pandas = pd.DataFrame(area_selvatica_pais)
    maximo_area_selvatica_pais = datos_pandas.max()
    json_area_selvatica = area_selvatica_pais.to_json(orient='split')

    return render(request, 'analisis/index.html', {
        'Pais': request.POST['Pais'],
        'AreaSelvatica': json_area_selvatica,
        'PoblacionUrbana': pobliacion_urbana.loc[request.POST['Pais'], '1990':'2017'],
        'Gases': gases_efecto_invernadero.loc[request.POST['Pais'], '1990':'2017'],
        'maximo_area_selvatica_pais': maximo_area_selvatica_pais,
    })