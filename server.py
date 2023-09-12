import socket as s
import sys
import threading
import time

# todo
# add graceful shutdown

def main():
    HOST = None
    PORT = None

    if not HOST:
        HOST = sys.argv[1]
    
    if not PORT:
        PORT = int(sys.argv[2])

    server = Server(HOST, PORT)
    input()
    server.end()
    print("Ended")
    return

class Server:
    def __init__(self, serverAddress, serverPort):
        self.__HOST = serverAddress
        self.__PORT = serverPort
        self.__OPERATOR_PORT = 2000 # used by management console to connect
        self.threads = []
        self.__endThread = False

        self.listeningSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.listeningSocket.bind((self.__HOST, self.__PORT))

        self.operatorSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.operatorSocket.bind((self.__HOST, self.__OPERATOR_PORT))
        
        # start listening thread
        self.listeningThread = threading.Thread(target=self.listen, args=(self.listeningSocket, False))
        self.listeningThread.start()

        self.operatorThread = threading.Thread(target=self.listen, args=(self.operatorSocket, True))
        self.operatorThread.start()

    def end(self):
        self.__endThread = True
        print("Ending...")
        print(threading.active_count())
        self.listeningThread.join(timeout=5)
        print("Completed")
        print(threading.active_count())
        return
    
    def listen(self, socket, operator):
        print("Starting listening thread")
        with socket:
            socket.listen()
            while not self.__endThread:
                clientSocket, address = socket.accept()
                print(f"Received connection {address}")

                target = self.handle_client

                if operator:
                    target = self.handle_operator

                threading.Thread(target=target, args=(clientSocket, address)).start()
        return

    
    def handle_client(self, clientSocket, address):
        # display message if management console has not engaged conversation
        while not self.__endThread:
            time.sleep(1)
            clientSocket.sendall(b"No one is online right now")
        clientSocket.sendall(b"Shutting down")
        clientSocket.close()
        return
    
    def handle_operator(self, operatorSocket, address):
        operatorSocket.sendall(b"Welcome operator")
        while not self.__endThread:
            pass
        operatorSocket.sendall(b"Shutting down")
        operatorSocket.close()
        return


    def display_active_connections(self):
        return [thread for thread in self.threads]

    def get_host(self):
        return self.__HOST
    
    def get_port(self):
        return self.__PORT


if __name__ == "__main__":
    main()