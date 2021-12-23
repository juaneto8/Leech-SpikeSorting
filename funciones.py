import numpy as np
import matplotlib.pyplot as plt

def definidor(bursts, times, threshold):
    # esta funcion me genera los intervalos para cada ciclo de la DE3
    # le tengo que dar el vector que me salio de getBursts y los tiempos de la DE3
    # el threshold maneja la distancia minima entre bursts para que no me tome 2 como 1
    # este valor va cambiando dependiendo del archivo, intente unificarlo en un numero pero
    # no lo logre
    comienzos=[]
    intervalos=[]
    for el in bursts:
        comienzos.append(el[0])
    for i in range(0,len(comienzos)-1):

        if i>=1 and np.abs(bursts[i][0]-bursts[i-1][-1])<threshold:
                intervalos.pop(-1)
                elementocorregido=[comienzos[i-1],comienzos[i+1]]
                intervalos.append(elementocorregido)
        else:
            elemento=[comienzos[i],comienzos[i+1]]
            intervalos.append(elemento)
    final=[intervalos[-1][-1],times[-1]]
    intervalos.append(final)
    return intervalos


def transformer(intervalos, freqtimes):
    # esta funcion transforma los tiempos de las espigas en el archivo original hacia el espacio
    # de frecuencias que esta discretizado
    indices=np.digitize(intervalos, freqtimes)
    resultado=freqtimes[indices]
    return resultado

def punteador(intervalosfreq,freqs, freqtimes):
    # esta funcion te genera los ciclos de DE3 a partir de los intervalos que generamos
    # con definidor
    resultado=[]
    for i in range(len(intervalosfreq)):
        intfreqs=freqs[np.where(freqtimes==intervalosfreq[i][0])[0][0]:np.where(freqtimes==intervalosfreq[i][1])[0][0]+1]
        inttimes=freqtimes[np.where(freqtimes==intervalosfreq[i][0])[0][0]:np.where(freqtimes==intervalosfreq[i][1])[0][0]+1]
        inttimes=(inttimes-inttimes[0])
        inttimes=inttimes/inttimes[-1]
        temp=[inttimes,intfreqs]
        resultado.append(temp)
    print(f'Obtuvimos {len(resultado)} ciclos')
    return resultado

def compareneurons(neuron_list, dict_frecuencias,intervalosfreq,nciclos,ciclesDE3,DE3):
    # Esta funcion te plotea las neuronas siempre la DE3 contra otra de las observadas
    freqtimes=dict_frecuencias[DE3][0]
    neuron_dict={}
    for el in neuron_list:
        frecuencias=dict_frecuencias[el][1]
        results=punteador(intervalosfreq, frecuencias, freqtimes)
        neuron_dict[f'{el}']=results
        plt.figure(el)
        plt.subplot(2,1,1)
        plt.title(f'Gráfico DE3-{el}')
        superponedor(ciclesDE3,nciclos)
        plt.subplot(2,1,2)
        superponedor(results,nciclos)
    return neuron_dict



def superponedor(lista,nciclos):
    # Lo mismo que la otra pero podes aparte modificar la cantidad de ciclos que queres ver con
    # el parametro nciclos
    for i in range(len(lista)-np.abs(len(lista)-nciclos)): #len(lista)-15
        #plt.figure(i)
        plt.plot(lista[i][0], lista[i][1], label=f'{i}')
        plt.xlabel('Posicion en un ciclo de DE3')
        plt.ylabel('Frecuencia (Hz?)')
        #plt.title('Ciclos superpuestos')
        plt.grid(True)
        plt.legend(ncol=2, loc='upper right')
        #plt.show()
    return



def cuadrados(vector,treshold):
    #Me vuelve las señales de frecuencia a funciones cuadradas
    vectorcuadrado=[]
    for j in range(len(vector)):
        cuadrado=np.zeros(len(vector[j][1]))
        maximo=np.max(vector[j][1])
        for i in range(len(vector[j][1])):
            if vector[j][1][i] > maximo*treshold:
                cuadrado[i]=1
            else:
                cuadrado[i]=0
        temp=[vector[j][0],cuadrado]
        vectorcuadrado.append(temp)
    return vectorcuadrado














