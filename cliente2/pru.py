import paho.mqtt.client as paho
import paho.mqtt.client as mqtt
import logging
import time
import random
import threading #Concurrencia con hilos
import sys 
import os 

def read(a):
    LISTADO = a
    datos = []
    archivo = open(LISTADO, 'r')
    registro = archivo.readlines()
    for i in range(len(registro)):
        datos.append(registro[i].replace('\n', '') ) 
    archivo.close()
    return datos

a = 'mqtt.log'
vect = read(a)
vect [1]= 'hola'
archivo = open(a,'w') #Abrir para SOBREESCRIBIR el archivo existente
for i in range(len(vect)):
    archivo.write(vect[i]+'\n')
archivo.close()
size =str(os.stat('audio_p.wav').st_size)
size=size.encode()
frr = vect[4].split('$')
frr[0] = frr[0].replace("b'\\",'')
print(frr)
print(size)
print(vect)
print(a)