import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import random
import subprocess, shlex
import os
import threading

import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


fig = plt.figure()
ax = plt.axes(xlim=(2400, 2500), ylim=(-100, -20))
line, = plt.plot([], [], lw=2, label="")
plt.xlabel("frecuencia MHZ (canales)")
plt.ylabel("potencia dB")
#datos que necesito
chanel=[]
freq=[]
signal=[]
name=[]

root = tkinter.Tk()
root.wm_title("Grafica insertada en Tkinter")
root.geometry('1000x800')



#metodo que tiene le hilo de consultar para almacenar datos en el txt
def consultar():
        while True:
                ssid = subprocess.getoutput("sudo iwlist "+consulta+" scan |egrep 'ESSID|Frequency|Channel|Signal'")
                row=ssid.splitlines()
                canal=[]
                frecuencia=[]
                señal=[]
                essid=[]
                aux=[]
                auxFreq=[]
                for j in range(len(row)):
                        if j*4+3<len(row):
                                aux=row[j*4].split(":")
                                canal.append(aux[1])

                                aux=row[j*4+1].split()
                                auxFreq=aux[0].split(":")
                                frecuencia.append(auxFreq[1])

                                aux=row[j*4+2].split("level=")
                                auxFreq=aux[1].split()
                                señal.append(auxFreq[0])

                                aux=row[j*4+3].split(":")
                                essid.append(aux[1])
                

                f = open ('holamundo.txt','w')
                for c in range(len(canal)):
                        f.write(str(essid[c])+','+str(frecuencia[c])+','+str(señal[c])+','+str(canal[c])+'\n')
                f.close()
        

#metodo que grafica
def animate(i):
        name.clear()
        freq.clear()
        signal.clear()
        chanel.clear()
        textoUp=[]
        for s in range(20):
                time_text = plt.text(0, 0, '')
                textoUp.append(time_text)

        graph_data = open('holamundo.txt','r').read()
        lineas = graph_data.split('\n')
        for linea in lineas:
            if len(linea) > 1:
                xname, xfreq, xsignal, xchanel  = linea.split(',')
                name.append(xname)
                freq.append(xfreq)
                signal.append(xsignal)
                chanel.append(xchanel)
        
        auxx=[]
        auxy=[]
        for k in range(len(signal)):
                a = (-100-float(signal[k]))/121
                frecuencia=float(freq[k])*1000
                x = np.arange(frecuencia-50, frecuencia+50, 1)
                y = a * (x-frecuencia) ** 2 + float(signal[k])
                auxx.append(x)
                auxy.append(y)
                mostrar="SSID:"+str(name[k])+", channel:"+str(chanel[k])+", signal:"+str(signal[k])
                textoUp[k].set_text(str(mostrar))
                textoUp[k].set_position((int(frecuencia), int(signal[k])))
                
        line.set_data(auxx,auxy)
        return line, textoUp[0], textoUp[1], textoUp[2], textoUp[3], textoUp[4], textoUp[5], textoUp[6], textoUp[7], textoUp[8], textoUp[9], textoUp[10], textoUp[11], textoUp[12], textoUp[13], textoUp[14], textoUp[15], textoUp[16], textoUp[17], textoUp[18]


#hago la primera consulta, de la interfaz y de los datos de la señal wifi
#comienzo consultando el nombre de la tarjeta de red
var=subprocess.getoutput('iwconfig')
interfaz=var.splitlines()
consulta=""
for i in range(len(interfaz)):
        if interfaz[i].find("w", 0, 1)==0:
                y=interfaz[i].split()
                consulta=y[0]

#hago laconsulta de los primeros datos
ssid = subprocess.getoutput("sudo iwlist "+consulta+" scan |egrep 'ESSID|Frequency|Channel|Signal'")
row=ssid.splitlines()
canal=[]
frecuencia=[]
señal=[]
essid=[]
aux=[]
auxFreq=[]
for j in range(len(row)):
        if j*4+3<len(row):
                aux=row[j*4].split(":")
                canal.append(aux[1])

                aux=row[j*4+1].split()
                auxFreq=aux[0].split(":")
                frecuencia.append(auxFreq[1])

                aux=row[j*4+2].split("level=")
                auxFreq=aux[1].split()
                señal.append(auxFreq[0])

                aux=row[j*4+3].split(":")
                essid.append(aux[1])

chanel=canal
freq=frecuencia
signal=señal
name=essid
#escribo en el txt que consume la grafica
f = open ('holamundo.txt','w')
for c in range(len(canal)):
        f.write(str(essid[c])+','+str(frecuencia[c])+','+str(señal[c])+','+str(canal[c])+'\n')
f.close()
#hilo de consulta
hilo1= threading.Thread(target=consultar)
hilo1.start()
#hilo de animacion, es un metodo de plot
anim = animation.FuncAnimation(fig, animate, frames=200, interval=900, blit=True)
plt.show()