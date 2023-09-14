import sys
import socket as s

def main():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    operatorConnected = False

    with s.socket(s.AF_INET, s.SOCK_STREAM) as socket:
        print(f"Connecting to {HOST}:{PORT}")
        socket.connect((HOST, PORT))

        # try:
        #     data = socket.recv(1024)
        #     if data == b"$OPERATOR_CONNECT":
        #         print("Operator Connected")
        #         operatorConnected = True
        #     elif data == b"$OPERATOR_OFFLINE":
        #         print("Operator Offline")
        #         # wait until operator connects or user exits
        #         data = socket.recv(1024)
        #         if data == b"$OPERATOR_CONNECT":
        #             pass
        # except KeyboardInterrupt:
        #     print("Shutting")
        #     socket.sendall(b"$DISCONNECT")

        try:
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
                    print("Operator Offline")
                    continue
        except KeyboardInterrupt:
            print("Shutting")
        finally:
            socket.sendall(b"$DISCONNECT")
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