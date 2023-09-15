import sys
import socket as s

HEADER_SIZE = 4
BUFFER_SIZE = 1024

def main():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    operatorConnected = False

    with s.socket(s.AF_INET, s.SOCK_STREAM) as socket:
        print(f"Connecting to {HOST}:{PORT}")
        try:
            socket.connect((HOST, PORT))
        except ConnectionRefusedError:
            print(f"Could not connect to {HOST}:{PORT}")
            quit()
        
        # waiting room code
        while True:
            data = receive_message(socket)
            if data == b"$DISCONNECT":
                break
            
            if data == b"$OPERATOR_CONNECT":
                operatorConnected = True
                print("Operator Connected")
                communication_loop(socket)
                break
            
            if not operatorConnected:
                print("Operator Offline")
    return

def send_message(socket, message):
    header = len(message).to_bytes(4, "big")
    socket.sendall(header + message)
    return

def receive_message(socket):
    header = socket.recv(HEADER_SIZE)
    messageLength = int.from_bytes(header[0:HEADER_SIZE], "big")
    chunks = []
    received = 0
    while received < messageLength:
        chunk  = socket.recv(min(messageLength - received, BUFFER_SIZE))
        
        if not chunk:
            raise RuntimeError
        chunks.append(chunk)
        received += len(chunk)

    return b"".join(chunks)

def communication_loop(socket):
    while True:
        data = receive_message(socket)
        if data == b"$DISCONNECT":
            print("Operator Disconnected")
            break

        print(data.decode())
        send = str(input(">> ")).encode()
        send_message(socket, send)
        if send == b"$DISCONNECT":
            break
    
    print("Connection Terminated")
    return

if __name__ == "__main__":
    main()