import socket
import threading

ipserver=input("Escribe la IP del servidor: ")
port=8000                  #PUERTO DEL SERVIDOR QUE ATENDERÁ PETICIONES


#SE CREA CONEXIÓN TCP/IP ENTRE CLIENTE Y SERVIDOR
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)        

client.connect((ipserver,port))


nombre=input("Escribe tu nombre de usuario: ")      #SE PREGUNTA A USUARIO SU NOMBRE

def encriptar(mensaje, desplazamiento):           #ENCRIPTACIÓN CIFRADO CÉSAR
    mensaje_encriptado = ""
    for caracter in mensaje:
        if str(caracter).isalpha():
            ascii_inicial = ord('a') if str(caracter).islower() else ord('A')
            ascii_encriptado = (ord(str(caracter)) - ascii_inicial + int(desplazamiento)) % 26 + ascii_inicial      #FÓRMULA ENCRIPTADO
            caracter_encriptado = chr(ascii_encriptado)
            mensaje_encriptado += caracter_encriptado
        else:
            mensaje_encriptado += str(caracter)
    return mensaje_encriptado


def decrypt(mensaje_encriptado, desplazamiento):    #DESENCRIPTACIÓN CIFRADO CÉSAR
    mensaje_desencriptado = ""
    for caracter in mensaje_encriptado:
        if caracter.isalpha():
            ascii_inicial = ord('a') if caracter.islower() else ord('A')
            ascii_desencriptado = (ord(caracter) - ascii_inicial - desplazamiento) % 26 + ascii_inicial     
            caracter_desencriptado = chr(ascii_desencriptado)
            mensaje_desencriptado += caracter_desencriptado
        else:
            mensaje_desencriptado += caracter
    return mensaje_desencriptado


def recibir():          #FUNCIÓN PARA RECIBIR MENSAJES DESDE EL SERVIDOR
    while True:         
        try:
            msj=client.recv(1024).decode('utf-8')       #SE RECIBEN MENSAJES DE MÁXIMO 1024 BYTES Y SE DECODIFICAN USANDO UTF-8
            print(decrypt(msj,10))                      #SE DESENCRIPTA CON CIFRADO CÉSAR

        except:                                         #EN CASO DE QUE HAYA ALGÚN ERROR...
            print("Desconectando del servidor...")
            client.close()
            break


hilorecibir = threading.Thread(target=recibir)          #UN HILO SE EJECUTA SIEMPRE Y SE ENCARGA DE RECIBIR MENSAJES
hilorecibir.start()                                     #SE INICIA EL HILO


while True:                          #CLIENTE ESCUCHANDO SIEMPRE A USUARIO PARA MANDAR MENSAJES AL SERVIDOR
    msj=input('>')                   #MENSAJE QUE ESCRIBE EL USUARIO
    if msj:                          #EN CASO DE QUE EL USUARIO HAYA ESCRITO UN MENSAJE
        if msj.upper()=="FIN":       #SI USUARIO ESCRIBE FIN --> SE TERMINA LA CONEXIÓN
            client.close()
            break

        else:
            msjsinencriptar=f"{nombre}: {msj}"      #SE CONCATENA EL NOMBRE DE USUARIO CON EL MENSAJE
            msjencriptado=encriptar(msjsinencriptar,10).encode("utf-8")     #SE ENCRIPTA EL MENSAJE USANDO CIFRADO CÉSAR CON DESPLAZAMIENTO 10
        #    print(msjencriptado)        #COMPROBACIÓN DE QUE SÍ ENCRIPTA
            client.sendall(msjencriptado)           #SE ENVÍA EL MENSAJE ENCRIPTADO AL SERVIDOR
        