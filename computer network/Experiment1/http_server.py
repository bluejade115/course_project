import socket
# 选择方法 web 或者 client
Method = 'web'

serverAddress = ('', 12000)
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(serverAddress)
Server.listen(1)
print("listening")
client, addr = Server.accept()
print("Connected!")

while True:
    request = client.recv(4096).decode()
    if Method == 'web': # web模式
        # 分割request 获取头
        headers = request.split('\n')
        # 取文件名
        filename = headers[0].split()[1]
        if filename == "/index.html":
            # index.html 为已写好的文件
            with open("index.html", 'r') as file:
                content = file.read()
            response_headers = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
            client.sendall(response_headers.encode() + content.encode())
        else:
            response_headers = 'HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n'
            # 编写html内容
            content = "<html><body><h1>404 Not Found</h1></body></html>"
            client.sendall(response_headers.encode() + content.encode())
    else: # client 模式
        if request == "index.html":
            response = "hello client!\r\n"
        elif request == "end":
            client.close()
            break
        else:
            response = "404 NOT FOUND\r\n"

    print("sending")




