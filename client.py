import socket
import threading
import tkinter

host = '127.0.0.1'
port = 8000

def receiveMsg():
    global msgList
    while True:
        msg=ClientSocket.recv(2048).decode('utf-8')
        if msg in serverMsgs:
            dispalyMsg(msg)
        else:
            setLabel(msg)

      
def sendMsg(event=None):   
    if msgToSend.get()=='quit':
        ClientSocket.send(str.encode('quit'))
        ClientSocket.close()
        root.quit()
    try:    
        msg=float(msgToSend.get())
        msgToSend.set('')
        ClientSocket.send(str.encode(str(msg)))
    except ValueError:
        dispalyMsg('Enter numbers only')
         

def onWindowClosing(event=None):
    msgToSend.set('quit')
    sendMsg()


#UI
root=tkinter.Tk()
root.geometry('400x200')
root.title('Auction portal')

bidFrame=tkinter.LabelFrame(root,text='CURRENT BID',labelanchor='n')
bidFrame.pack(padx=20)
currentBidInfo=tkinter.Label(bidFrame,text='0.0',width=15)
currentBidInfo.pack(padx=20,pady=20)
def setLabel(msg):
    currentBidInfo['text']=msg
    currentBidInfo.pack(padx=20,pady=20)

msgFrame=tkinter.LabelFrame(root,text='',bd=0)
msgFrame.pack(padx=20)
msgDisplay=tkinter.Label(msgFrame, text='')
msgDisplay.pack(padx=40,pady=20)
def dispalyMsg(msg):
    msgDisplay['text']=msg
    msgDisplay.pack(padx=40,pady=20)

msgToSend = tkinter.StringVar() 
msgToSend.set('')
entryField = tkinter.Entry(root, textvariable=msgToSend, bd=0, justify='center')
entryField.bind("<Return>", sendMsg)
entryField.pack()

sendButton = tkinter.Button(root, text="BID", command=sendMsg, activebackground='#14c07b', bg='#16f29f', fg='#000', activeforeground='#000', bd=0, width=9, height=1)
sendButton.pack(pady=5)

root.protocol("WM_DELETE_WINDOW", onWindowClosing)


#main
serverMsgs=['Start bidding','Bid successful','Bid not placed! Place bid higher than current bid']
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
    print('You are in the auction')
    clientThread=threading.Thread(target=receiveMsg)
    clientThread.start()
    tkinter.mainloop()
except socket.error as e:
    print(str(e))
