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
#variablews globales 

#GDTA SE CONFIGURA ARCHIVO PARA HISTORIAL Y LOGGING
LOG_FILENAME = 'mqtt.log'
sockt = socket.socket()
#os.remove("mqtt.log")

#Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )

class comandos:
    def __init__(self, data = []):
        self.data = True

    #La "longitud" del objeto, es en realidad representado
    #por la cantidad de datos de su lista principal
    def __len__(self):
        return len(self.data)
    def __str__(self):
        return str(self.data)
    #mensaje de alive cada 2 segundos
    def alive(self,ALIVE_PERIOD):
      # se envia un menaje cada 2 segundos indicando que sigue conectado
        intentos = 0
        desconeccion = 0
        while True:      
            client.publish(topicComandos_alive, tramaALIV, qos = 0,retain = False)
            time.sleep(ALIVE_PERIOD)
            vect_alive = read(LOG_FILENAME)
            a = list(vect_alive[1])
            if len(a) == 1:
                intentos += 1
                if intentos > 3:
                    ALIVE_PERIOD = 0.1
                    desconeccion += 1
                    if desconeccion == 200:
                        logging.critical('no se puede establecer conexión al servidor.')
                        sys.exit() 
            if len(a) > 1:
                ALIVE_PERIOD = 2
                intentos = 0
                desconeccion = 0
                i = 1
                mensaje = 1
                comand.archi(mensaje,i)
   
    def archi(self,pay,i):
        vect_alive = read(LOG_FILENAME)
        vect_alive[i]= str(pay)
        archivo = open(LOG_FILENAME,'w') #Abrir para SOBREESCRIBIR el archivo existente
        for i in range(len(vect_alive)):
            archivo.write(vect_alive[i]+'\n')
        archivo.close()
    def negociación (self,mnsa):
        res = mnsa.split('$')
        res[0]=res[0].replace("b'\\",'')
        return res[0]
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


class Manejo_Cliente:
    def __init__(self, data = []):
        self.data = True
    def mensajes(self,x):
        print('a. Enviar a usuario')
        print('b. Enviar a sala')
        t = input('-:')
        if t == 'a':
            print('1. 201612625')
            print('2. ---')
            t = input('-:')
            if t == '1' :
                t = input('escriba el texto:  ')
                trama = user_t + SEPARADOR + t.encode() #codifica el mensaje 
                #enviamos el mensaje
                client.publish(PUBL_user2, trama, qos = 0,retain = False)
        if t == 'b':
            print('1. 24S15')
            print('2. 24S11')
            t = input('-:')
            if t == '1' :
                t = input('escriba el texto:  ')
                trama = user_t + SEPARADOR + t.encode() #codifica el mensaje 
                #enviamos el mensaje
                client.publish(topic_sala1 , trama, qos = 0,retain = False)
            if t == '2' :
                t = input('escriba el texto:  ')
                trama = user_t + SEPARADOR + t.encode() #codifica el mensaje 
                #enviamos el mensaje
                client.publish(topic_sala2, trama, qos = 0,retain = False)

    def audio(self,x):
        print('elija la duración del audio')
        t = int(input('-:'))
        os.system('arecord -d {!r} -f U8 -r 8000 audio_p.wav'.format(t))
        size =str(os.stat('audio_p.wav').st_size)
            
        '''
        f = open("audio_p.wap", "rb")
        imagestring = f.read()
        f.close()
        trama_audio = bytearray(imagestring)
        '''
        print('Enviar a')
        print('1. sala')
        print('2. usuario')
        t = input('-:')
        if t == '1' :   
            print('Enviar a')
            print('1. sala1')
            print('2. sala2')
            t = input('-:')
            if t == '1':
                tramaFTR= FTR+SEPARADOR+sala1.encode()+SEPARADOR+size.encode() 
                client.publish(topic_comandos,tramaFTR , qos = 0,retain = False)
            if t == '2':
                tramaFTR= FTR+SEPARADOR+sala2.encode()+SEPARADOR+size.encode() 
                client.publish(topic_comandos,tramaFTR , qos = 0,retain = False)
        if t == '2':
            tramaFTR= OK+SEPARADOR+user2_t+SEPARADOR+size.encode()
            client.publish(topic_comandos,tramaFTR , qos = 0,retain = False)
            print('esperando respuesta .....')
            time.sleep(0.5)
            res =comand.respuesta ()
            if res == True:
                print('enviar archivo')
                sockt.connect(('localhost',9824))
               
                with open('audio_p.wav', 'rb') as f: #Se abre el archivo a enviar en BINARIO
                    sockt.sendfile(f, 0)
                    f.close()
                sockt.close()
                print("\n\nArchivo enviado a: ")
            if res == False:
                logging.error('no es posible enviar el archivo')
manejo = Manejo_Cliente()     
comand = comandos()
#GDTA SE CONFIGURAN LA REPRODUCCCION DE AUDIO LAS SUSCRIPCIONES
# LAS PUBLICACIONES  Y LA LECTURA,ESCRITURA DE LOS ARCHIVOS DE AUDIO      
def play():
    os.system('aplay audio_s.wap')


#Handler en caso suceda la conexion con el broker MQTT
def on_connect(client, userdata, flags, rc): 
    client.subscribe([SUBS_comandos,SUBS_usuario,SUBS_sala1,SUBS_sala2])#,SUBS_comandos2
    t2 = threading.Thread (name = 'verificacion',
                            target = comand.alive,
                            args=(ALIVE_PERIOD,),
                            daemon = True
                            )

    t2.start()

#Handler en caso se publique satisfactoriamente en el broker MQTT

def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.debug( str(publishText) )


def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    respuesta = comand.negociación(str(msg.payload))
    '''
    if topic_audio== str(msg.topic) or topic_audio_sala1 == str(msg.topic) or topic_audio_sala2 == str(msg.topic):
        archivo = open('audio_s.wav', 'wb')
        archivo.write(msg.payload)
        hil ()
    '''
    if topic_comandos == str(msg.topic) and str(ACK1)== respuesta:
        logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
        logging.info("El contenido del mensaje es: " + str(msg.payload))
        mensaje = msg.payload
        i = 1
        comand.archi(mensaje,i)
    if topic_comandos == str(msg.topic) and (str(NO1) == respuesta or str(OK1)== respuesta):
        logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
        logging.info("El contenido del mensaje es: " + str(msg.payload))
        mensaje = msg.payload
        i = 4
        comand.archi(mensaje,i)
    if topic_comandos == str(msg.topic) and str(FRR1) == respuesta :
        logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
        logging.info("El contenido del mensaje es: " + str(msg.payload))
        mensaje = msg.payload
        i = 7
        comand.archi(mensaje,i)
    '''
    else:
        logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
        logging.info("El contenido del mensaje es: " + str(msg.payload))
    '''




logging.info("Cliente MQTT con paho-mqtt") #Mensaje en consola

'''
Config. inicial del cliente MQTT
'''
client = paho.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto

#SMC hilo alive

def hil ():
    t1 = threading.Thread (name = 'verificacion',
                                target = play,
                                daemon = True
                                )

    t1.start()




#SMC Loop principal:  TODA LA INTERACCION CON EL USUARIO Y LAS PETICIONES
#DE INSTRUCCIONES
client.loop_start()
try:
    while True:
        print('1. Enviar texto')
        print('2. Enviar mensaje de voz')
        print('3. Salir')
        x = int(input('-:'))
    #vemos que hacción hacer y a quien enviarlo
        #enviar mensaje 
        if x == 1 :  #usurio 1
            manejo.mensajes(x)
        elif x == 2:
            manejo.audio(x)
        elif x == 3:
            logging.warning("Desconectando del broker MQTT...")
            client.loop_stop()
            #if t1.isAlive():
             #   t1._stop()
            break      
        else:
            print('numero incorrecto')

except KeyboardInterrupt:
    logging.warning("Desconectando del broker MQTT...")
    client.loop_stop()


finally:
    client.disconnect()
    logging.info("Se ha desconectado del broker. Saliendo...")