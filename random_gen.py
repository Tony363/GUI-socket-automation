import sys
import socket
import selectors
import types
import random
import time
import json
import requests
from tkinter import *
from tkinter.messagebox import showinfo

def service_connection(key, mask,sel,messages,counter):
    sock = key.fileobj
    data = key.data
    # print(data)
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read

        if 'number used' in str(repr(recv_data)):
            guiFrame.messages = guiFrame.messages.pop('')
            print('FUCKq!')

        if recv_data:
            print('received', repr(recv_data), 'from connection', data)
            # data += len(recv_data)
        if not recv_data or data == data.msg_total:
            print('closing connection', data)
            sel.unregister(sock)
            sock.close()
            sys.exit()

    if mask & selectors.EVENT_WRITE:
        if not data and data.messages:
            data = data.messages.pop(0)
            # print(data.outb)
        if data:
            print('sending', repr(data), 'to connection', data)
            sent = sock.send(data)  # Should be ready to write
            # data.outb = data.outb[sent:]


def start_connections(host, port, num_conns,sel,messages):
    print(type(messages))
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print('starting connection', connid, 'to', server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # data = types.SimpleNamespace(connid=connid,
        #                             msg_total=sum(len(m) for m in messages),
        #                             recv_total=0,
        #                             messages=iter(messages),
        #                             outb=b'')
        data1 = json.dumps(messages).encode('utf-8')
        sel.register(sock, events, data=data1)



class GUI(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        
        self.grid()
        self.counter = 1000
        self.data = {'number':[],'label1':[],'label2':[]}
        # self.messages = [bytes(f'{i}',encoding='utf8') for i in range(1000,100000)] 
        self.messages = {i:dict() for i in range(1000,100000)}

        self.sel = selectors.DefaultSelector()
        # start_connections('',8000,1,self.sel,self.messages)
        

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

        self.submit = Button(text = f'Submit {self.counter}', command = self.send_data, fg = "black", bg = "white")
        self.submit.grid()

    def get_entry1(self):
        self.messages[self.counter]['label1'] = self.Entry1.get()
        self.data['label1'].append(self.Entry1.get())
        # print(self.messages)
        print(self.data)

    def get_entry2(self):
        self.messages[self.counter]['label2'] = self.Entry2.get()
        self.data['label2'].append(self.Entry2.get())
        # print(self.messages)
        print(self.data)

    def get_entry3(self):
        self.messages[self.counter]['label3'] = self.Entry3.get()
        self.data[self.counter] = self.Entry3.get()
 

    def get_entry4(self):
        self.messages[self.counter]['label4'] = self.Entry4.get()
        self.data[self.counter] = self.Entry4.get()
               

    def nClick(self):
        self.counter += 1   
        
        if self.counter > 100000:
            stop = Label(text="exceeded 5 digits").pack()
            time.sleep(1)
            sys.exit()    
        # start_connections('',8000,1,self.sel,self.messages)
        self.events = self.sel.select(timeout=None)
        for key,mask in self.events:
            service_connection(key,mask,self.sel,self.messages,self.counter)   
        self.submit.config(text = f'Submit {self.counter}')

    def return_messages(self):
        return self.messages

    def send_data(self):
        self.counter += 1
        self.data['number'].append(self.counter)
        print(self.data)
        
        if self.counter > 100000:
            stop = Label(text="exceeded 5 digits").pack()
            time.sleep(1)
            sys.exit() 
        
        url = f'http://localhost:8000/data/'
        r = requests.post(url,json=self.data)
        print(r.text)
        print(r.status_code)
        if r.status_code == 404:
            showinfo('Repeating','data already processed') 
            # self.counter += 1

        self.submit.config(text = f'Submit {self.counter}')

if __name__ == "__main__":
    # messages = [bytes(f'{i}',encoding='utf8') for i in range(1000,100000)]  
    guiFrame = GUI()   
    guiFrame.mainloop()
    
   








    



    
