import socket as s
import sys

HEADER_SIZE = 4
BUFFER_SIZE = 1024

def main():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    with s.socket(s.AF_INET, s.SOCK_STREAM) as socket:
        try:
            try:
                socket.connect((HOST, PORT))
            except ConnectionRefusedError:
                print(f"Could not connect to {HOST}:{PORT}")
                quit()
            data = receive_message(socket)
            print(data.decode())
            print("Enter IP and port to connect to")
            selected = str(input(">> ")).encode()
            send_message(socket, selected)

            status = receive_message(socket)
            if status == b"$CONNECTION_FAILURE":
                print("Failed to Connect")
            elif status == b"$CONNECTION_SUCCESS":
                print("Connected")
                communication_loop(socket)
        except KeyboardInterrupt:
            print("Shutting")

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
    send = str(input(">> ")).encode()
    send_message(socket, send)
    if send == b"$DISCONNECT":
        print("Disconnecting")
        return

    while True:
        data = receive_message(socket)

        if data == b"$DISCONNECT":
            print("Client Disconnected")
            break

        print(data.decode())
        send = str(input(">> ")).encode()
        send_message(socket, send)
        if send == b"$DISCONNECT":
            print("Disconnecting")
            break
    print("Connection Terminated")

if __name__ == "__main__":
    main()