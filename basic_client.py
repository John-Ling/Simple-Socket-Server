import sys
import socket as s

def main():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    operatorConnected = False

    with s.socket(s.AF_INET, s.SOCK_STREAM) as socket:
        print(f"Connecting to {HOST}:{PORT}")
        socket.connect((HOST, PORT))
        statusVisible = False
        # waiting room code
        while True:
            data = socket.recv(1024)
            if data == b"$DISCONNECT":
                break
            
            if data == b"$OPERATOR_CONNECT":
                operatorConnected = True
                print("Operator Connected")
                communication_loop(socket)
                break
            
            if not operatorConnected:
                if not statusVisible:
                    print("Operator Offline")

        print("Shutting")
    return

def communication_loop(socket):
    while True:
        data = socket.recv(1024)
        if data == b"$DISCONNECT":
            break

        print(data.decode())
        send = str(input(">> ")).encode()
        socket.sendall(send)
        if send == b"$DISCONNECT":
            break
    
    print("Disconnecting")
    return

if __name__ == "__main__":
    main()