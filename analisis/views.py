# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import statistics as st

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
    # Elimina valores NAN
    area_selvatica_values_no_nan = area_selvatica_pais.values[~pd.isnull(area_selvatica_pais.values)]

    maximo_area_selvatica_pais = area_selvatica_values_no_nan.max()
    minimo_area_selvatica_pais = area_selvatica_values_no_nan.min()
    mediana = st.median(area_selvatica_values_no_nan)
    desviacion_estandar = np.std(area_selvatica_values_no_nan)

    # Grafica area selvatica
    plt.plot(area_selvatica_pais.index, area_selvatica_pais.values, label='Área selvatica')
    # plt.plot(x, x ** 2, label='quadratic')
    # plt.plot(x, x ** 3, label='cubic')

    plt.xlabel('Año')
    plt.ylabel('Área selvatica (Km2)')

    plt.title("Historico área selvatica %s", request.POST['Pais'])

    plt.legend()

    plt.savefig('C:/Users/jgr70/Documents/diplomado/analisis/static/analisis/images/foo.png')

    json_area_selvatica = area_selvatica_pais.to_json(orient='split')
    return HttpResponse(json_area_selvatica)
    '''datos_pandas = pd.DataFrame(area_selvatica_pais)
    maximo_area_selvatica_pais = datos_pandas.max()
    json_area_selvatica = area_selvatica_pais.to_json(orient='split')

    return render(request, 'analisis/index.html', {
        'Pais': request.POST['Pais'],
        'area_selvatica_json': json_area_selvatica,
        'poblacion_urbana_json': pobliacion_urbana.loc[request.POST['Pais'], '1990':'2017'],
        'gases_efecto_invernadero_json': gases_efecto_invernadero.loc[request.POST['Pais'], '1990':'2017'],
        'maximo_area_selvatica_pais': maximo_area_selvatica_pais,
    })'''