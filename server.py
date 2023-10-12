import socket
import sys
import threading
import time
import Data

host = '127.0.0.1'
port = 8000

clientList = {}

basePrice=float(100)
currentBid=basePrice
newBid=float(0)

def evaluateBid(newBid):
    global currentBid
    global basePrice
    if currentBid==basePrice:
        if newBid>=currentBid:
            currentBid=newBid
            basePrice=0.0
            return True
    elif currentBid>basePrice:
        if newBid>currentBid:
            currentBid=newBid
            return True
    return False


def sendEveryone(currentBid):
    txt=str(currentBid)
    for bidder in clientList:
        bidder.send(txt.encode('utf-8'))


def clientHandler(connection,address):
    connection.send(str.encode('Start bidding'))
    time.sleep(0.1)
    connection.send(str.encode(str(currentBid)))
    while True:
        msg=connection.recv(2048).decode('utf-8')
        if msg!='quit':
            newBid = float(msg)
            bidStatus=evaluateBid(newBid)
            if bidStatus==True: 
                print('Current bid: ',currentBid)
                Data.storeBid(clientList[connection],currentBid)        
                connection.send(str.encode('Bid successful'))
                sendEveryone(currentBid)
            else:
                connection.send(str.encode('Bid not placed! Place bid higher than current bid'))
                sendEveryone(currentBid)
        elif msg=='quit':
            connection.close()
            del clientList[connection]
            print('Disconnected from: ' + address[0] + ':' + str(address[1]))
            break


def acceptConnections(ServerSocket):
    Client, address = ServerSocket.accept()
    clientList[Client]=Client,address
    Data.storeClients(clientList)
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    threading.Thread(target=clientHandler, args=(Client,address,)).start()


def startServer(host, port):
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print(f'Server is listing on the port {port}...')
    ServerSocket.listen()   
    while True:
        acceptThread=threading.Thread(target=acceptConnections,args=(ServerSocket,))
        acceptThread.start()
        acceptThread.join()

startServer(host, port)
