import sys
import socket
import selectors
import types
import random
import time
import json
from tkinter import *

def service_connection(key, mask,sel,messages):
    sock = key.fileobj
    data = key.data
    # print(next(data.outb))
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read

        if 'number used' in str(repr(recv_data)):
            guiFrame.messages = guiFrame.messages[1:]
            print('FUCKq!')

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


def start_connections(host, port, num_conns,sel,messages,bytes_dic):
    print(type(messages),type(bytes_dic))
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
                                    messages=messages,
                                    outb=b'')
        sel.register(sock, events, data=data)



class GUI(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        
        self.grid()
        self.data = {}
        self.bytes_dic = json.dumps(self.data).encode('utf-8')

        self.counter = 1000

        ##!!!!!!!!!!!!!!!!!
        self.messages = [bytes(f'{i}',encoding='utf8') for i in zip(range(1000,100000),self.bytes_dic)]
        
        self.sel = selectors.DefaultSelector()
        start_connections('',8000,1,self.sel,self.messages,self.bytes_dic)
        

        self.label1 = Label(master,text='label1')
        self.label1.grid()

        self.Entry1 = Entry(master)
        self.Entry1.grid()

        self.button1 = Button(master,height=1,width=10,text='Enter',command=self.get_entry1)
        self.button1.grid()

        self.label2 = Label(master,text='label2')
        self.label2.grid()

        self.Entry2 = Entry(master)
        self.Entry2.grid()

        self.button2 = Button(master,height=1,width=10,text='Enter',command=self.get_entry2)
        self.button2.grid()

        self.submit = Button(text = f'Submit {self.counter}', command = self.nClick, fg = "black", bg = "white")
        self.submit.grid()

    def change(self,Frame):
        Frame.pack_forget()
    def get_entry1(self):
        self.data['label1'] = self.Entry1.get()
        print(self.data)

    def get_entry2(self):
        self.data['label2'] = self.Entry2.get()
        print(self.data)

    def get_entry3(self):
        self.data['label3'] = self.Entry3.get()
        print(new_data)

    def get_entry4(self):
        self.data['label4'] = self.Entry4.get()
        print(self.data)
    
    def nClick(self):
        self.counter += 1   
        
        if self.counter > 100000:
            stop = Label(text="exceeded 5 digits").pack()
            time.sleep(1)
            sys.exit()    
        # start_connections('',8000,1,self.sel,self.messages)
        self.events = self.sel.select(timeout=None)
        for key,mask in self.events:
            service_connection(key,mask,self.sel,self.messages)   
        self.submit.config(text = f'Submit {self.counter}')

    def return_messages(self):
        return self.messages

# class newGUI(Frame):
#     def __init__(self,parent,controller):
#         Frame.__init__(self,parent)

 


if __name__ == "__main__":
    # messages = [bytes(f'{i}',encoding='utf8') for i in range(1000,100000)]  
    guiFrame = GUI()   
    guiFrame.mainloop()
   
   








    



    
