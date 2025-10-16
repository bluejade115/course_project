import socket
serverAddress = ('', 15115)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(serverAddress)
serverSocket.listen(5)
clientSocket, clientAddress = serverSocket.accept()
while 1:
    request = clientSocket.recv(1024)
    if request.decode() == "letter": # 文件存在则读取文件返回客户端
        with open("letter.txt", 'r') as file:
            response = file.read()
        clientSocket.send(response.encode())
    elif request.decode() == "end":
        clientSocket.close()
        break
    else:
        response = "error" #文件不存在
        clientSocket.send(response.encode())
