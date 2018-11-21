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

def estadisticos(values_no_nan):
    est = {
        'maximo': values_no_nan.max(),
        'minimo': values_no_nan.min(),
        'mediana': st.median(values_no_nan),
        'desviacion_estandar': np.std(values_no_nan)
    }
    return est

def graficar(label_graf, label_x, label_y, titulo, guardar_como, datos, pais):

    # http://kitchingroup.cheme.cmu.edu/blog/2013/09/13/Plotting-two-datasets-with-very-different-scales/
    plt.figure()
    f, axes = plt.subplots(3, 1, constrained_layout=True)

    size_layouts = 9

    datos_1990_2000 = datos.loc[pais, '1990':'2000']
    axes[0].plot(datos_1990_2000.index, datos_1990_2000.values)
    axes[0].set_ylabel(label_y, color='r', size=size_layouts)
    axes[0].get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    axes[0].set_xlabel(label_x, color='r', size=size_layouts)
    del datos_1990_2000

    datos_2000_2010 = datos.loc[pais, '2000':'2010']
    axes[1].plot(datos_2000_2010.index, datos_2000_2010.values)
    axes[1].set_ylabel(label_y, color='r', size=size_layouts)
    axes[1].get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    axes[1].set_xlabel(label_x, color='r', size=size_layouts)
    del datos_2000_2010

    datos_2010_2017 = datos.loc[pais, '2010':'2017']
    axes[2].plot(datos_2010_2017.index, datos_2010_2017.values)
    axes[2].set_ylabel(label_y, color='r', size=size_layouts)
    axes[2].get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    axes[2 ].set_xlabel(label_x, color='r', size=size_layouts)

    del datos_2010_2017

    # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html
    axes[0].legend([label_graf])
    axes[1].legend([label_graf])
    axes[2].legend([label_graf])

    # https://matplotlib.org/gallery/subplots_axes_and_figures/figure_title.html
    f.suptitle(titulo, fontsize=16)

    plt.savefig(guardar_como)

    return ''

def graficar_deforestacion(indices, datos_dentro, datos_fuera, guardar_como):

    # http://kitchingroup.cheme.cmu.edu/blog/2013/09/13/Plotting-two-datasets-with-very-different-scales/

    # http://kitchingroup.cheme.cmu.edu/blog/2013/09/13/Plotting-two-datasets-with-very-different-scales/
    plt.figure()
    f, axes = plt.subplots(2, 1, constrained_layout=True)

    size_layouts = 9

    axes[0].plot(indices, datos_dentro)
    axes[0].set_ylabel("Dentro", color='r', size=size_layouts)
    axes[0].get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    axes[0].set_xlabel(label_x, color='r', size=size_layouts)

    axes[1].plot(indices, datos_fuera)
    axes[1].set_ylabel("Fuera", color='r', size=size_layouts)
    axes[1].get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    axes[1].set_xlabel(label_x, color='r', size=size_layouts)

    # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html
    axes[0].legend(["% Deforestación"])
    axes[1].legend(["% Deforestación"])

    # https://matplotlib.org/gallery/subplots_axes_and_figures/figure_title.html
    f.suptitle("Deforestación en los parques naturales", fontsize=16)

    plt.savefig(guardar_como)
    return ''

# Create your views here.
def index(request):
    # return HttpResponse("You're looking at question %s.")
    if request.POST['Pais'] == '':
        return HttpResponseRedirect(reverse('mapas:index'))

    # MacOS
    ruta = "/Users/jgarcia/diplomado/analisis/static/analisis/"
    # Windows
    # ruta = "C:/Users/jgr70/Documents/diplomado/analisis/static/analisis/"

    area_selvatica = volcar(ruta+'files/area_selvatica.csv', ',')
    poblacion_urbana = volcar(ruta+'files/poblacion_urbana.csv', ',')
    gases_efecto_invernadero = volcar(ruta+'files/gases_efecto_invernadero.csv', ',')
    deforestacion = volcar(ruta + 'files/deforestacion.csv', ',')

    # Inicio área selvatica

    '''area_selvatica_pais = area_selvatica.loc[request.POST['Pais'], '1990':'2017']
    # Elimina valores NAN
    area_selvatica_values_no_nan = area_selvatica_pais.values[~pd.isnull(area_selvatica_pais.values)]
    estadistica_area_selvatica = estadisticos(area_selvatica_values_no_nan)
    
    png_areasel = 'area_selvatica_'+request.POST['Pais']+'.png'

    graficar('Área selvatica (Km2)',
        'Año',
        'Km2',
        'Historico área selvatica '+request.POST['Pais'],
        ruta + 'images/'+png_areasel,
        area_selvatica,
        request.POST['Pais']
    )

    # Fin área selvatica

    # Inicio población urbana

    poblacion_urbana_pais = poblacion_urbana.loc[request.POST['Pais'], '1990':'2017']
    # Elimina valores NAN
    poblacion_urbana_values_no_nan = poblacion_urbana_pais.values[~pd.isnull(poblacion_urbana_pais.values)]
    estadistica_poblacion_urbana = estadisticos(poblacion_urbana_values_no_nan)

    png_poburb = 'poblacion_urbana_' + request.POST['Pais'] + '.png'

    graficar('Población urbana',
         'Año',
         'Habitantes',
         'Historico población urbana ' + request.POST['Pais'],
         ruta + 'images/' + png_poburb,
         poblacion_urbana,
         request.POST['Pais']
    )

    # Fin población urbana

    # Inicio gases de efecto invernadero

    gases_efecto_invernadero_pais = gases_efecto_invernadero.loc[request.POST['Pais'], '1990':'2017']
    # Elimina valores NAN
    gases_efecto_invernadero_pais_no_nan = gases_efecto_invernadero_pais.values[~pd.isnull(gases_efecto_invernadero_pais.values)]
    estadistica_gases_efecto_invernadero = estadisticos(gases_efecto_invernadero_pais_no_nan)

    png_gases = 'gases_efecto_invernadero_' + request.POST['Pais'] + '.png'

    graficar('Gases CO2',
         'Año',
         'CO2',
         'Historico gases efecto invernadero ' + request.POST['Pais'],
         ruta + 'images/' + png_gases,
         gases_efecto_invernadero,
         request.POST['Pais']
    )'''

    # Fin gases de efecto invernadero

    # Inicio deforestación

    deforestacion_pais = deforestacion.loc[request.POST['Pais'], 'year':'inside (up to 10 km from park boundary) deforestation rate in %']
    grupo_por_anio = deforestacion_pais.groupby(['year']).mean()
    fuera_de_10_km = grupo_por_anio.values[:,0]
    dentro_de_10_km = grupo_por_anio.values[:, 1]

    png_deforestacion = 'deforestacion_' + request.POST['Pais'] + '.png'

    # graficar_deforestacion(deforestacion_pais.index, dentro_de_10_km, fuera_de_10_km, ruta + 'images/' + png_deforestacion)

    # Fin deforestación


    deforestacion_pais_json_1 = grupo_por_anio.to_json(orient='split')
    deforestacion_pais_json = pd.Series(fuera_de_10_km).to_json(orient='split')
    deforestacion_pais_json_2 = pd.Series(dentro_de_10_km).to_json(orient='split')
    return HttpResponse(grupo_por_anio['index']+"<br />"+deforestacion_pais_json+"<br />"+deforestacion_pais_json_2)
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