from client import Client, Operator

import socket as s
import sys
import threading


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
    def __init__(self, host, port):
        self.__HOST = host
        self.__PORT = port
        self.__OPERATOR_PORT = 2000 # used by management console to connect
        self.__BUFFER_SIZE = 1024
        self.__HEADER_SIZE = 4
        self.clients = {}
        self.__endThread = False

        self.listeningSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.listeningSocket.bind((host, port))

        self.operatorSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.operatorSocket.bind((host, self.__OPERATOR_PORT))
        
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
    

    def receive_data(self, socket):
        # reads n number of bytes from socket where n is the length of the message
        # in the packet header

        header = socket.recv(self.__HEADER_SIZE)

        messageLength = int.from_bytes(header[0:self.__HEADER_SIZE], "big")
        chunks = []
        received = 0
        while received < messageLength:
            chunk  = socket.recv(min(messageLength - received, self.__BUFFER_SIZE))
            
            if not chunk:
                raise RuntimeError
            chunks.append(chunk)
            received += len(chunk)
    
        return b"".join(chunks)

    
    def listen(self, socket, operator):
        print("Starting Listening Thread")
        with socket:
            socket.listen()
            while not self.__endThread:
                clientSocket, address = socket.accept()
                handlingMethod = self.handle_client

                if operator:
                    client = Operator(clientSocket)
                    handlingMethod = self.handle_operator
                else:
                    client = Client(clientSocket)

                print(f"Received Connection {address}")
                communicationThread = threading.Thread(target=handlingMethod, args=(client,))
                communicationThread.start()
        return

    def handle_client(self, client):
        host, port = client.socket.getpeername()
        socketString = f"{host}:{port}"
        self.clients[socketString] = client
        sent = False

        # put client in "waiting room" until operator connects and selects them
        while not self.__endThread:
            # hand off control to the operator and begin_communication() function
            if client.operatorConnected:
                try:
                    client.socket.sendall(b"$OPERATOR_CONNECT")
                except: # remove stale socket connection if client has already left
                    del self.clients[socketString]
                break

            if not sent:
                client.socket.sendall(b"$OPERATOR_NOT_ONLINE")
                sent = True

        if socketString in self.clients:
            del self.clients[socketString]
        return
    
    def handle_operator(self, operator):
        availableSockets = ""
        for client in self.clients.values():
            address, port = client.socket.getpeername()
            availableSockets += f"{address}:{port}\n"

        operator.socket.sendall(f"Welcome Operator\nAvailable Connections\n{availableSockets}".encode())
        # selectedAddress = operator.socket.recv(1024).decode()
        selectedAddress = self.receive_data(operator.socket).decode()
        if selectedAddress in self.clients:
            client = self.clients[selectedAddress]
            client.operatorConnected = True

            operator.socket.sendall(b"$CONNECTION_SUCCESS")

            self.begin_communication(client, operator)
        return

    def begin_communication(self, client, operator):
        # begin two-way communication between operator and client
        try:
            while not self.__endThread:
                operatorMessage = self.receive_data(operator.socket)
                if operatorMessage == b"$DISCONNECT":
                    client.socket.sendall(b"$DISCONNECT")
                    break
                client.socket.sendall(operatorMessage)
                # clientMessage = client.socket.recv(1024)
                clientMessage = self.receive_data(client.socket)
                if clientMessage == b"$DISCONNECT":
                    operator.socket.sendall(b"$DISCONNECT")
                    break
                operator.socket.sendall(clientMessage)
        except:
            print("Connection Severed")
            try:
                operator.socket.sendall(b"$DISCONNECT")
            except:
                pass
            
            try:
                client.socket.sendall(b"$DISCONNECT")
            except:
                pass
        finally:
            client.socket.close()
            operator.socket.close()
        return

    def get_host(self):
        return self.__HOST
    
    def get_port(self):
        return self.__PORT


if __name__ == "__main__":
    main()