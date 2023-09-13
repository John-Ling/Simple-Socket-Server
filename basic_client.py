import sys
import socket

def main():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    operatorConnected = False

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        print(f"Connecting to {HOST}:{PORT}")
        clientSocket.connect((HOST, PORT))

        while True:
            try:
                data = clientSocket.recv(1024)
                if data == b"$DISCONNECT":
                    break
                
                if data == b"$OPERATOR_CONNECT":
                    print("Operator Connected")
                    operatorConnected = True
                    data = clientSocket.recv(1024)
                
                if not operatorConnected:
                    print("Operator not online")
                    continue
                
                print(f"Received data: {data!r}")
                send = str(input(">"))

                if send == "$DISCONNECT":
                    break

                clientSocket.sendall(bytes(send, "utf-8"))
            except KeyboardInterrupt:
                break

    return

if __name__ == "__main__":
    main()