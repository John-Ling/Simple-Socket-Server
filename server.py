import socket as s
import sys
import threading
import random
import time

# todo
# add graceful shutdown
# allow management console to perform 1-1 half-duplex communication with selected client

def main():
    HOST = None
    PORT = None

    if not HOST:
        HOST = sys.argv[1]
    
    if not PORT:
        PORT = int(sys.argv[2])

    server = Server(HOST, PORT)
    try:
        input()
    except KeyboardInterrupt:
        pass
    finally:
        server.end_server()
    return

class Server:
    def __init__(self, serverAddress, serverPort):
        self.__HOST = serverAddress
        self.__PORT = serverPort
        self.__OPERATOR_PORT = 2000 # used by management console to connect
        self.sockets = []
        self.__endThread = False
        self.operatorActive = False

        self.listeningSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.listeningSocket.bind((self.__HOST, self.__PORT))

        self.operatorSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.operatorSocket.bind((self.__HOST, self.__OPERATOR_PORT))
        
        # start listening thread
        self.listeningThread = threading.Thread(target=self.listen, args=(self.listeningSocket, False))
        self.listeningThread.daemon = True
        self.listeningThread.start()

        self.operatorThread = threading.Thread(target=self.listen, args=(self.operatorSocket, True))
        self.operatorThread.daemon = True
        self.operatorThread.start()

    def end_server(self):
        self.__endThread = True
        self.listeningThread.join(timeout=1)
        self.operatorThread.join(timeout=1)
        return
    
    def listen(self, socket, operator):
        print("Starting listening thread")
        with socket:
            socket.listen()
            while not self.__endThread:
                try:
                    clientSocket, address = socket.accept()
                    print(f"Received connection {address}")

                    target = self.handle_client
                    if operator:
                        target = self.handle_operator

                    communicationThread = threading.Thread(target=target, args=(clientSocket, address))

                    if not operator:
                        self.sockets.append(clientSocket)
                    communicationThread.start()
                except s.timeout:
                    pass
        return


    def handle_client(self, clientSocket, address):
        # display message if management console has not engaged conversation
        sent = False
        while not self.__endThread:
            if self.operatorActive:
                clientSocket.sendall(b"$OPERATOR_CONNECT")
                break
            else:
                if not sent:
                    clientSocket.sendall(b"No connection")
                    sent = True
        return
    
    def handle_operator(self, operatorSocket, address):
        self.operatorActive = True
        operatorSocket.sendall(bytes("Welcome operator", "utf-8"))
        clientSocket = random.choice(self.sockets)
        
        self.begin_communication(clientSocket, operatorSocket)

        operatorSocket.sendall(b"Shutting down")
        operatorSocket.close()
        return

    def begin_communication(self, clientSocket, operatorSocket):
        while not self.__endThread:
            operatorMessage = operatorSocket.recv(1024)
            clientSocket.sendall(operatorMessage)
            clientMessage = clientSocket.recv(1024)
            operatorSocket.sendall(clientMessage)
        
        return
            

    def get_host(self):
        return self.__HOST
    
    def get_port(self):
        return self.__PORT


if __name__ == "__main__":
    main()