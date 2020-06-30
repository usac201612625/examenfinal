import paho.mqtt.client as paho
import paho.mqtt.client as mqtt
import logging
import time
import socket
import random
import threading #Concurrencia con hilos
import sys 
import os 
from brokerData import* #Informacion de la conexion
from servertcp import *



#GDTA SE CONFIGURA ARCHIVO PARA HISTORIAL Y LOGGING
LOG_FILENAME = 'mqtt.log'
sockt = socket.socket()
audio = Servidor_tcp()
#os.remove("mqtt.log")

#Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )
#SMC clase de comandos
class comandos:
    def __init__(self, data = []):
        self.data = True
    #SMC funcion alive
    def alive(self,ALIVE_PERIOD):
        intentos = 0
        desconeccion = 0
         #smc se envia un menaje cada 2 segundos indicando que sigue conectado
        while True:      
            client.publish(topicComandos_alive, tramaALIV, qos = 0,retain = False)
            time.sleep(ALIVE_PERIOD)
            vect_alive = read(LOG_FILENAME)
            a = list(vect_alive[1])
            #SMC verifica los mensajes de verificacon de servidor
            if len(a) == 1: #SMC lee el vector donde se guardan los mensajes entrantes
                intentos += 1
                if intentos > 3:
                    ALIVE_PERIOD = 0.1 #SMC aumenta la velocidad de envio de mensaje alive 
                    desconeccion += 1
                    if desconeccion == 200:
                        logging.critical('no se puede establecer conexión al servidor.')
                        sys.exit()
                        client.loop_stop() 
            if len(a) > 1:
                ALIVE_PERIOD = 2
                intentos = 0
                desconeccion = 0
                i = 1
                mensaje = 1
                comand.archi(mensaje,i)
    #SMC escribe en el alrchivo mqrr.log
    def archi(self,pay,i):
        vect_datos = read(LOG_FILENAME)
        vect_datos[i]= str(pay)
        archivo = open(LOG_FILENAME,'w') #Abrir para SOBREESCRIBIR el archivo existente
        for i in range(len(vect_datos)):
            archivo.write(vect_datos[i]+'\n')
        archivo.close()
    #SMC pasa a un vector los mensajes que llegan
    def negociación (self,mnsa):
        res = mnsa.split('$')
        res[0]=res[0].replace("b'\\",'')
        return res[0]
    #SMC verifica las respuestas del servidor 
    def respuesta (self):
        vect_respuesta = read(LOG_FILENAME)
        ver = comand.negociación(vect_respuesta[4])
        if ver == OK1 :
            mensaje = 1
            i = 4
            comand.archi(mensaje,i)
            return True
        if ver == NO1:
            mensaje = 1
            i = 4
            comand.archi(mensaje,i)
            return False
           

    #SMC Representacion cuando se invoca el objeto sin casting a STRING.
    def __repr__(self):
        return self.__str__()

#SMC clase de manejo del cliente
class Manejo_Servidor:
    def __init__(self, data = []):
        self.data = True

def on_publish(client, userdata, mid):
    pass
#smc Handler en caso suceda la conexion con el broker MQTT
def on_connect(client, userdata, flags, rc): 
    servidor.subscribe(topic = 'comandos/24/#')#suscripcion
    #SMC evia el mensaje de alive 
    
#smc Handler en caso se publique satisfactoriamente en el broker MQTT

def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    #respuesta = comand.negociación(str(msg.payload))

    if topic_comandos == str(msg.topic) and ALIVE1 == respuesta:
        hil2()
    
    if topic_comandos == str(msg.topic) and FRR1 == respuesta:
        audio.recibir_audio()
        hil ()

    if topic_comandos == str(msg.topic) and str(ALIVE1)== respuesta:
        mensaje = msg.payload
        i = 1
        comand.archi(mensaje,i)
    if topic_comandos == str(msg.topic) and (str(NO1) == respuesta or str(OK1)== respuesta):
        mensaje = msg.payload
        i = 4
        comand.archi(mensaje,i)
    if topic_comandos == str(msg.topic) and str(FTR1) == respuesta :
        mensaje = msg.payload
        i = 7
        comand.archi(mensaje,i)


manejo = Manejo_Servidor()     
comand = comandos()

logging.info("Servidor MQTT con paho-mqtt") #Mensaje en consola

'''
Config. inicial del cliente MQTT
'''
servidor= paho.Client(clean_session=True) #Nueva instancia de cliente
servidor.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
servidor.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo
servidor.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
servidor.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
servidor.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto

#SMC hilo alive

def hil ():
    t1 = threading.Thread (name = 'verificacion',
                                target = reproducir.reproducir_recibido ,
                                daemon = True
                                )#gdta lo deje como demonio porque sino ya no se cerraba
    t1.start()                           
def hil2():
    t2 = threading.Thread (name = 'verificacion',
                            target = comand.alive,
                            args=(ALIVE_PERIOD,),
                            daemon = True
                            )
    t2.start()

#SMC Loop principal:  TODA LA INTERACCION CON EL USUARIO Y LAS PETICIONES
#DE INSTRUCCIONES
servidor.loop_forever()
try:
    pass

except KeyboardInterrupt:
    logging.warning("Desconectando del broker MQTT...")
    client.loop_stop()


finally:
    client.disconnect()
    logging.info("Se ha desconectado del broker. Saliendo...")
