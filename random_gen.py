import sys
import random
import time
import json
import requests
import csv
from tkinter import *
from tkinter.messagebox import showinfo

class deleter:
    def __init__(self,root):
        self.root = root
        self.root.geometry("300x200")

        self.data = {'number':[],'label1':[],'label2':[]}
        self.delete_label = Label(root,text='Number to Delete')
        self.delete_label.pack()
        
        self.delete_prompt = Entry(root)
        self.delete_prompt.pack()

        self.delete_button = Button(root,text='delete record',command=self.delete)
        self.delete_button.pack()

    def delete(self):
        self.data['number'].append(self.delete_prompt.get())
        # url = 'http://104.197.53.135/delete/'
        url = 'http://127.0.0.1:8000/data/'
        r = requests.post(url,json=self.data)
        print(r.content)
        print(r.status_code)
        if r.status_code == 404:
            showinfo('Repeating','data already processed') 

        time.sleep(1)
        self.root.destroy()
        

class editor:
    def __init__(self,root):
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

        self.update = Button(root,text = 'Update Record', command = self.update_data )
        self.update.pack()

        self.close_window = Button(root,text = 'Close', command = self.close_window )
        self.close_window.pack()

    def update_data(self):
        self.data['number'].append(self.Entry1.get())
        self.data['label1'].append(self.Entry2.get())
        self.data['label2'].append(self.Entry3.get())
        print(self.data)

        # url = 'http://104.197.53.135/update/'
        url = 'http://127.0.0.1:8000/data/'
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



class GUI:
    def __init__(self,root):
        self.root = root
        self.root.geometry("300x300+200+200")

        self.counter = 1000
        self.data = {'number':[],'label1':[],'label2':[]}
        # self.messages = [bytes(f'{i}',encoding='utf8') for i in range(1000,100000)] 
        # self.messages = {i:dict() for i in range(1000,100000)}

        # self.sel = selectors.DefaultSelector()
        # start_connections('',8000,1,self.sel,self.messages)        

        self.label1 = Label(self.root,text='label1')
        self.label1.pack()

        self.Entry1 = Entry(self.root)
        self.Entry1.pack()

        self.label2 = Label(self.root,text='label2')
        self.label2.pack()

        self.Entry2 = Entry(self.root)
        self.Entry2.pack()

        self.submit = Button(self.root,text = f'Submit {self.counter}', command = self.send_data )
        self.submit.pack()

        self.download_csv = Button(self.root,text = 'Download', command = self.download)
        self.download_csv.pack()

        self.edit = Button(self.root,text = 'edit', command = lambda: self.edit_records(editor) )
        self.edit.pack()

        self.delete = Button(self.root,text='delete',command=lambda:self.delete_records(deleter))
        self.delete.pack()

    def delete_records(self,_class):
        self.delete = Toplevel(self.root)
        _class(self.delete)

    def edit_records(self,_class):
        self.edit = Toplevel(self.root)
        _class(self.edit)
               

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
        self.data['number'].append(self.counter)
        self.data['label1'].append(self.Entry1.get())
        self.data['label2'].append(self.Entry2.get())
        print(self.data)
  
        if self.counter > 100000:
            stop = Label(text="exceeded 5 digits").grid()
            time.sleep(1)
            sys.exit() 
            
        # url = 'http://104.197.53.135/data/'
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
        # url = 'http://104.197.53.135/feed_data/'
        url = 'http://127.0.0.1:8000/feed_data'
        r = requests.post(url)
        data = dict(r.json())['data so far']
        
        array = [i for i in data.values()]
        print(array)
        with open('mycsv.csv','w') as f:
            
            w = csv.writer(f)
            w.writerows(array)
           

 
# if __name__ == "__main__":
root = Tk()
root.geometry("200x200")
root.title("My Button Increaser")
app = GUI(root)
app.root.title('csv automation')
root.mainloop()
    

        
   








    



    
