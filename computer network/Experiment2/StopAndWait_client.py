import socket
import time
import random
# 决定本地还是联机
Method = 'local'
if Method == 'local':
    serverAddress = ('localhost', 11000)
else:
    serverAddress = ('172.30.232.112', 11000)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(serverAddress)
# 设置任务参数
arrivedTime = 0
timeoutMax = 0.5
timeoutNum = 0.0
executeTime = 10  # 发送的数据包的数量
lossRate = 0.5    # 丢失率
# 用随机插入列表来决定何时丢失包
# 先创建大小与要发送的数据包等大的列表
sendQueue = [1 for _ in range(1, executeTime + 1)]
# 随机插入
for i in range(0, int(executeTime * lossRate)):
    while 1:
        indexList = random.randint(2, executeTime-1)
        if sendQueue[indexList] != indexList:
            sendQueue[indexList] = indexList
            break
# print(int(executeTime * lossRate))
# print(len(sendQueue))
startTime = time.time()
for i in sendQueue:
    # cmd = input("input:")
    if i == 1: # 未发生丢包时
        clientSocket.send("arrived".encode())
        response = clientSocket.recv(1024)
        arrivedTime += 1
        print(f"the {arrivedTime} times of response:", response.decode())
    else: # 发生丢包时
        timeoutBegin = time.time()
        while time.time() - timeoutBegin < timeoutMax:
            clientSocket.send("loss".encode())
            response = clientSocket.recv(1024)
            if response.decode() == '0':
                continue
        timeoutNum += 1
        arrivedTime += 1
        clientSocket.send("arrived".encode())
        response = clientSocket.recv(1024)
        print(f"the {int(timeoutNum)} times of response after time out:", response.decode())
endTime = time.time()
totalTime = endTime - startTime
# 计算并输出结果
print("the numbers of packet is", executeTime)
print("total time is", totalTime)
print("the packet loss rate is ", timeoutNum / executeTime)
print("average time of RTT is", (totalTime - timeoutNum * timeoutMax) / executeTime)
clientSocket.send("end".encode())
clientSocket.close()