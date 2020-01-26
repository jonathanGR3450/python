import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import random
import subprocess, shlex
import os
import threading
import time

fig = plt.figure()
ax = plt.axes(xlim=(2400, 2500), ylim=(-100, -20))
#line, = plt.plot([], [], lw=2, label="")
plt.xlabel("frecuencia MHZ (canales)")
plt.ylabel("potencia dB")
line = []
textoUp=[]

#datos que necesito
chanel=[]
freq=[]
signal=[]
name=[]

def consultar():
        while True:
                print("entro a consultar")
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
                print("esta haciendo la consulta")
        


def animate(i):
        line.clear()
        name.clear()
        freq.clear()
        signal.clear()
        chanel.clear()
        graph_data = open('holamundo.txt','r').read()
        lineas = graph_data.split('\n')
        print("datos en txt")
        for linea in lineas:
            if len(linea) > 1:
                xname, xfreq, xsignal, xchanel  = linea.split(',')
                name.append(xname)
                freq.append(xfreq)
                signal.append(xsignal)
                chanel.append(xchanel)
        
        print("datos traidos del txt:")
        textoUp.clear()
        # for s in range(len(signal)):
        #         tex=plt.text(0, 0 , "")
        #         textoUp.append(tex)
        
        for k in range(len(signal)):
                a = (-100-float(signal[k]))/121
                frecuencia=float(freq[k])*1000
                x = np.arange(frecuencia-50, frecuencia+50, 1)
                y = a * (x-frecuencia) ** 2 + float(signal[k])

                mostrar="SSID:"+str(name[k])+", channel:"+str(chanel[k])+", signal:"+str(signal[k])
                textoUp.append(mostrar)
                aux,=plt.plot(x,y,color=color[k], lw=1)

                plt.text(int(frecuencia), int(signal[k]), str(mostrar))
                # aux.set_label("")
                print(aux)
                # aux.set_label(mostrar)
                line.append(aux)
        #plt.legend(loc='upper left')
        #time.sleep(2)
        return (line)


color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(50)]

var=subprocess.getoutput('iwconfig')
interfaz=var.splitlines()
consulta=""
for i in range(len(interfaz)):
        if interfaz[i].find("w", 0, 1)==0:
                y=interfaz[i].split()
                consulta=y[0]

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
f = open ('holamundo.txt','w')
for c in range(len(canal)):
        f.write(str(essid[c])+','+str(frecuencia[c])+','+str(señal[c])+','+str(canal[c])+'\n')
f.close()

hilo1= threading.Thread(target=consultar)
hilo1.start()

anim = animation.FuncAnimation(fig, animate, frames=200, interval=900, blit=True)
plt.show()