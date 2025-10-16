import socket
import time
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddress = ('localhost', 11220)
serverSocket.bind(serverAddress)
while 1:
    request, client = serverSocket.recvfrom(1024)
    if request.decode() == "1":
        response = "GET!"
        waitTime = time.time()
        while time.time() - waitTime < 0.1:
            continue
        serverSocket.sendto(response.encode(), client)
    elif request.decode() == "end":
        exit()
    else:
        response = "loss"
        serverSocket.sendto(response.encode(), client)