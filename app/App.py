from .Config import *
from .Constants import *
from socket import *

class App(object):
    '''
    Sets up and runs a Pygame application.
    '''
    
    def __init__(self, app_directory):
        self.app_directory = app_directory
        self.socket = socket()

        self.openSocket()
        self.joinChannel()
        self.listen()

    def openSocket(self) -> None:
        self.socket.connect((HOST, PORT))
        self.socket.send(("PASS " + KEYPASS + "\r\n").encode("UTF-8"))
        self.socket.send(("NICK " + NICK + "\r\n").encode("UTF-8"))
        self.socket.send(("JOIN #" + CHANNEL + "\r\n").encode("UTF-8"))

    def sendMessage(self, message: str) -> None:
        tempMessage = "PRIVMSG #" + CHANNEL + " :" + message + "\r\n"
        self.socket.send(tempMessage.encode("UTF-8"))
        print ("Sent: " + tempMessage)


    def joinChannel(self) -> None:
        readbuffer = ""
        loading = True
        while loading:
            readbuffer = readbuffer + self.socket.recv(BUFFER).decode("UTF-8")
            temp = readbuffer.split("\n")
            readbuffer = temp.pop()

            for line in temp:
                if ("End of /NAMES list" in line):
                    loading = False
        self.sendMessage("has joined the channel")
    
    def getUser(self, line: str) -> str:
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        return user

    def getMessage(self, line: str) -> str:   
        separate = line.split(":", 2)
        message = separate[2]
        return message.rstrip("\r\n")

    def listen(self) -> None:
        while True:
            readbuffer = ""
            readbuffer = readbuffer + self.socket.recv(BUFFER).decode("UTF-8")
            temp = readbuffer.split("\n")
            readbuffer = temp.pop()

            for line in temp:
                if "PING" in line: 
                    self.socket.send(line.replace("PONG").encode("UTF-8"))
                    break
            user = self.getUser(line)
            message = self.getMessage(line)

            if message == "hello": 
                self.sendMessage("Hello " + user + " and welcome")
