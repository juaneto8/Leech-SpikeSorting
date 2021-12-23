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

np.set_printoptions(precision=3)
plt.ion()
#%%
filenames = ['prueba.abf', #esto cambia dependiendo el nombre del archivo
             ]
#levanto de los abf los datos
arr_dict, time , fs= abfe.getArraysFromAbfFiles(filenames, ['IN4','IN5'])

n1=arr_dict['IN5'] # este tiene que ser el DP, estos los invertimos dependiendo del archivo siguiendo el word
n2=arr_dict['IN4'] #
del arr_dict

ln = len(time)
#corro un filtro para bajar el ruido
n1_filt = filterUtils.runButterFilter(n1, 5000, sampling_rate=fs)
n1_filt = filterUtils.runButterFilter(n1_filt, 5, sampling_rate=fs, butt_order=4, btype='high')

n2_filt = filterUtils.runButterFilter(n2, 5000, sampling_rate=fs)
n2_filt = filterUtils.runButterFilter(n2_filt, 5, sampling_rate=fs, butt_order=4, btype='high')

sorter = SpSorter.SpSorter(filenames, "Data", [n1_filt, n2_filt], time, fs)
del time, n1, n1_filt, n2, n2_filt

sorter.normTraces()
#sorter.plotTraceAndStd()
#sorter.smoothAndVisualizeThreshold()
# selecciono los picos que voy a utilizar
sorter.smoothAndFindPeaks(vect_len=5, threshold=10, min_dist=150)
sorter.makeEvents(99, 100)
sorter.makeNoiseEvents(size=4000)
sorter.plotEvents(plot_noise=False)
#me quedo con una fraccion para agilizar el proceso, si tomo todos tarda mucho tiempo
sorter.takeSubSetEvents(0.3) #esto lo cambiamos dependiendo del archivo
sorter.getPcaBase()
sorter.getVectorWeights(30)
#genero el mapa tsne
sorter.fitTSNE(pca_dim_size=10)
sorter.viewTSNE()
#realizo proceso de clustering, ya me guarda el archivo pkl. El proceso continua en el archivo
# "loaddoble.py"
sorter.GmmClusterEvents(20, use_tsne=True, n_init=400, max_iter=6000, save=True)

#sorter.viewTSNE()
#sorter.plotTemplates()
#sorter.plotClusteredEvents()