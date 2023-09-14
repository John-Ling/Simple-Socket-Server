import socket as s
import sys

def main():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    with s.socket(s.AF_INET, s.SOCK_STREAM) as socket:
        try:
            socket.connect((HOST, PORT))
            data = socket.recv(1024)
            print(data.decode())
            print("Enter IP and port to connect to")
            selected = str(input(">> ")).encode()
            socket.sendall(selected)

            status = socket.recv(1024)
            if status == b"$CONNECTION_FAILURE":
                print("Failed to Connect")
            elif status == b"$CONNECTION_SUCCESS":
                print("Connected")
                communication_loop(socket)
        except KeyboardInterrupt:
            print("Shutting")
        finally:
            socket.sendall(b"$DISCONNECT")

    return

def communication_loop(socket):
    send = str(input(">> ")).encode()
    socket.sendall(send)
    if send == b"$DISCONNECT":
        print("Disconnecting")
        return

    while True:
        data = socket.recv(1024)

        if data == b"$DISCONNECT":
            print("Client Disconnected")
            break

        print(data.decode())
        send = str(input(">> ")).encode()
        socket.sendall(send)
        if send == b"$DISCONNECT":
            print("Disconnecting")
            break
    print("Connection Terminated")


if __name__ == "__main__":
    main()