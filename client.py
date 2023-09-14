class Client:
    def __init__(self, socket):
        self.operatorConnected = False
        self.socket = socket

class Operator:
    def __init__(self, socket):
        self.socket = socket