import socket
import pickle

# Connection with server
class Connection:

  def __init__(self):
    self.infoToSend = {}
    self.host = ''
    self.port = 0

  def setHostAndPort(self, host, port):
    self.host = host
    self.port = port

  # Sends given information to server and server processes it
  def sendMouseOperation(self, **kwargs):
    for key, value in kwargs.items():
      self.infoToSend[key] = value

    print(self.host)
    print(self.port)
    s = socket.socket()
    s.connect((self.host, self.port))
    print(s.recv(1024).decode())
    s.send(pickle.dumps(self.infoToSend))
    s.close()

    self.infoToSend = {}