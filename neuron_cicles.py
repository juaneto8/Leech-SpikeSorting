import PyLeech.Utils.unitInfo as burstStorerLoader
import PyLeech.Utils.burstUtils as burstUtils
import matplotlib.pyplot as plt
import numpy as np
import funciones
import PyLeech.Utils.burstClasses as burstClasses
from scipy import signal as sig
import pandas as pd
import seaborn as sb
#%%
# Posibles archivos que se pueden utilizar por ahora:
# filelist = ['2019_08_30_0006.pklspikes','2019_08_28_0007.pklspikes', '2021_06_15_0004.pklspikes', '2021_06_15_0009.pklspikes']

filename='2019_08_30_0006.pklspikes' #este es el que hay que cambiar

# Cargo el archivo pklspikes

datos_load=burstStorerLoader.UnitInfo(filename=filename,foldername='Data/pklspikes')
step=0.3
# Esto me saca el dictionario de adentro del archivo
spike_processed=burstUtils.processSpikeFreqDict(datos_load.spike_freq_dict, step=step, time_length=datos_load.time_length, counting=True)
# Me genera un diccionario con las neuronas y sus respectivas frecuencias y tiempos
dict_frecuencias=burstUtils.smoothBinnedSpikeFreqDict(spike_processed,2,10,step, half_gaussian=True)
# Me plotea todos los datos, lo puedo comentar
burstUtils.plotFreq(dict_frecuencias)
DE3 = datos_load.isDe3
neuron_list = list(dict_frecuencias.keys()) #Me genero una lista con las neuronas sacando la DE3 que las voy a usar despues
neuron_list.remove(DE3)

#%%
# Me tengo que generar un diccionario para los cortes en el tiempo dependiendo de cada archivo
# Estan ordenados de la forma [cortes, threshold]
utils = {'2019_08_30_0006.pklspikes': [3409, 3] , '2019_08_28_0007.pklspikes': [49, 3.5], '2021_06_15_0004.pklspikes' : [[2805,5680],3], 
 '2021_06_15_0009.pklspikes' : [2088,3]}

#Me elije el corte dependiendo de que archivo estoy mirando
micorte = utils[f'{filename}'][0]
# Corto los vectores de tiempo y spikes en los tiempos que quiero para DE3, hay que recordar cual era en el archivo
if filename == '2019_08_30_0006.pklspikes' or filename == '2019_08_28_0007.pklspikes':
    timesDE3=datos_load.spike_freq_dict[DE3][0][micorte:]
    datosDE3=datos_load.spike_freq_dict[DE3][1][micorte:]
elif filename == '2021_06_15_0004.pklspikes':   
    timesDE3=datos_load.spike_freq_dict[DE3][0][micorte[0]:micorte[1]]
    datosDE3=datos_load.spike_freq_dict[DE3][1][micorte[0]:micorte[1]]
else:
    timesDE3=datos_load.spike_freq_dict[DE3][0][:micorte]
    datosDE3=datos_load.spike_freq_dict[DE3][1][:micorte]
    
    

# Creo un diccionario con los datos para que lo lea el getbursts
DE3dict= {'times':timesDE3, 'datos':datosDE3}

burstsDE3=burstUtils.getBursts(times=timesDE3)
#prueba = burstClasses.crawlingSegmenter()

# Defino los intervalos usando la funcion
threshold = utils[f'{filename}'][1]
intervalos=funciones.definidor(burstsDE3, timesDE3,threshold)
# Defino los tiempos y frecuencias de DE3 que voy a usar en los vectores de frecuencias,
# no en los originales de spikes
freqtimes=dict_frecuencias[DE3][0]
freqsDE3=dict_frecuencias[DE3][1]
# me genera los intervalos en el mundo de frecuencias a partir de los intervalos del mundo de spikes
intervalosfreq=funciones.transformer(intervalos,freqtimes)
# Esto devuelve una lista de listas de los intervalos con tiempos de 0 a 1 y sus frecuencias
cicles_DE3=funciones.punteador(intervalosfreq,freqsDE3,freqtimes)
# Puedo graficar los ciclos superpuestos de DE3, nciclos me dice cuantos quiero graficar,
# hay que tener en cuenta el numero total de ciclos
# funciones.superponedor(prueba,nciclos=10)
# Lista con las neuronas que no son DE3 que quiero comparar
# numero de ciclos que quiero comparar
ciclos=10
#me genera un diccionario con los resultados obtenidos para todas las neuronas usando los intervalos de DE3 y tambien me los plotea
neuron_dict=funciones.compareneurons(neuron_list, dict_frecuencias, intervalosfreq,ciclos, cicles_DE3,DE3)
neuron_dict[f'{DE3}'] = cicles_DE3

# Checkea si todo salio bien a la hora de generar el diccionario, deberian todos los vectores
# tener la misma cantidad de intervalos (creo)
largos = []
for j in neuron_list:
    largos.append(len(neuron_dict[f'{j}']))
if np.all(largos):
    print('Parece que salio todo bien')
else:
    print('Houston tenemos un problema')
#%%
# Ahora voy a usar el neuron_dict para promediar la señal sobre todos los ciclos para cada una de las neuronas y luego volver a compararlas
# Primero que todo como cada ciclo tiene una cantidad de puntos diferentes, hago un resampleo de la señal tomando puntos = el max de puntos
# en un ciclo

#Veo cual tiene la mayor cantidad de puntos en su ciclo
maximos = []
for el in neuron_dict:
    temp = []
    for j in range(len(neuron_dict[el])):
        temp.append(len(neuron_dict[el][j][0]))
    maximos.append(max(temp))
    
#Esto es meramente para checkear que todos tengan el mismo largo por las dudas, solo importa el valor de uno de ellos
#%%
# Ahora entonces resampleo reemplazando en cada ciclo por su respectivo resampleado
# Pruebo primero con uno
for neuron in neuron_dict:
    for j in range(len(neuron_dict[str(neuron)])):
        neuron_dict[neuron][j][1] = sig.resample(neuron_dict[neuron][j][1],maximos[0])
        

#%%
#A partir de aca arrancamos devuelta la parte de resamplear y bien todo

#la idea ahora es generar listas e ir apendiandolas en el dataframe para luego graficarlos
#Agrego la DE3 a la lista de neuronas, esto hay que moverlo a mano, asi que estar atento
neuron_list.insert(1,DE3)
ciclos=np.linspace(1,len(cicles_DE3),len(cicles_DE3)) #para saber la cantidad de ciclos len(cicles_DE3)
ciclos = list(map(int,ciclos ))
time = np.linspace(0,1,len(neuron_dict['0'][1][1]))
#dataframe = pd.DataFrame(columns = ['tiempo', 'señal', 'ciclo', 'neurona'])
lista1=[]
lista2=[]
lista3=[]
lista4=[]
for neurona in neuron_list:
    for j in ciclos:
        signal = neuron_dict[str(neurona)][j-1][1]
        ciclo = np.ones(len(neuron_dict['0'][1][1]))*ciclos[j-1]
        neuron = neurona * np.ones(len(neuron_dict['0'][1][1]), dtype=int)
        lista1.extend(time)
        lista2.extend(signal)
        lista3.extend(ciclo)
        lista4.extend(neuron)
        #lista = [time, signal, ciclo, neuron]
        #dataframe = dataframe.append({'tiempo':lista[0], 'señal': lista[1], 'ciclo': lista[2], 'neurona': lista[3]}, ignore_index=True)
        #dataframe = dataframe.explode(['tiempo', 'señal', 'ciclo', 'neurona'], ignore_index=True)

dataframe = pd.DataFrame(lista1, columns = ['tiempo'])
dataframe['señal'] = lista2
dataframe['ciclo'] = lista3
dataframe['neurona'] = [str(i) for i in lista4]
#Ahora que tengo el dataframe que necesitaba, voy a hacer el grafico usando seaborn
#%%
#[dataframe.ciclo<11]
sb.lineplot(data=dataframe, x = 'tiempo', y = 'señal',hue ='neurona') #, ci='sd'

#Listo esto funciona! Habria que ver de mejorarlo para que se vea mejor. Mañana preguntar como embellecerlo un poco
#%%
#Duty cicle

time_ciclo = np.linspace(0,1,len(neuron_dict[str(DE3)][1][1]))
cuentas=[]
for j in range(len(cicles_DE3)):
        
    freqs_ciclo = neuron_dict[str(DE3)][j][1]
    cuadrado = funciones.cuadrados(neuron_dict[str(DE3)], .15)
    counter = 0
        
    for i in range(len(cuadrado[0][1])):
            
        if cuadrado[j][1][i] == 1:
                
            counter = counter + 1
    cuentas.append(counter)
    #plt.plot(time_ciclo,cuadrado[j][1])
    

duty_cicle = np.array(cuentas)/len(neuron_dict[str(DE3)][1][1])

#Ahora tengo que calcular los maximos para cada ciclo para todas las demas neuronas
#%%
pos_maximos = []

for neuron in neuron_list:
    
    max_cicles =[]
    
    for i in range(len(cicles_DE3)):
        
        freqs_ciclo = neuron_dict[str(neuron)][i][1]
        max_cicles.append(time_ciclo[np.where(freqs_ciclo == np.max(freqs_ciclo))[0][0]])
        
    pos_maximos.append(max_cicles)

#%%
#Algo asi el plot? Ahora que lo pienso denuevo no tiene demasiado sentido lo que habiamos pensado

plt.plot(range(18), pos_maximos[5][0:18],label = 'maximo')
plt.plot(range(18), duty_cicle[0:18], label ='duty cicle')
plt.grid()
plt.legend()

#%%
#Ahora voy a ver de plotear las mismas curvas de promedio pero cada 10 ciclos para ver como se mueve la cosa
if len(ciclos)>=10:
    ciclos10=np.linspace(1,10,10)
else:
    ciclos10=np.linspace(1,len(ciclos),len(ciclos))


ciclos10 = list(map(int,ciclos10))
time = np.linspace(0,1,len(neuron_dict[str(neuron_list[0])][1][1]))
#dataframe = pd.DataFrame(columns = ['tiempo', 'señal', 'ciclo', 'neurona'])
lista1_10=[]
lista2_10=[]
lista3_10=[]
lista4_10=[]
for neurona in neuron_list:
    for j in ciclos10:
        signal = neuron_dict[str(neurona)][j-1][1]
        ciclo = np.ones(len(neuron_dict[str(neuron_list[0])][1][1]))*ciclos10[j-1]
        neuron = neurona * np.ones(len(neuron_dict[str(neuron_list[0])][1][1]), dtype=int)
        lista1_10.extend(time)
        lista2_10.extend(signal)
        lista3_10.extend(ciclo)
        lista4_10.extend(neuron)
        #lista = [time, signal, ciclo, neuron]
        #dataframe = dataframe.append({'tiempo':lista[0], 'señal': lista[1], 'ciclo': lista[2], 'neurona': lista[3]}, ignore_index=True)
        #dataframe = dataframe.explode(['tiempo', 'señal', 'ciclo', 'neurona'], ignore_index=True)

dataframe_10 = pd.DataFrame(lista1_10, columns = ['tiempo'])
dataframe_10['señal'] = lista2_10
dataframe_10['ciclo'] = lista3_10
dataframe_10['neurona'] = [str(i) for i in lista4_10]
#%%
#Ahora de 20
if len(ciclos)>=20:
    ciclos20=np.linspace(1,20,20)
else:
    ciclos20=np.linspace(1,len(ciclos),len(ciclos))
ciclos20 = list(map(int,ciclos20))
time = np.linspace(0,1,len(neuron_dict[str(neuron_list[0])][1][1]))
#dataframe = pd.DataFrame(columns = ['tiempo', 'señal', 'ciclo', 'neurona'])
lista1_20=[]
lista2_20=[]
lista3_20=[]
lista4_20=[]
for neurona in neuron_list:
    for j in ciclos20:
        signal = neuron_dict[str(neurona)][j-1][1]
        ciclo = np.ones(len(neuron_dict[str(neuron_list[0])][1][1]))*ciclos20[j-1]
        neuron = neurona * np.ones(len(neuron_dict[str(neuron_list[0])][1][1]), dtype=int)
        lista1_20.extend(time)
        lista2_20.extend(signal)
        lista3_20.extend(ciclo)
        lista4_20.extend(neuron)
        #lista = [time, signal, ciclo, neuron]
        #dataframe = dataframe.append({'tiempo':lista[0], 'señal': lista[1], 'ciclo': lista[2], 'neurona': lista[3]}, ignore_index=True)
        #dataframe = dataframe.explode(['tiempo', 'señal', 'ciclo', 'neurona'], ignore_index=True)

dataframe_20 = pd.DataFrame(lista1_20, columns = ['tiempo'])
dataframe_20['señal'] = lista2_20
dataframe_20['ciclo'] = lista3_20
dataframe_20['neurona'] = [str(i) for i in lista4_20]

#%%
#Ploteo para 10 ciclos y para 20
sb.lineplot(data=dataframe_10, x = 'tiempo', y = 'señal',hue ='neurona')
sb.lineplot(data=dataframe_20, x = 'tiempo', y = 'señal',hue ='neurona')
#No se ven diferencias significativas en este caso
#%%
#Que pasa si miro los siguientes 10?
if len(ciclos)>=20:
    ciclos_pr=np.linspace(11,20,10)
else:
    ciclos_pr=np.linspace(11,len(ciclos),len(ciclos))

ciclos_pr = list(map(int,ciclos_pr))
time = np.linspace(0,1,len(neuron_dict[str(neuron_list[0])][1][1]))
#dataframe = pd.DataFrame(columns = ['tiempo', 'señal', 'ciclo', 'neurona'])
lista1_pr=[]
lista2_pr=[]
lista3_pr=[]
lista4_pr=[]
for neurona in neuron_list:
    for j in ciclos_pr:
        signal = neuron_dict[str(neurona)][j-1][1]
        ciclo = np.ones(len(neuron_dict[str(neuron_list[0])][1][1]))*ciclos_pr[j-11]
        neuron = neurona * np.ones(len(neuron_dict[str(neuron_list[0])][1][1]), dtype=int)
        lista1_pr.extend(time)
        lista2_pr.extend(signal)
        lista3_pr.extend(ciclo)
        lista4_pr.extend(neuron)
        #lista = [time, signal, ciclo, neuron]
        #dataframe = dataframe.append({'tiempo':lista[0], 'señal': lista[1], 'ciclo': lista[2], 'neurona': lista[3]}, ignore_index=True)
        #dataframe = dataframe.explode(['tiempo', 'señal', 'ciclo', 'neurona'], ignore_index=True)

dataframe_pr = pd.DataFrame(lista1_pr, columns = ['tiempo'])
dataframe_pr['señal'] = lista2_pr
dataframe_pr['ciclo'] = lista3_pr
dataframe_pr['neurona'] = [str(i) for i in lista4_pr]

#%%
#comparo los primeros 10 con los segundos 10
sb.lineplot(data=dataframe_10, x = 'tiempo', y = 'señal',hue ='neurona')
sb.lineplot(data=dataframe_pr, x = 'tiempo', y = 'señal',hue ='neurona')
#%%
neuron_corr =[]
mean_corr = []
for neuron in neuron_list:
    corr=[]
    for j in range(len(neuron_dict[str(DE3)])):
        cicloDE3 = neuron_dict[str(DE3)][j][1]
        otra = neuron_dict[str(neuron)][j][1]
        corr.append(np.corrcoef(cicloDE3, otra)[0,1])
    corr = [i for i in corr if np.isnan(i) == False]
    neuron_corr.append(corr)
    mean_corr.append(np.mean(corr))

#En algunos no funciona me devuelve not a number porque divide por 0
#se los saco

#for j in range(len(neuron_corr)):
 #   neuron_corr[j] = [i for i in neuron_corr[j] if np.isnan(i) == False]
#%%
plt.plot(range(22), neuron_corr[2]) 





