import threading #Concurrencia con hilos
#Parametros de conexion
#"157.245.82.242"
MQTT_HOST = "167.71.243.238"
MQTT_PORT = 1883
BUFFER_SIZE = 64*1024
#GDTA
#MQTT_USER = "pr24"
#MQTT_PASS = "Patito!#2020"
MQTT_USER = "proyectos"
MQTT_PASS = "proyectos980"
arch = 'topics'
ESTADO_ALIVE = False
ALIVE_PERIOD = 2
#SMC pasa los datos del archivo  a una vector
def read(a):
    LISTADO = a
    datos = []
    archivo = open(LISTADO, 'r')
    registro = archivo.readlines()
    for i in range(len(registro)):
        datos.append(registro[i].replace('\n', '') ) 
    archivo.close()
    return datos
#SMC se obtienen los datos del vextor 
datos = read(arch)
usuario = datos[1]
sala1= datos[3]
sala2= datos[4]
sala3= datos[5]
qos = 2
user2 = datos[13]  #titus
user2_t = datos[13].encode() 
user_t =datos[1].encode()  #sebas
GRUPO = datos[15]
#SMC comandos SE CONFIGURAN LAS INSTRUCCIONES, LOS TOPICS Y LAS TRAMAS DE 
# CADA USUARIO
FTR = b'\x03'       #audio
ALIVE = b'\x04'     #alive
ACK = b'\x05'
FRR = b'\x02'
NO = b'\x07'
OK = b'\x06'

FRR1 = 'x02'
FTR1 = 'x03'
ALIVE1 = 'x04'
ACK1 = 'x05'
OK1 = 'x06'
NO1 = 'x07'
SEPARADOR = b'$'



#SMC destinos o topics de subscripcion
#alive
topicComandos_alive = 'comandos/'+str(GRUPO)
tramaALIV = ALIVE+SEPARADOR+user_t  

#SMC salas
topic_sala1 = 'salas/'+str(GRUPO)+'/'+sala1
topic_sala2 = 'salas/'+str(GRUPO)+'/'+sala2
#SMC subs
SUBS_comandos2 = (topicComandos_alive, qos)
SUBS_comandos = (datos[7], qos)
SUBS_usuario = (datos[8], qos)
SUBS_sala1 = (datos[9], qos)
SUBS_sala2 = (datos[10], qos)

#SMC tramas de comandos
trama_ACK = ACK+user_t

#SMC audio
PUBL_user2 = 'usuarios/'+str(GRUPO)+'/'+str(user2)
PUBL_audios_us =  'audios/'+str(GRUPO)+'/'+str(user2)
PUBL_audios_sal1= 'audios/'+str(GRUPO)+'/'+str(sala1)
PUBL_audios_sal2= 'audios/'+str(GRUPO)+'/'+str(sala2)
#SMC topics
topic_comandos = datos[7]
topic_audio = 'audios/'+str(GRUPO)+'/'+str(usuario)
topic_audio_sala1 = 'salas/'+str(GRUPO)+'/'+str(sala1)
topic_audio_sala2 = 'salas/'+str(GRUPO)+'/'+str(sala1)



SUBS_usuario2 = (PUBL_user2, qos)