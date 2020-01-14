from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk
import time
import os  
import mysql.connector as conn
import tkinter.messagebox as messagebox
from decimal import Decimal

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.master.destroy
        master.wm_title("CENECO PAYMENT MACHINE")
        master.geometry("1024x768")
        load = Image.open("Electric-Post.png")
        load = load.resize((1024, 768), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)
        
        
    def initfirst(self):
        can = Canvas(self, height=100, width=20)
        can.place(relx=0.5, rely=0.5, anchor=CENTER)
        entry = Entry(can, font=("Calibri 50"), justify="center")
        entry.pack(ipady=3)
        entry.focus()
        button1 = Button(self,  text="Confirm", bg="Green", fg="Black",width=15, command=lambda:Window.getbillid(self,entry.get()),font = ("TimesNewRoman 24"), justify="center")
        button1.place(x=375, y=450)
        text = Label(self, text="Enter Billing Number",fg='light gray', bg='dark green', font="Times 35 bold")
        text.place(x=290,y=245)
        self.master.bind('<Return>',lambda x:Window.getbillid(self, entry.get()))
        
    def getbillid(self, inputt):
        connectss = conn.connect(host='localhost', user='root', password='root1234', db='ceneco_old')
        
        b = connectss.cursor()
        b.execute("select bill_id from bills where bill_id='" + inputt + "'")
        resultb = b.fetchall()

        n = connectss.cursor()
        n.execute("select account_name from accounts, bills where bill_id='" + inputt + "' and meter_number = bills_meter_number")
        resultn = n.fetchall()

        ba = connectss.cursor()
        ba.execute("select bill_amount from bills where bill_id='" + inputt + "'")
        resultba = ba.fetchall()

        cred = connectss.cursor()
        cred.execute("select credit_balance from accounts, bills where bill_id='" + inputt + "' and meter_number = bills_meter_number")
        resultcred = cred.fetchall()

        #print(resultba)
        #length = len(line1var.get())
        #for (len= 0; len < length; len++){
        #    if(result[len] == "("){
        #        len++;
        #        lenresult[i] = result[len];
        #        if(result[len] == ",")
                    
        # }   
        #}
        #convertba = [int(round(float(i))) for i in resultba]
       # convertcred = [int(round(float(i))) for i in resultcred]

        #if (inputt = resultb)
        Window.nextwindow(self, resultb, resultn, resultba, resultcred)
        connectss.close()
        #else ()
        #    tkinter.messagebox.showinfo('ERROR', 'NO USER FOUND with this BILLING NUMBER')

    def nextwindow(self, resultb, resultn, resultba, resultcred):
        window = Toplevel(self)
        Window(window)
        self.master.withdraw()
        window.focus_force()
        button1 = Button(window, text="Return", bg="Red", fg="Black", command=lambda :Window.back(self,window), font = ("TimesNewRoman 24 bold"), justify="center")
        button1.place(x=275, y=620)
        button2 = Button(window, text="Continue", bg="Green", fg="Black", command=lambda: Window.final(self,window, resultb, resultn, resultba, resultcred), font = ("TimesNewRoman 24 bold"), justify="center")
        button2.place(x=575, y=620)
        window.bind('<Return>',lambda y:Window.final(self,window))
        window.bind('<g>', lambda y:Window.back(self,window))
        canvas = Canvas(window, width=700, height= 350, bg="white")
        canvas.place(x=175,y=250)
        canvas.create_text(350,30,fill="black",font="Times 40 bold",text="Account Information")
        canvas.create_text(115,120,fill="black",font="Times 20",text="Account Holder:  ")
        canvas.create_text(315,120,fill="black",font="Times 20",text= resultn)
        canvas.create_text(115,155,fill="black",font="Times 20",text="Billing Number: ")
        canvas.create_text(315,155,fill="black",font="Times 20",text= resultb)
        canvas.create_text(110,190,fill="black",font="Times 20",text="Credit Balance: ")
        canvas.create_text(315,190,fill="black",font="Times 20",text= resultcred)
        canvas.create_text(150,320,fill="black",font="Times 20",text="Current Bill Amount: ")
        canvas.create_text(325,320,fill="black",font="Times 20",text= resultba)
        canvas.update

    def back(self,window):
        self.master.deiconify()
        window.destroy()
        Window.initfirst(self)

    def final(self,prevwindow, resultb, resultn, resultba, resultcred):
        window = Toplevel(self)
        Window(window)
        window.focus_force()
        prevwindow.destroy()
        window.bind('<g>',lambda y:Window.back(self,window))
        button2 = Button(window, text="Continue", bg="Green", fg="Black", command=lambda: Window.confirm(self,window,resultb, resultn, resultba, resultcred), font = ("TimesNewRoman 24 bold"), justify="center")
        button2.place(x=500, y=650)
        window.bind('<Return>',lambda y:Window.confirm(self,window))
        button = Button(window, text="CANCEL", bg="Red", fg="Black", command=lambda: Window.back(self,window), font = ("TimesNewRoman 24"), justify="center")
        button.place(x=800, y=650)
        canvas = Canvas(window, width=400, height= 50, bg="white")
        canvas.place(x=70,y=300)
        canvas.create_text(85,30,fill="black",font="Times 15",text="Billing Number: ")
        canvas.create_text(245,30,fill="black",font="Times 20",text= resultb)
        canvas1 = Canvas(window, width=400, height= 50, bg="white")
        canvas1.place(x=70,y=375)
        canvas1.create_text(70,30,fill="black",font="Times 15",text="Bill Amount: ")
        canvas1.create_text(245,30,fill="black",font="Times 20",text= resultba)
        canvas2 = Canvas(window, width=400, height= 50, bg="white")
        canvas2.place(x=70,y=450)
        canvas2.create_text(80,30,fill="black",font="Times 15",text="Credit Balance: ")
        canvas2.create_text(245,30,fill="black",font="Times 20",text= resultcred)
        canvas3 = Canvas(window, width=400, height= 50, bg="white")
        canvas3.place(x=70,y=525)
        canvas3.create_text(90,30,fill="black",font="Times 15",text="Amount to be Paid: ")
        canvas3.create_text(245,30,fill="black",font="Times 20",text= resultba)
        canvas.update
        canvas1.update
        canvas2.update
        canvas3.update
        load = Image.open("accept.png")
        load = load.resize((450, 250), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(window, image=render)
        img.image = render
        img.place(x=525, y=315)
        textt = Label(window, text="Amount Inserted: ", bg='light gray', font="Times 25 bold")
        textt.place(x=70,y=600)
        texttt = Label(window, text="12,200.00", bg='light gray', font="Times 25 bold")
        texttt.place(x=335,y=600)

    def confirm(self, pasok, resultb, resultn, resultba, resultcred):
        window = Toplevel(self)
        Window(window)
        pasok.destroy()
        window.focus_force()
        button1 = Button(window, text="Return", bg="Red", fg="Black", command=lambda :Window.back(self,window), font = ("TimesNewRoman 24 bold"), justify="center")
        button1.place(x=275, y=475)
        button2 = Button(window, text="Continue", bg="Green", fg="Black", command=lambda: Window.print(self,window, resultba), font = ("TimesNewRoman 24 bold"), justify="center")
        button2.place(x=570, y=475)
        window.bind('<Return>',lambda y:Window.print(self,window))
        window.bind('<g>', lambda y:Window.back(self,window))
        canvas = Canvas(window, width=700, height= 150, bg="white")
        canvas.place(x=150,y=300)
        textt = Label(window, text="Please review your transaction before clicking the confirm button.", bg='light gray', font="Times 25 bold")
        textt.place(x=50,y=245)
        canvas.create_text(110,30,fill="black",font="Times 20",text="Account Holder: ")
        canvas.create_text(110,75,fill="black",font="Times 20",text="Billing Number: ")
        canvas.create_text(115,120,fill="black",font="Times 20",text="Amount Inserted: ")
        canvas.create_text(310,30,fill="black",font="Times 20",text= resultn)
        canvas.create_text(315,75,fill="black",font="Times 20",text= resultb)
        canvas.create_text(315,120,fill="black",font="Times 20",text="12,200.00")
        canvas.update

    def print(self, pasok, resultba):
        window = Toplevel(self)
        Window(window)
        pasok.destroy()
        window.focus_force()
        button1 = Button(window, text="EXIT", bg="Red", fg="Black", command=lambda :Window.back(self,window), font = ("TimesNewRoman 24 bold"), justify="center")
        button1.place(x=475, y=515)
        window.bind('<g>',lambda y:Window.back(self,window))
        canvas = Canvas(window, width=700, height= 150, bg="white")
        canvas.place(x=175,y=325)
        textt = Label(window, text="TRANSACTION SUCCESSFUL", bg='light gray', font="Times 35 bold")
        textt.place(x=190,y=230)
        canvas.create_text(280,30, fill="green",font="Times 25 bold",text="Your credit of Php")
        canvas.create_text(475,30, fill="green",font="Times 25 bold",text= resultba)
        canvas.create_text(320,90,fill="green",font="Times 25 bold",text="will be deducted to your\nnext transaction ")
        load = Image.open("images.png")
        load = load.resize((150, 150), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(window, image=render)
        img.image = render
        img.place(x=150, y=325)
        canvas.update

    

    