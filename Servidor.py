import socket
import threading as threading


host=socket.gethostbyname(socket.gethostname())
port=8000

socketserver=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socketserver.bind((host,port))
socketserver.listen()
    
print(f"El servidor se encuentra en: {socket.gethostbyname(socket.gethostname())}:{port}")      #SE DA IP:PUERTO DEL SERVIDOR
    
print("Esperando conexión con clientes...")

clientes=[]
    

def broadcast(msj,remitente):
    for client in clientes:
        if client != remitente:
            try:
                client.sendall(msj.encode("utf-8"))
            except:
                clientes.remove(client)
                print(f"Desconectando a {client} por un error en la conexión")

def recibiryenviar(client,address):
    clientes.append(client)
    print(f"Conexión establecida desde {address}") 
    
    while True:
        try:
            msj=client.recv(1024).decode("utf-8")
            if msj:
                print(f"Mensaje recibido desde {address}: {msj}")
                broadcast(msj,client)
        except:
            broadcast(f"{client} se ha desconectado", client)
            print(f"Conexión cerrada desde {address}")
            clientes.remove(client)
            break


while True:
    client,address=socketserver.accept()
    hilo = threading.Thread(target=recibiryenviar,args=(client,address))
    hilo.start()