import sys
import socket

def main():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        print(f"Connecting to {HOST}:{PORT}")
        clientSocket.connect((HOST, PORT))
        while True:
            data = clientSocket.recv(1024)
            print(f"Received data: {data!r}")

    return

if __name__ == "__main__":
    main()