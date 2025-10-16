import socket
# 选择模式
Method = 'local'
if Method == 'local':
    serverAddress = ('', 11000)
else:
    serverAddress = ('172.30.232.125', 11000)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(serverAddress)
serverSocket.listen(1)
clientSocket, clientAddress = serverSocket.accept()
print("Connected")
print("client address is", clientAddress)
# 处理丢包和未丢包的情况
while 1:
    request = clientSocket.recv(1024)
    if request.decode() == 'end':
        serverSocket.close()
        break
    elif request.decode() == "arrived":
        clientSocket.send("ACK".encode())
    elif request.decode() == "loss":
        clientSocket.send('0'.encode()) # 回复0 模拟丢包


