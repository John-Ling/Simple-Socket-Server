# Simple-Socket-Server
Made a socket server because I could.

## How to use
Users use basic_client.py to connect to the server and wait until an operator connects and selects them. 
An operator uses management_console.py on port 2000 (I specified this manually but changing that shouldn't be hard) and enters the IP:PORT combination of the machine they want to talk to.
Then the operator and client can send text to each other in half-duplex communication and either user can end the conversation by issuing $DISCONNECT.

## Specific Usage
server.py
```
python server.py {serverIP} {clientPort}
```

basic_client.py
```
python basic_client.py {serverIP} {clientPort}
```

management_console.py
```
python management_console.py {serverIP} {operatorPort}
```
