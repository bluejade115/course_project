import socket
# 决定本地还是联机
Method = 'local'
if Method == 'local':
    serverAddress = ('localhost', 11000)
else:
    serverAddress = ('172.30.232.112', 11000)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(serverAddress)
while 1:
    cmd = input("input the name of files that you want:")
    clientSocket.send(cmd.encode())
    response = clientSocket.recv(1024)
    if response.decode() != "error": # 正确接收文件
        print(response.decode())
        print("******received file has been saved in FTP_File.txt******")
        with open("FTP_File.txt", 'w') as file: # 存储文件
            file.write(response.decode())
    else:
        print(response.decode()) # 无请求文件
    cmd = input("please input y to restart or input end to stop:")
    if cmd == "y":
        continue
    elif cmd == "end":
        clientSocket.send("end".encode())
        clientSocket.close()
        break

