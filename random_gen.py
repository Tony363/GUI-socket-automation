import sys
import socket
import selectors
import types
import random
import time
from tkinter import *

def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print('starting connection', connid, 'to', server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=connid,
                                     msg_total=sum(len(m) for m in messages),
                                     recv_total=0,
                                     messages=list(iter(messages)),
                                     outb=b'')
        sel.register(sock, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    # print(next(data.outb))
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print('received', repr(recv_data), 'from connection', data.connid)
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print('closing connection', data.connid)
            sel.unregister(sock)
            sock.close()
            sys.exit()

    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
            print(data.outb)
        if data.outb:
            print('sending', repr(data.outb), 'to connection', data.connid)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
            
            


def nClick():
    global counter
    counter += 1
            
    if counter > 100000:
        stop = Label(text="exceeded 5 digits").pack()
        time.sleep(1)
        sys.exit()
        
    events = sel.select(timeout=None)
   
    for key,mask in events:
        # print(messages)
        service_connection(key,mask)
        
    mButton1.config(text = counter)



global counter
counter = 1000
root = Tk()
root.geometry("200x200")
root.title("My Button Increaser")

messages = [bytes(f'{i}',encoding='utf8') for i in range(1000,100000)]
sel = selectors.DefaultSelector()
start_connections('',8000,2)

mButton1 = Button(text = counter, command = nClick, fg = "darkgreen", bg = "white")
mButton1.pack()

root.mainloop()






    



    
