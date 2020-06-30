import os
import threading as hilo
import socket
import logging




#GDTA CLASE QUE MANEJA LA COMUNICACION TCP DEL CLIENTE
class Cliente_tcp:
    def __init__(self):              #GDTA CONSTRCTOR
        self.HOST = "localhost" #GDTA IP HOST
        self.TCP_PORT = 9824         #GDTA PUERTO TCP
        self.BUFF_SIZE = 64 * 1024   #GDTA TAMAÑO DE BUFFER

    def enviar_audio(self):          #GDTA METODO PARA ENVIAR EL AUDIO
        clientSocket = socket.socket() #GDTA INSTANCIA DEL SOCKET TCP
        clientSocket.connect((self.HOST, self.TCP_PORT))  #GDTA SE CONECTA CON EL SERVIDOR
        loginfo = 'Enviando audio a: ' + str(self.HOST)   #GDTA SE CONCATENA EL NOMBRE DE QUIEN ENVIA EL MENSAJE, PARA EL CLIENTE SIEMPRE ES EL SERVIDOR
        logging.info(loginfo) #GDTA SE DESPLIEGA LA INFO DE QUIEN LO ENVIO
        with open('audio_p.wav','rb') as f: #GDTA SE ABRE EL ARCHIVO A ENVIAR EN BINARIO
            clientSocket.sendfile(f,0) 
            f.close()
        clientSocket.close() #gdta se cierra el archivo
        loginfo = 'Audio enviado a: ' + str(self.HOST)
        logging.info(loginfo)
        logging.info('Cerrando conexion tcp')
        clientSocket.close() #gdta se cierra el socket
    
    def recibir_audio(self): #gdta metodo para enviar el audio
        clientSocket = socket.socket() #GDTA INSTANCIA DEL SOCKET TCP
        clientSocket.connect((self.HOST, self.TCP_PORT)) #GDTA SE CONECTA CON EL SERVIDOR
        try:
            buff = clientSocket.recv(self.BUFF_SIZE)
            archivo = open('audio_s.wav', 'wb') #gdta se guarda el archivo entrante
            while buff: #gdta mientras hallan datos en buffer se sigue recibiendo
                buff = clientSocket.recv(self.BUFF_SIZE) #gdta se recibe el resto de datos, si hay mas
                archivo.write(buff) #gdta se escribe el resto de datos, si hay mas
            archivo.close() #sgdta e cierra el archivo
            logging.info('Recepcion finalizada')
            archivo = Audio(0) #gdta se crea una instancia para Audio
            archivo.reproducir_recibido() #gdta se reproduce el audio
        finally:
            logging.info('Cerrando conexion tcp')
            clientSocket.close()  #gdta se cierra socket tcp

           
class Audio: #gdta clase audio, manejo los archivos de audio
    def __init__(self, duracion):
        self.duracion = duracion #gdta duracion del audio, solo para grabar puede ser 0 si solo se desea reproducir
    
    def grabar(self): #gdta metodo que graba el audio
        logging.info('Grabando audio')
        os.system('arecord -d {} -f U8 -r 8000 pista.wav'.format(self.duracion))
        logging.info('Grabacion finalizada')
        #gdta el audio se graba a 8 bits con 8kHz de muestreo

    def reproducir(self): #gdta se reproduce el audio grabado localmente
        logging.info('Se reproducira el audio')
        os.system('pista.wav')
        logging.info('Reproduccion finalizada')
    
    def reproducir_recibido(self): #gdta para reproducir el audio recibido
        logging.info('Se reproducira el audio recibido')
        os.system('aplay pista2.wav')
        logging.info('Reproduccion finalizada')

    def peso(self): #gdta devuelve el tamaño del archivo de audio local
        audio_size = os.stat('pista.wav').st_size
        return audio_size


