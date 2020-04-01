import time
import socket
import types
import sys
import selectors
from tkinter import *

used = list()

def GUI():
    root = Tk()
    root.geometry("200x200")
    root.title("counts")
    sign = Label(root,text=used[-1]).pack()
    root.mainloop()

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        try:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
            else:
                print('closing connection to', data.addr)
                sel.unregister(sock)
                sock.close()
        except ConnectionResetError:
            print(used)
            GUI()
            pass
        
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            if data.outb in used:
                print('number used')
                sent = sock.send(bytes(f'{data.outb} number used',encoding='utf8'))
            
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            used.append(data.outb)
            data.outb = data.outb[sent:]
            
        




sel = selectors.DefaultSelector()
lsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind(('',8000))
lsock.listen()
print('listening on',('',8000))

lsock.setblocking(False)
sel.register(lsock,selectors.EVENT_READ,data=None)



while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)
