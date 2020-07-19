from socket import AF_INET, socket, SOCK_STREAM,gethostname
from threading import Thread


clients = {}

header = 10

s = socket(AF_INET, SOCK_STREAM)
s.bind((gethostname(), 1235))
s.listen()
def accept_client():
    while True:
        client, adress = s.accept()
        msg = 'hello in this server,write your name and press enter'
        msg =  f"{len(msg):<{header}}" +msg
        client.send(bytes(msg,'utf8'))
        Thread(target=send_msg, args=(client,)).start()
        
def send_msg(client):
    name = client.recv(1024).decode("utf8")
    name = name[header:]
    welcome = 'Welcome %s! If you ever want to quit, send quit to exit.' % name
    welcome = f"{len(welcome):<{header}}" + welcome
    client.send(bytes(welcome, "utf8"))
    msg ="%s has joined the chat!" % name
    send_msg_to_the_group(msg)
    clients[client] = name
    
    while True :
        full_msg = ''
        new_msg= True
        while True:
            msg = client.recv(16)
            if new_msg:
                print(msg[:header])
                msg_l = int(msg[:header])
                new_msg = False
            full_msg += msg.decode('utf-8')
            if len(full_msg) - header == msg_l:
                if full_msg[header:] == 'quit':
                    del clients[client]
                    send_msg_to_the_group(f'{name} has left the group')
                    client.close()
                else :
                    print(full_msg[header:])
                    send_msg_to_the_group(full_msg[header:],name)
                    new_msg = True
                    full_msg = ''
    


    
                
                
                
def send_msg_to_the_group(msg,name=""):
    if len(clients) > 0 :
        for sock in clients:
            msg_send = f"{name}:{msg}"
            msg_send =f"{len(msg_send):<{header}}"+msg_send
            print(msg)
            sock.send(bytes(msg_send,'utf-8'))
        
        
        
        
if __name__ == "__main__":
    s.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_client())
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    s.close()