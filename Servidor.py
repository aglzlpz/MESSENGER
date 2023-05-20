import socket
import threading as threading


host=socket.gethostbyname(socket.gethostname())         #IP PRIVADA DEL SERVIDOR
port=8000                                               #PUERTO DEL SERVIDOR DONDE SE ATIENDEN PETICIONES

socketserver=socket.socket(socket.AF_INET,socket.SOCK_STREAM)       #SE CREA EL SOCKET
socketserver.bind((host,port))                                      #SE VINCULA EL SOCKET A UNA IP Y UN PUERTO
socketserver.listen()                  #EL SERVIDOR EMPIEZA A ESCUCHAR DESDE EL PUERTO PARA ATENDER LAS CONEXIONES DEL CLIENTE
    
print(f"El servidor se encuentra en: {host}")      #SE DA IP DEL SERVIDOR
    
print("Esperando conexión con clientes...")

clientes=[]             #LISTA DE CLIENTES
    

def broadcast(msj,remitente):           #FUNCIÓN QUE ENVÍA MENSAJE A TODOS LOS CLIENTES MENOS A REMITENTE
    for client in clientes:     
        if client != remitente:         #SI EL CLIENTE NO ES EL REMITENTE
            try:
                client.sendall(msj.encode("utf-8"))         #SE ENVÍA EL MENSAJE
            except:
                clientes.remove(client)                     #SI HAY ALGÚN ERROR, SE ELIMINA AL CLIENTE DE LA LISTA DE CLIENTES
                print(f"Desconectando a {address} por un error en la conexión")

def recibiryenviar(client,address):     #FUNCIÓN QUE ESTABLECE CONEXIÓN CON UN CLIENTE Y SE ENCARGA DE DISTRIBUIR EL TRÁFICO
    clientes.append(client)             #SE AÑADE EL NUEVO CLIENTE A LA LISTA DE CLIENTES
    print(f"Conexión establecida desde {address}") 
    
    while True:                         #BUCLE INFINITO
        try:
            msj=client.recv(1024).decode("utf-8")           #SE RECIBEN LOS MENSAJES ENCRIPTADOS DEL CLIENTE (MÁXIMO 1024 BYTES)
            if msj:                                         #SI HAY UN MENSAJE
                print(f"Mensaje recibido desde {address}: {msj}")       #SE IMPRIME EN PANTALLA EL MENSAJE ENCRIPTADO
                broadcast(msj,client)                       #EL MENSAJE RECIBIDO POR EL SERVIDOR SE ENVÍA A TODOS LOS CLIENTES
        except:
            broadcast(f"{client} se ha desconectado", client)
            print(f"Conexión cerrada desde {address}")
            clientes.remove(client)         #EN CASO DE ERROR SE AVISA DE LA DESCONEXIÓN Y SE ELIMINA AL CLIENTE DE LA LISTA
            break                           #SE ACABA EL BUCLE


while True:                 #POR SIEMPRE
    client,address=socketserver.accept()            #ACEPTAR LAS CONEXIONES QUE LLEGAN AL SOCKET
    hilo = threading.Thread(target=recibiryenviar,args=(client,address))        #SE CREA UN HILO POR CADA CLIENTE QUE EJECUTA LA FUNCION RECIBIRYENVIAR()
    hilo.start()            #SE EJECUTA EL HILO