import socket
import threading

ipclient=input("Escribe la IP del servidor: ")
port=8000

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect((ipclient,port))


nombre=input("Escribe tu nombre de usuario: ")

def recibir():
    while True:
        try:
            msj=client.recv(1024).decode('utf-8')
            print(msj)

        except:
            print("Desconectando del servidor...")
            client.close()
            break


hilorecibir = threading.Thread(target=recibir)
hilorecibir.start()

while True:
    msj=input('>')
    if msj:
        if msj.upper()=="FIN":
            client.close()
            
            break
        else:
            client.sendall(f"{nombre}: {msj}".encode("utf-8"))
        

#hiloenviar.start()
#hiloenviar = threading.Thread(target=enviar)