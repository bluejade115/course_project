import socket
import time
import random
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 决定本地还是联机
Method = 'local'
if Method == 'local':
    serverAddress = ('localhost', 11000)
else:
    serverAddress = ('172.30.232.112', 11000)
# 生成随机列表 以决定何时发送包超时
sendNum = 10
lossNum = random.randint(1, 5)
sendQueue = [1 for i in range(0, sendNum)]
for i in range(0, lossNum):
    while 1:
        indexList = random.randint(2, sendNum - 1)
        if sendQueue[indexList] != indexList:
            sendQueue[indexList] = indexList
            break
startTime = time.time()
# 遍历列表发送包
for i in sendQueue:
    if i == 1: # 无超时时
        ping_message = "1"
        RTT_start = time.time()
        clientSocket.sendto(ping_message.encode(), serverAddress)
        pong_response, server = clientSocket.recvfrom(1024)
        RTT_end = time.time()
        print(pong_response.decode()," delay=",RTT_end-RTT_start-0.1) # 计算时延
    else: # 超时
        waitTime = time.time()
        ping_message = f"{i}"
        while time.time() - waitTime < 1:
            clientSocket.sendto(ping_message.encode(), serverAddress)
            pong_response, server = clientSocket.recvfrom(1024)
            if pong_response.decode() == 'loss':
                continue
        print("Request timed out")

endTime = time.time()
clientSocket.sendto("end".encode(), serverAddress)
print("total time is", endTime - startTime-1)
print("RTT is", ( endTime - startTime - lossNum) / (sendNum - lossNum))