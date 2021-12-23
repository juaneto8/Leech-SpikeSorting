import PyLeech.Utils.AbfExtension as abfe
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import PyLeech.Utils.constants as constants
import PyLeech.Utils.burstUtils as burstUtils
import PyLeech.Utils.spsortUtils as spsortUtils
import PyLeech.Utils.SpSorter as SpSorter
import PyLeech.Utils.unitInfo as burstStorerLoader
nan = constants.nan
opp0 = constants.opp0
import PyLeech.Utils.filterUtils as filterUtils
sorter = SpSorter.SpSorter('Data/2019_08_30_0006.pkl')
sorter.setGoodColors()
sorter.plotTemplates()
sorter.viewTSNE()
#sorter.plotTemplates()
#sorter.plotClusteredEvents()

'''
Aca voy a arrancar a trabajar los clusters
'''

#En esta parte del codigo una vez cargado el archivo voy a tener que usar las funciones
# de la clase sorter para juntar, separar y modificar los clusters hasta llegar a lo que busco.
# Esto se hace por consola por eso no aparece nada aca. 

#%%
#me genera el diccionario con los spikes de los clusters
sorter.makeCenterDict(400, 700)
sorter.plotCenterDict()
#genera una prediccion inicial para reemplazar los potenciales de accion por sus templados
sorter.clusteringPrediction()
sorter.before = 50
sorter.after = 50


#realiza devuelta el proceso de prediccion para seguir reemplazando spikes
sorter.secondaryPeeling(vect_len=5, threshold=9, min_dist=50, store_mid_steps=False)
sorter.plotPeeling(time=sorter.time[::2], to_peel_data=sorter.peel[-2][:,::2],
                   pred=sorter.pred[-1][:,::2])
#guarda los resultados del peeling
sorter.mergeRoundsResults()
#genera las frecuencias
spike_freqs = burstUtils.getInstFreq(sorter.time, sorter.final_spike_dict, sorter.sample_freq)

# Esto me sirve para ver las frecuencias y ver si triggerean al mismo tiempo

fig, ax_list = sorter.plotCompleteDetection(step=5,legend=True, lw=0.5)
burstUtils.plotFreq(spike_freqs, template_dict=sorter.template_dict, scatter_plot=True,
                                  outlier_thres=3.5, sharex=ax_list[0], ms=3, facecolor='k')

# Esto es para guardar una vez haya terminado
good_colors = spsortUtils.setColors(list(sorter.final_spike_dict.keys()))
DE3 = 1  #esto cambia dependiendo del archivo
#al guardar es importante que foldername sea lo que vos digas
#aca se guarda como archivo pklspikes que abriremos en el script "neuron_cicles.py"
burst_object = burstStorerLoader.UnitInfo(sorter.filename,foldername='Data/pklspikes', mode='save', time_length=sorter.time[-1], spike_dict=sorter.final_spike_dict, spike_freq_dict=spike_freqs,
                                          De3=DE3, template_dict=sorter.template_dict, color_dict=good_colors,nerve_channels=['DP','AA'])






