import sys
import socket
import selectors
import types
import random
import time
import json
import requests
import mimetypes
import os
import pandas as pd
from tkinter import *
from tkinter.messagebox import showinfo
from itertools import cycle

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
        #                        # self.Entry1 = Entry(master)
        # self.Entry1.grid()      msg_total=sum(len(m) for m in messages),
        #                             recv_total=0,
        #                             messages=iter(messages),
        #                             outb=b'')
        data1 = json.dumps(messages).encode('utf-8')
        sel.register(sock, events, data=data1)

class editor:
    def __init__(self,root=Tk()):
        self.root = root
        self.root.geometry("300x300+200+200")

        self.data = {'number':[],'label1':[],'label2':[]}
        
        self.label_counter = Label(root,text='Count number')
        self.label_counter.pack()

        self.Entry1 = Entry(root)
        self.Entry1.pack()

        self.label2 = Label(root,text='label1')
        self.label2.pack()

        self.Entry2 = Entry(root)
        self.Entry2.pack()

        self.label3 = Label(root,text='label2')
        self.label3.pack()

        self.Entry3 = Entry(root)
        self.Entry3.pack()

        # self.label4 = Label(master,text='label3')
        # self.label4.grid()

        # self.Entry4 = Entry(master)
        # self.Entry4.grid()

        self.update = Button(root,text = 'Update Record', command = self.update_data )
        self.update.pack()

        self.close_window = Button(root,text = 'Close', command = self.close_window )
        self.close_window.pack()

    def update_data(self):
        self.data['number'].append(self.Entry1.get())
        self.data['label1'].append(self.Entry2.get())
        self.data['label2'].append(self.Entry3.get())
        print(self.data)

        url = 'http://127.0.0.1:8000/update/'
        r = requests.post(url,json=self.data)
        print(r.content)
        print(r.status_code)
        if r.status_code == 404:
            showinfo('Repeating','data already processed') 
        
        self.data['number'].pop()
        self.data['label1'].pop()
        self.data['label2'].pop()

    def close_window(self):
        self.root.destroy()






class GUI(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        
        self.grid()
        self.counter = 1000
        self.data = {'number':[],'label1':[],'label2':[]}
        # self.messages = [bytes(f'{i}',encoding='utf8') for i in range(1000,100000)] 
        # self.messages = {i:dict() for i in range(1000,100000)}

        # self.sel = selectors.DefaultSelector()
        # start_connections('',8000,1,self.sel,self.messages)        

        self.label1 = Label(master,text='label1')
        self.label1.grid()

        self.Entry1 = Entry(master)
        self.Entry1.grid()

        self.label2 = Label(master,text='label2')
        self.label2.grid()

        self.Entry2 = Entry(master)
        self.Entry2.grid()

        self.submit = Button(text = f'Submit {self.counter}', command = self.send_data )
        self.submit.grid()

        self.download_csv = Button(text = 'Download', command = self.download)
        self.download_csv.grid()

        self.edit = Button(text = 'edit', command = lambda: self.edit_records(editor) )
        self.edit.grid()

    def edit_records(self,_class):
        self.edit = Toplevel()
        _class(self.edit)


    def get_entry1(self):
        self.messages[self.counter]['label1'] = self.Entry1.get()
        self.data['label1'].append(self.Entry1.get())
        
        print(self.data)

    def get_entry2(self):
        self.messages[self.counter]['label2'] = self.Entry2.get()
        self.data['label2'].append(self.Entry2.get())
        
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
            service_connection(key,mask,self.sel,self.messages,self.counter)   
        self.submit.config(text = f'Submit {self.counter}')

    def return_messages(self):
        return self.messages

    def send_data(self):
        self.counter += 1
        self.data['number'].append(self.counter)
        self.data['label1'].append(self.Entry1.get())
        self.data['label2'].append(self.Entry2.get())
        print(self.data)
  
        if self.counter > 100000:
            stop = Label(text="exceeded 5 digits").pack()
            time.sleep(1)
            sys.exit() 
            
        # url = 'http://34.84.220.35/data/'
        url = 'http://127.0.0.1:8000/data/'
        r = requests.post(url,json=self.data)
        print(r.content)
        print(r.status_code)
        if r.status_code == 404:
            showinfo('Repeating','data already processed') 

        self.counter += 1
        self.submit.config(text = f'Submit {self.counter}')
        self.data['number'].pop(0)
        self.data['label1'].pop(0)
        self.data['label2'].pop(0)
    
    def download(self):
        # url = 'http://34.84.220.35/feed_data/'
        url = 'http://127.0.0.1:8000/feed_data'
        r = requests.post(url)
        data = dict(r.json())
        print(data['data so far'])
        df = pd.DataFrame(data['data so far'])
      
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
        df.to_csv(desktop + '/your_data.csv')
 

guiFrame = GUI()   
guiFrame.mainloop()
        
   








    



    
