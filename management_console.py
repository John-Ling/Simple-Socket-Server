import socket as s
import threading
import sys

def main():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    with s.socket(s.AF_INET, s.SOCK_STREAM) as socket:
        socket.connect((HOST, PORT))
        data = socket.recv(1024)
        print(f"{data!r}")
        selectedPort = str(input(">"))
        socket.sendall(bytes(selectedPort, "utf-8"))

        while True:
            data = socket.recv(1024)
            print(f"Received: {data!r}")
            send = str(input(">"))
            if send == "$DISCONNECT":
                break
            socket.sendall(bytes(send, "utf-8"))
            

    return


if __name__ == "__main__":
    main()