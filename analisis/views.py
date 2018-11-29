# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import statistics as st
import collections

def volcar(archivo, delimitador):
    datos = pd.read_csv(archivo,delimiter=delimitador,decimal=".",index_col=0)
    return datos

def estadisticos(values_no_nan):
    est = {
        'maximo': values_no_nan.max(),
        'minimo': values_no_nan.min(),
        'conteo': collections.Counter(values_no_nan),
        'mediana': st.median(values_no_nan),
        'media': st.mean(values_no_nan),
        'desviacion_estandar': np.std(values_no_nan),
        'varianza': np.var(values_no_nan),

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

    axes[0].grid(True)
    axes[1].grid(True)
    axes[2].grid(True)

    # https://matplotlib.org/gallery/subplots_axes_and_figures/figure_title.html
    f.suptitle(titulo, fontsize=16)

    plt.savefig(guardar_como)

    return ''

def graficar_deforestacion(indices, datos_dentro, datos_fuera, guardar_como):

    # http://kitchingroup.cheme.cmu.edu/blog/2013/09/13/Plotting-two-datasets-with-very-different-scales/
    plt.figure()
    f, axes = plt.subplots(2, 1, constrained_layout=True)

    size_layouts = 9

    axes[0].plot(indices, datos_dentro)
    axes[0].set_ylabel("Dentro 10 Km", color='r', size=size_layouts)
    axes[0].get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    axes[0].set_xlabel("Año", color='r', size=size_layouts)

    axes[1].plot(indices, datos_fuera)
    axes[1].set_ylabel("Fuera 10 Km", color='r', size=size_layouts)
    axes[1].get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    axes[1].set_xlabel("Año", color='r', size=size_layouts)

    # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html
    axes[0].legend(["% Deforestación"])
    axes[1].legend(["% Deforestación"])

    axes[0].grid(True)
    axes[1].grid(True)

    # https://matplotlib.org/gallery/subplots_axes_and_figures/figure_title.html
    f.suptitle("Deforestación limites de los parques naturales", fontsize=16)

    plt.savefig(guardar_como)
    return ''

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

def graficar_multiple(selvatica, gases, poblacion, pais, guardar_como, desde, hasta):

    fig, host = plt.subplots()
    fig.subplots_adjust(right=0.75)

    par1 = host.twinx()
    par2 = host.twinx()
    # par3 = host.twinx()

    # Offset the right spine of par2.  The ticks and label have already been
    # placed on the right by twinx above.
    par2.spines["right"].set_position(("axes", 1.2))
    # par2.spines["left"].set_position(("axes", 1.2))
    # Having been created by twinx, par2 has its frame off, so the line of its
    # detached spine is invisible.  First, activate the frame but make the patch
    # and spines invisible.
    make_patch_spines_invisible(par2)
    # Second, show the right spine.
    par2.spines["right"].set_visible(True)

    areselva_1990_2000 = selvatica.loc[pais, desde:hasta]
    gases_1990_2000 = gases.loc[pais, desde:hasta]
    poblacion_1990_2000 = poblacion.loc[pais, desde:hasta]

    p1, = host.plot(areselva_1990_2000.index, areselva_1990_2000.values, "g-", label="Área selvatica")
    p2, = par1.plot(gases_1990_2000.index, gases_1990_2000.values, "r-", label="Gases efecto invernadero")
    p3, = par2.plot(poblacion_1990_2000.index, poblacion_1990_2000.values, "b-", label="Población urbana")

    host.set_xlabel("Año")
    host.set_ylabel("Km2")
    par1.set_ylabel("CO")
    par2.set_ylabel("Millones habitantes")

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())

    tkw = dict(size=4, width=1.5)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)

    lines = [p1, p2, p3]

    host.legend(lines, [l.get_label() for l in lines])

    plt.grid(True)

    plt.savefig(guardar_como)

    return ''

# Create your views here.
def index(request):
    # return HttpResponse("You're looking at question %s.")
    if request.POST['Pais'] == '':
        return HttpResponseRedirect(reverse('mapas:index'))

    # MacOS
    # ruta = "/Users/jgarcia/diplomado/analisis/static/analisis/"
    # Windows
    ruta = "C:/Users/jgr70/Documents/diplomado/analisis/static/analisis/"

    area_selvatica = volcar(ruta+'files/area_selvatica.csv', ',')
    poblacion_urbana = volcar(ruta+'files/poblacion_urbana.csv', ',')
    gases_efecto_invernadero = volcar(ruta+'files/gases_efecto_invernadero.csv', ',')
    deforestacion = volcar(ruta + 'files/deforestacion.csv', ',')

    # Inicio área selvatica

    area_selvatica_pais = area_selvatica.loc[request.POST['Pais'], '1990':'2017']
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
    )

    # Fin gases de efecto invernadero

    # Inicio deforestación

    PaisDeforestacion = request.POST['Pais']
    if(request.POST['Pais'] == 'Brasil'):
        PaisDeforestacion = 'Brazil'

    try:
        deforestacion_pais = deforestacion.loc[PaisDeforestacion,
                             'year':'inside (up to 10 km from park boundary) deforestation rate in %']
        grupo_por_anio = deforestacion_pais.groupby(['year']).mean()
        fuera_de_10_km = grupo_por_anio.values[:, 0]
        dentro_de_10_km = grupo_por_anio.values[:, 1]

        png_deforestacion = 'deforestacion_' + request.POST['Pais'] + '.png'

        grupo_por_anio_no_nan = grupo_por_anio.values[~pd.isnull(grupo_por_anio.values)]

        estadistica_deforestacion = estadisticos(grupo_por_anio_no_nan)

        graficar_deforestacion(grupo_por_anio.index, dentro_de_10_km, fuera_de_10_km, ruta + 'images/' + png_deforestacion)

    except KeyError:
        png_deforestacion = ''



    # Fin deforestación

    # Inicio comparativo

    png_comparativo_1990_2000 = 'comparativo_' + request.POST['Pais'] + '_1990_2000.png'
    graficar_multiple(
        area_selvatica,
        gases_efecto_invernadero,
        poblacion_urbana,
        request.POST['Pais'],
        ruta + 'images/' + png_comparativo_1990_2000,
        '1990',
        '2000'
    )

    png_comparativo_2000_2010 = 'comparativo_' + request.POST['Pais'] + '_2000_2010.png'
    graficar_multiple(
        area_selvatica,
        gases_efecto_invernadero,
        poblacion_urbana,
        request.POST['Pais'],
        ruta + 'images/' + png_comparativo_2000_2010,
        '2000',
        '2010'
    )

    png_comparativo_2010_2017 = 'comparativo_' + request.POST['Pais'] + '_2010_2017.png'
    graficar_multiple(
        area_selvatica,
        gases_efecto_invernadero,
        poblacion_urbana,
        request.POST['Pais'],
        ruta + 'images/' + png_comparativo_2010_2017,
        '2010',
        '2017'
    )

    request.session['pais'] = request.POST['Pais']
    request.session['area_selvatica'] = png_areasel
    request.session['estadistica_area_selvatica'] = estadistica_area_selvatica
    request.session['poblacion_urbana'] = png_poburb
    request.session['estadistica_poblacion_urbana'] = estadistica_poblacion_urbana
    request.session['gases_efecto_invernadero'] = png_gases
    request.session['estadistica_gases_efecto_invernadero'] = estadistica_gases_efecto_invernadero
    request.session['deforestacion'] = png_deforestacion
    request.session['estadistica_deforestacion'] = estadistica_deforestacion
    request.session['comparativo_1990_2000'] = png_comparativo_1990_2000
    request.session['comparativo_2000_2010'] = png_comparativo_2000_2010
    request.session['comparativo_2010_2017'] = png_comparativo_2010_2017

    '''request.session['area_selvatica'] = 'area_selvatica_'+request.POST['Pais']+'.png'
    request.session['poblacion_urbana'] = 'poblacion_urbana_' + request.POST['Pais'] + '.png'
    request.session['gases_efecto_invernadero'] = 'gases_efecto_invernadero_' + request.POST['Pais'] + '.png'
    request.session['deforestacion'] = 'deforestacion_' + request.POST['Pais'] + '.png'''

    # Fin comparativo
    return HttpResponseRedirect('/analisis/resultados')

def resultados(request):

    return render(request, 'analisis/resultados.html', {
        'titulo': 'Dashboard - Resultados',
        'pais': request.session['pais'],
        'area_selvatica': request.session['area_selvatica'],
        'poblacion_urbana': request.session['poblacion_urbana'],
        'gases_efecto_invernadero': request.session['gases_efecto_invernadero'],
        'deforestacion': request.session['deforestacion'],
        'estadistica_area_selvatica': request.session['estadistica_area_selvatica'],
        'estadistica_poblacion_urbana': request.session['estadistica_poblacion_urbana'],
        'estadistica_gases_efecto_invernadero': request.session['estadistica_gases_efecto_invernadero'],
        'comparativo_1990_2000': request.session['comparativo_1990_2000'],
        'comparativo_2000_2010': request.session['comparativo_2000_2010'],
        'comparativo_2010_2017': request.session['comparativo_2010_2017'],
    })