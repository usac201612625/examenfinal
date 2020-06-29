import os
import threading as hilo
import socket
import logging

#GDTA CONFIGURACION LOGGING
logging.basicConfig(level = logging.DEBUG, format = '%(message)s')

class Servidor_tcp:
    def __init__(self):              #GDTA CONSTRCTOR
        self.HOST = "localhost"
        self.TCP_PORT = 9824         #GDTA PUERTO TCP
        self.BUFF_SIZE = 64 * 1024   #GDTA TAMAÑO DE BUFFER

    def montar(self):
        serverSocket = socket.socket() #gdta se crea instancia del socket
        serverSocket.bind((self.HOST, self.TCP_PORT)) #GDTA SE CONECTA CON EL SERVIDOR
        serverSocket.listen(5)

    def enviar_audio(self):          #GDTA METODO PARA ENVIAR EL AUDIO
        ''' serverSocket = socket.socket() #gdta se crea instancia del socket
        serverSocket.bind((HOST, TCP_PORT)) #GDTA SE CONECTA CON EL SERVIDOR
        serverSocket.listen(5) '''
        conn, addr = serverSocket.accept()
        loginfo = 'Concetado con: ' + str(addr)
        logging.info(loginfo)
        loginfo = 'Enviando audio a: ' + str(conn)   #GDTA SE CONCATENA EL NOMBRE DE QUIEN ENVIA EL MENSAJE, PARA EL CLIENTE SIEMPRE ES EL SERVIDOR
        logging.info(loginfo) #GDTA SE DESPLIEGA LA INFO DE QUIEN LO ENVIO
        with open('pista.wav','rb') as f: #GDTA SE ABRE EL ARCHIVO A ENVIAR EN BINARIO
            conn.sendfile(f,0) 
            f.close()
        conn.close() #gdta se cierra el archivo
        loginfo = 'Audio enviado a: ' + str(conn)
        logging.info(loginfo)
        logging.info('Cerrando conexion tcp')
        clientSocket.close() #gdta se cierra el socket
        
    def recibir_audio(self): #gdta metodo para enviar el audio
        ''' serverSocket = socket.socket() #gdta se crea instancia del socket
        serverSocket.bind((HOST, TCP_PORT)) #GDTA SE CONECTA CON EL SERVIDOR
        serverSocket.listen(5) '''
        try:
            conn, addr = serverSocket.accept()
            loginfo = 'Concetado con: ' + str(addr)
            logging.info(loginfo)
            buff = conn.recv(self.BUFF_SIZE)
            archivo = open('pista.wav', 'wb') #gdta se guarda el archivo entrante
            while buff: #gdta mientras hallan datos en buffer se sigue recibiendo
                buff = serverSocket.recv(self.BUFF_SIZE) #gdta se recibe el resto de datos, si hay mas
                archivo.write(buff) #gdta se escribe el resto de datos, si hay mas
            archivo.close() #sgdta e cierra el archivo
            logging.info('Recepcion finalizada')
            
        finally:
            logging.info('Cerrando conexion tcp')
            serverSocket.close()  #gdta se cierra socket tcp

sc = Servidor_tcp()
sc.montar()
