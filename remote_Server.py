import socket
from  threading import Thread
from pynput.mouse import Button, Controller
from screeninfo import get_monitors
from pynput.keyboard import Key, Controller

SERVER=None
PORT=8002
IP_ADDRESS="192.168.117.97"

screen_width=None
screen_height=None

keyboard=Controller()


def setup():
    print("\n\t\t\t\t\t*** Welcome TO Remote Mouse ***\n")
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS,PORT))
    SERVER.listen(10)
    print("\t\t\t\t SERVER IS WAITING FOR INCOMING CONNECTIONS...\n")
    getDeviceSize()
    acceptConnections()


def getDeviceSize():
    global screen_height
    global screen_width

    for v in get_monitors():
        screen_width=int(str(v).split(",")[2].strip().split('width=')[1])
        screen_height=int(str(v).split(",")[3].strip().split('height=')[1])


def recvMessage(client_socket):
    global keyboard

    while True:
        try:
            message=client_socket.recv(2048).decode()
            if(message):
                keyboard.press(message)
                keyboard.release(message)
                print(message)

        except Exception as error:
            pass        


def acceptConnections():
    global SERVER
    while True:
        client_socket,addr=SERVER.accept()
        print(f"CONNECTION established with{client_socket}: {addr}")
        thread1=Thread(target=recvMessage,args=(client_socket,))
        thread1.start()


setup()            
