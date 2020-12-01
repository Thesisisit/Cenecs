import serial
from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk
import os  
import mysql.connector as conn
import tkinter.messagebox as messagebox
from decimal import Decimal
import threading
import time
from datetime import datetime,date
today = date.today()
now= datetime.now()
import sys
import os

from random import randint
randomm = str(int(randint(0, 2000)))

print(randomm)
#test account = 202002
total = 0  


class Window(Frame):
    

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.master.destroy
        master.wm_title("CENECO PAYMENT MACHINE")
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        master.geometry(f"{self.width}x{self.height}")
        load = Image.open("//home//pi//Documents//git//Cenecs//Electric-Post.png")
        load = load.resize((self.width, self.height), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)
        
        
        
    def initfirst(self):
        control="F"
        billcontrol = serial.Serial('/dev/ttyACM0', 115200)
        billcontrol.write(control.encode())
        can = Canvas(self, height=100, width=20)
        can.place(relx=0.5, rely=0.5, anchor=CENTER)
        entry = Entry(can, font=("Calibri 50"), justify="center")
        entry.pack(ipady=3)
        entry.focus()
        button1 = Button(self,  text="Confirm", bg="Green", fg="Black",width=15, command=lambda:Window.getbillid(self,entry.get()),font = ("TimesNewRoman 24"), justify="center")
        button1.place(x=375, y=450)
        text = Label(self, text="Enter Billing Number",fg='light gray', bg='dark green', font="Times 35 bold")
        text.place(x=290,y=245)
        self.master.bind('<KP_Enter>',lambda x:Window.getbillid(self, entry.get()))
        
        
    def getbillid(self, inputt):
        connectss = conn.connect(host='192.168.1.15', user='remote', password='remote', db='ceneco_old', auth_plugin='mysql_native_password')
     #connectss = conn.connect(host='localhost', user='root', password='NewRootPassword', db='ceneco_older')
        
        b = connectss.cursor()
        b.execute("select bill_id from bills where bill_id='" + inputt + "'")
        resultb = b.fetchall()

        n = connectss.cursor()
        n.execute("select account_name from accounts, bills where bill_id='" + inputt + "' and account_number = bills_account_number")
        resultn = n.fetchall()

        ba = connectss.cursor()
        ba.execute("select bill_balance from bills where bill_id='" + inputt + "'")
        resultba = ba.fetchall()


        cred = connectss.cursor()
        cred.execute("select credit_balance from accounts, bills where bill_id='" + inputt + "' and account_number = bills_account_number")
        resultcred = cred.fetchall()

        stat = connectss.cursor()
        stat.execute("select a.status from accounts as a, bills as b where bill_id='" + inputt + "' and a.account_number = b.bills_account_number")
        resultstat = stat.fetchall()

        date = connectss.cursor()
        date.execute("select due_date from bills as b where bill_id='" + inputt + "'")
        dateee = date.fetchall()

        nam = list(resultn)
        name = str(nam)[3:-4]
        if name == "":
            messagebox.showinfo("Error", "Bill not found")
            Window.initfirst(self)
        else:
            Window.nextwindow(self, resultb, resultn, resultba, resultcred, inputt, resultstat, dateee)
            connectss.close()    
            
        

    
    def nextwindow(self, resultb, resultn, resultba, resultcred, inputt, resultstat,dateee):
        window = Toplevel(self)
        
        Window(window)
        self.master.withdraw()
        window.focus_force()
        stringstatus = list(resultstat)
        stats = str(stringstatus)[2:-3]
        button1 = Button(window, text="Back", bg="Red", fg="Black", command=lambda :Window.back(self,window), font = ("TimesNewRoman 24 bold"), justify="center")
        button1.place(x=275, y=620)
        button2 = Button(window, text="Continue", bg="Green", fg="Black", command=lambda: Window.final(self,window, resultb, resultn, resultba, resultcred, inputt,total,  resultstat,dateee), font = ("TimesNewRoman 24 bold"), justify="center")
        button2.place(x=575, y=620)
        window.bind('<KP_Enter>',lambda y:Window.final(self,window, resultb, resultn, resultba, resultcred, inputt,total, resultstat,dateee))
        window.bind('<KP_Decimal>', lambda y:Window.back(self,window))
        canvas = Canvas(window, width=700, height= 350, bg="white")
        canvas.place(x=175,y=250)
        nam = list(resultn)
        name = str(nam)[3:-4]
        canvas.create_text(350,30,fill="black",font="Times 40 bold",text="Account Information")
        canvas.create_text(115,120,fill="black",font="Times 20",text="Account Holder:  ")
        canvas.create_text(315,120,fill="black",font="Times 20",text= name)
        canvas.create_text(115,155,fill="black",font="Times 20",text="Billing Number: ")
        canvas.create_text(315,155,fill="black",font="Times 20",text= resultb)
        canvas.create_text(110,190,fill="black",font="Times 20",text="Credit Balance: ")
        canvas.create_text(315,190,fill="black",font="Times 20",text= resultcred)
        canvas.create_text(150,225,fill="black",font="Times 20",text="Bill Amount: ")
        canvas.create_text(325,225,fill="black",font="Times 20",text= resultba)
        #2019101396013
        if stats == "0":
            balance1 = list(resultba)
            balances1 = str(balance1)[2:-3]
            floatbalance1 = float(str(balances1)) + 22.41
            balance10 = list(resultcred)
            balances10 = str(balance10)[2:-3]
            floatbalance10 = float(str(balances10))
            balmincredi = floatbalance1 - floatbalance10
            conv = str(float(round(balmincredi, 2)))

            canvas.create_text(150,260,fill="black",font="Times 20",text="Reconnection fee: ")
            canvas.create_text(325,260,fill="black",font="Times 20",text= "22.41")
            canvas.create_text(150,320,fill="black",font="Times 20",text="Current Bill Balance: ")
            canvas.create_text(325,320,fill="black",font="Times 20",text= conv)
        else:
            balance1 = list(resultba)
            balances1 = str(balance1)[2:-3]
            floatbalance1 = float(str(balances1))
            balance10 = list(resultcred)
            balances10 = str(balance10)[2:-3]
            floatbalance10 = float(str(balances10))
            balmincred = floatbalance10 - floatbalance1

            conv = str(float(abs(round(balmincred, 2))))
            canvas.create_text(150,260,fill="black",font="Times 20",text="Reconnection fee: ")
            canvas.create_text(325,260,fill="black",font="Times 20",text= "00.00")
            canvas.create_text(150,320,fill="black",font="Times 20",text="Current Bill Balance: ")
            canvas.create_text(325,320,fill="black",font="Times 20",text= conv)
        canvas.update

    def back(self,window):
        self.master.deiconify()
        window.destroy()
        receiptPrinter = serial.Serial('/dev/ttyUSB0', 19200)
        dataToReceipt  = "e$"
        control="F"
        billcontrol = serial.Serial('/dev/ttyACM0', 115200)
        billcontrol.write(control.encode())
        receiptPrinter.write(dataToReceipt.encode())
        python = sys.executable
        os.execl(python,python, * sys.argv)
    def fromconfirmtopayment(self,prevwindow, resultb, resultn, resultba, resultcred, inputt,total, resultstat, dateee):
        # self.master.deiconify()
        Window.destroy(self)
        Window.final(self,prevwindow, resultb, resultn, resultba, resultcred, inputt,total, resultstat, dateee)

    def final(self,prevwindow, resultb, resultn, resultba, resultcred, inputt, total, resultstat, dateee):
        control="N"
        billcontrol = serial.Serial('/dev/ttyACM0', 115200)
        billcontrol.write(control.encode())
        window = Toplevel(self.master)
        Window(window)
        print("f")
        print(window)
        window.focus_force()
        prevwindow.destroy()
        window.bind('<KP_Decimal>',lambda y:Window.back(self,window))
        lisba = list(resultba)
        resba = str(lisba)[2:-3]
        flotba = float(str(resba))
        lis = list(resultcred)
        res = str(lis)[2:-3]
        flot = float(str(res))
        stringstatus = list(resultstat)
        stats = str(stringstatus)[2:-3]
        button = Button(window, text="Back", bg="Red", fg="Black", command=lambda: Window.back(self,window), font = ("TimesNewRoman 24"), justify="center")
        button.place(x=800, y=650)
        sub= flotba-flot
        stat = Label(window, text= "Account Status: ", bg='white', font="Times 15 bold")
        stat.place(x=75,y=260)
        if stats == "0":
            textstatus = Label(window, text= "Disconnected",fg="red", bg='white', font="Times 15 bold")
            textstatus.place(x=220,y=260)
        else:
            textstatus = Label(window, text= "Active",fg="Green", bg='white', font="Times 15 bold")
            textstatus.place(x=220,y=260)
            
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
        if stats == "0":
            balance3 = list(resultba)
            balances3 = str(balance3)[2:-3]
            floatbalance3 = float(str(balances3)) + 22.41
            balance10 = list(resultcred)
            balances10 = str(balance10)[2:-3]
            floatbalance10 = float(str(balances10))
            balmincredit = floatbalance3 - floatbalance10
            conv5 = str(float(round(balmincredit, 2)))
            canvas3.create_text(90,30,fill="black",font="Times 15",text="Amount to be Paid: ")
            canvas3.create_text(245,30,fill="black",font="Times 20",text= conv5)
        else:
            canvas3.create_text(90,30,fill="black",font="Times 15",text="Amount to be Paid: ")
            canvas3.create_text(245,30,fill="black",font="Times 20",text= sub)
        canvas.update
        canvas1.update
        canvas2.update
        canvas3.update
        print(resultstat)
        stringstatus = list(resultstat)
        stats = str(stringstatus)[2:-3]

        #det = list(dateee)
        #datee = str(det)[16:-4]
        #detee = str(today)
        #print(today)
        #print(datee)
        #date_object = datetime.strptime(datee, '%m-%d-%Y').date()
        #print(type(date_object))
        #print(date_object)
        
        
        canvas10 = Canvas(window, width=450, height= 250, bg="white")
        canvas10.place(x=525, y=315)
        canvas10.create_text(110,10,fill="black",font="Times 15",text="number of bills inserted")
        canvas10.create_text(380,10,fill="black",font="Times 15",text="Bill amount")
        canvas10.create_text(100,20,fill="black",font="Times 15",text="------------------------------------------------------------------------------------------------------")
        canvas10.create_text(380,40,fill="black",font="Times 15",text="20")
        canvas10.create_text(380,70,fill="black",font="Times 15",text="50")
        canvas10.create_text(380,100,fill="black",font="Times 15",text="100")
        canvas10.create_text(380,130,fill="black",font="Times 15",text="200")
        canvas10.create_text(380,160,fill="black",font="Times 15",text="500")
        canvas10.create_text(380,190,fill="black",font="Times 15",text="1000")
        canvas10.create_text(100,40,fill="black",font="Times 15",text="0x")
        canvas10.create_text(100,70,fill="black",font="Times 15",text="0x")
        canvas10.create_text(100,100,fill="black",font="Times 15",text="0x")
        canvas10.create_text(100,130,fill="black",font="Times 15",text="0x")
        canvas10.create_text(100,160,fill="black",font="Times 15",text="0x")
        canvas10.create_text(100,190,fill="black",font="Times 15",text="0x")
        canvas10.create_text(100,210,fill="black",font="Times 15",text="------------------------------------------------------------------------------------------------------")
        canvas10.create_text(100,230,fill="black",font="Times 15",text="TOTAL")
          
        texttt = Label(window, text= " PLEASE INSERT BILL", bg='white', font="Times 25 bold")
        texttt.place(x=575,y=275)
        #test account = 2019101396013
        textt = Label(window, text="Amount Inserted: ", bg='light gray', font="Times 25 bold")
        textt.place(x=70,y=600)
        #texttt = Label(window, text= total, bg='white', font="Times 15")
        #texttt.place(x=890,y=530)
        #inserted = IntVar()
        window.update()
        global stop_thread
        stop_thread = False
        mt = threading.Thread(target=self.read, args = (window, resultb, resultn, resultba, resultcred, inputt, total, resultstat, dateee))
        mt.start()

    def read(self, window, resultb, resultn, resultba, resultcred, inputt, total, resultstat, dateee):
        output=0
        twenty=0
        fifty=0
        print("l")
        print(window)
        hundred=0
        twohundred=0
        fivehundred=0
        thousand=0
        finalWindow = window
        while True:
            global stop_thread
            if stop_thread :
                print("Stop Thread")
                break
            else :
                print("Thread still running")
            
            arduinoData = serial.Serial('/dev/ttyACM0', 115200, timeout=2)
            print("after init")
            myData = (arduinoData.readline().strip())
            if myData :
                print("after read")
                sulod = int(myData.decode('utf-8'))
                output = total + sulod
                print(output)
                
                texttt = Label(finalWindow, text= total, bg='white', font="Times 15")
                texttt.place(x=890,y=530)
                if sulod == 20:
                    twenty += 1
                    stri = str(int(twenty))
                    twen = Label(finalWindow, text= stri + 'x', bg='white', font="Times 15")
                    twen.place(x=613,y=342)
                if sulod == 50:
                    fifty += 1
                    stri5 = str(int(fifty))
                    twen = Label(finalWindow, text= stri5 + 'x', bg='white', font="Times 15")
                    twen.place(x=613,y=372)
                if sulod == 100:
                    hundred += 1
                    stri1 = str(int(hundred))
                    twen = Label(finalWindow, text= stri1 + 'x', bg='white', font="Times 15")
                    twen.place(x=613,y=402)
                if sulod == 200:
                    twohundred += 1
                    stri2 = str(int(twohundred))
                    twen = Label(finalWindow, text= stri2 + 'x', bg='white', font="Times 15")
                    twen.place(x=613,y=432)
                if sulod == 500:
                    fivehundred += 1
                    stri2 = str(int(fivehundred))
                    twen = Label(finalWindow, text= stri2 + 'x', bg='white', font="Times 15")
                    twen.place(x=613,y=462)
                if sulod == 1000:
                    thousand += 1
                    stri11 = str(int(thousand))
                    twen = Label(finalWindow, text= stri11 + 'x', bg='white', font="Times 15")
                    twen.place(x=613,y=492)
                    
                texttt = Label(finalWindow, text= output, bg='light gray', font="Times 25 bold")
                texttt.place(x=335,y=600)
                total = output
                button2 = Button(finalWindow, text="Continue", bg="Green", fg="Black", command=lambda: Window.confirm(self,finalWindow, resultb, resultn, resultba, resultcred, inputt, total, resultstat, dateee), font = ("TimesNewRoman 24 bold"), justify="center")
                button2.place(x=500, y=650)
                finalWindow.bind('<KP_Enter>',lambda y:Window.confirm(self,finalWindow, resultb, resultn, resultba, resultcred, inputt, total, resultstat, dateee))
            
                

            
            
    #def terminate (self, window,resultb, resultn, resultba, resultcred, inputt, total):
    #    mt = threading.Thread(target=self.read, args = (window, resultb, resultn, resultba, resultcred, inputt, total))
     #   mt._stop()
    #    self.master.deiconify()
    #    window.destroy()
     #   Window.confirm(self,window,resultb, resultn, resultba, resultcred, inputt, total)
    def confirm(self, pasok, resultb, resultn, resultba, resultcred, inputt, total, resultstat, dateee):
        control="F"
        billcontrol = serial.Serial('/dev/ttyACM0', 115200)
        billcontrol.write(control.encode())
        window = Toplevel(self.master)
        Window(window)
        global stop_thread
        stop_thread = True
        pasok.destroy()
        window.focus_force()
        button1 = Button(window, text="Back", bg="Red", fg="Black", command=lambda :Window.fromconfirmtopayment(self,window, resultb, resultn, resultba, resultcred, inputt, total, resultstat, dateee), font = ("TimesNewRoman 24 bold"), justify="center")
        button1.place(x=275, y=475)
        button2 = Button(window, text="Continue", bg="Green", fg="Black", font = ("TimesNewRoman 24 bold"), justify="center", command=lambda :Window.printss(self, window, resultb, resultn, resultba, resultcred, inputt, total, resultstat, dateee))
        button2.place(x=570, y=475)
        window.bind('<KP_Enter>',lambda y:Window.printss(self, window, resultb, resultn, resultba, resultcred, inputt, total, resultstat, dateee))
        window.bind('<KP_Decimal>', lambda y:Window.fromconfirmtopayment(self,window, resultb, resultn, resultba, resultcred, inputt, total, resultstat, dateee))
        canvas = Canvas(window, width=700, height= 150, bg="white")
        canvas.place(x=150,y=300)
        textt = Label(window, text="Please review your transaction before clicking the confirm button.", bg='light gray', font="Times 25 bold")
        textt.place(x=50,y=245)
        nam = list(resultn)
        name = str(nam)[3:-4]
        print(total)
        canvas.create_text(110,30,fill="black",font="Times 20",text="Account Holder: ")
        canvas.create_text(110,75,fill="black",font="Times 20",text="Billing Number: ")
        canvas.create_text(115,120,fill="black",font="Times 20",text="Amount Inserted: ")
        canvas.create_text(310,30,fill="black",font="Times 20",text= name)
        canvas.create_text(315,75,fill="black",font="Times 20",text= resultb)
        canvas.create_text(315,120,fill="black",font="Times 20",text= total )
        canvas.update

    def printss(self, pasok, resultb, resultn, resultba, resultcred, inputt, total, resultstat, dateee):
        window = Toplevel(self.master)
        Window(window)
        pasok.destroy()
        window.focus_force()
        button1 = Button(window, text="EXIT", bg="Red", fg="Black", command=lambda :Window.back(self,window), font = ("TimesNewRoman 24 bold"), justify="center")
        button1.place(x=475, y=515)     
        window.bind('<KP_Decimal>',lambda y:Window.back(self,window))
        canvas = Canvas(window, width=700, height= 150, bg="white")
        canvas.place(x=175,y=325)
        textt = Label(window, text="TRANSACTION SUCCESSFUL", bg='light gray', font="Times 35 bold")
        textt.place(x=190,y=230)
        
        
        datetimee = now.strftime("%Y/%m/%d %H:%M:%S")
        heh = list(resultstat)
        ehee = str(heh)[2:-3]
        if ehee =="0":  
            bal = list(resultba)
            bala = str(bal)[2:-3]
            balan = float(str(bala))
            answer = str(round(balan, 2)) #bill balance
            final = float(str(answer))
            difference = str(round(total - (final + 22.41),2))
            finallly = float(str(difference))
        else:  
            bal = list(resultba)
            bala = str(bal)[2:-3]
            balan = float(str(bala))
            answer = str(round(balan, 2)) #bill balance
            final = float(str(answer))
            difference = str(round(total - final ,2))
            finallly = float(str(difference))
        print(difference)
        if finallly > 0:
            cr = list(resultcred)
            cred = str(cr)[2:-3]
            credit = float(str(cred))
            lisba = list(resultba)
            resba = str(lisba)[2:-3]
            finals = total - float(str(resba)) - credit - 22.41
            conv = str(float(abs(finals)))
            canvas.create_text(280,30, fill="green",font="Times 25 bold",text="Your credit of Php")
            canvas.create_text(475,30, fill="green",font="Times 25 bold",text= conv)
            canvas.create_text(320,90,fill="green",font="Times 25 bold",text="will be deducted to your\nnext bill ")
        else:
            cr = list(resultcred)
            cred = str(cr)[2:-3]
            credit = float(str(cred))

            lisba = list(resultba)
            resba = str(lisba)[2:-3]
            
            finals = float(str(resba)) - total  -credit
            conv1 = str(float(abs(round(finals, 2))))
            canvas.create_text(320,30, fill="green",font="Times 25 bold",text="Your new balance is: ")
            canvas.create_text(400,90, fill="green",font="Times 25 bold",text= "Php "+ conv1)
        
#2020111396012
        load = Image.open("//home//pi//Documents//git//Cenecs//images.png")
        load = load.resize((150, 150), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(window, image=render)
        img.image = render
        img.place(x=150, y=325)
        connectss = conn.connect(host='192.168.1.15', user='remote', password='remote', db='ceneco_old', auth_plugin='mysql_native_password')
        #connectss = conn.connect(host='localhost', user='root', password='NewRootPassword', db='ceneco_older')
        namee = list(resultn)
        nameeee = str(namee)[3:-4]
        print(nameeee)
        if finallly > 0:
            
            print(conv)
            billbalancechange = connectss.cursor()
            billbalancechange.execute("UPDATE bills SET bill_balance = 0 WHERE bill_id ='" + inputt + "'")
            connectss.commit()
            creditupdate = connectss.cursor()
            
            trans = connectss.cursor()
            
            datetimeee = now.strftime("%Y/%m/%d %H:%M:%S")
            totals= str(total)
            print(datetimee)
            print(inputt)
            print(total)
            print(conv)
            #UPDATE accounts SET credit_balance = '500' Where bills.bills_accout_number = accounts.account_number and bill_id =2020011396011
            trans.execute("INSERT INTO transactions( transaction_id, date_time, transactions_bill_id, amount_paid, credit_balance) VALUES (NULL, '"+datetimeee+"', "+inputt+", "+ totals +", "+conv+")")
            connectss.commit()
            print(resultstat)
            he = list(resultstat)
            hehe = str(he)[2:-3]
            if hehe == "0":
                totals= float(str(total))
                cr = list(resultcred)
                cred = str(cr)[2:-3]
                credit = float(str(cred)) #credit
                lisba = list(resultba)
                resba = str(lisba)[2:-3]
                finals = (totals + credit) -float(str(resba)) - 22.41
                conv = str(float(abs(finals)))
                creditupdate.execute("UPDATE accounts SET credit_balance = '" + conv + "' Where account_name = '"+nameeee+"'")
                connectss.commit()
                creditupdatedisco = connectss.cursor()
                creditupdatedisco.execute("UPDATE bills SET status = '1' Where bill_id ='"+inputt+"'")
                connectss.commit()
                print("success")
            else:
                totals= float(str(total))
                cr = list(resultcred)
                cred = str(cr)[2:-3]
                credit = float(str(cred)) #credit
                lisba = list(resultba)
                resba = str(lisba)[2:-3]
                finals = (totals + credit) -float(str(resba))
                conv = str(float(abs(finals)))
                creditupdate.execute("UPDATE accounts SET credit_balance = '" + conv + "' Where account_name = '"+nameeee+"'")
                connectss.commit()
                print("still connected")    
        else:
            totals= float(str(total))
            balance2 = list(resultba)
            balances2 = str(balance2)[2:-3]
            cr = list(resultcred)
            cred = str(cr)[2:-3]
            creditss = float(str(cred))
            floatbalance2 = float(str(balances2)) -totals -creditss
            billbalchange = str(float(floatbalance2))
            print("else less cred")
            print(billbalchange)
            billbalancechange = connectss.cursor()
            billbalancechange.execute("UPDATE bills SET bill_balance = '"+ billbalchange + "' WHERE bill_id ='" + inputt + "'")
            print("success update bill balance")
            connectss.commit()
            creditupdate = connectss.cursor()
            creditupdate.execute("UPDATE accounts SET credit_balance = 0 Where account_name ='"+nameeee+"'")
            print("success update accounts cred balance")
            connectss.commit()
            trans = connectss.cursor()
            trans.execute("UPDATE transactions SET credit_balance = 0.00 Where transactions_bill_id ='"+inputt+"'")
            print("success update transacton credit balance")
            connectss.commit()
            datetimeee = now.strftime("%Y/%m/%d %H:%M:%S")
            totals= str(total)
            print(datetimee)
            print(inputt)
            print(total)
            trans.execute("INSERT INTO transactions( transaction_id, date_time, transactions_bill_id, amount_paid, credit_balance) VALUES (NULL, '"+datetimeee+"', "+inputt+", "+ totals +", '0.00')")
            connectss.commit()
        #
        
        ad = connectss.cursor()
        ad.execute("select address from accounts, bills where bill_id='" + inputt + "' and account_number = bills_account_number")
        addresss = ad.fetchall()

        tra = connectss.cursor()
        tra.execute("select MAX(transaction_id) from transactions, bills where bill_id='" + inputt + "' and transactions_bill_id='"+inputt+"'")
        transNumbers = tra.fetchall()


        billmo = connectss.cursor()
        billmo.execute("select bill_month from bills where bill_id='" + inputt + "'")
        billMonths = billmo.fetchall()

        due = connectss.cursor()
        due.execute("select due_date from bills where bill_id='" + inputt + "'")
        dueDates = due.fetchall()

        ba = connectss.cursor()
        ba.execute("select bill_amount from bills where bill_id='" + inputt + "'")
        billAmounts = ba.fetchall()

        cre = connectss.cursor()
        cre.execute("select credit_balance from accounts,bills where bill_id='" + inputt + "' and account_number = bills_account_number")
        creditBalances = cre.fetchall()

        b = connectss.cursor()
        b.execute("select account_number from accounts,bills where bill_id='" + inputt + "' and account_number = bills_account_number")
        accountNumbers = b.fetchall()

        bs = connectss.cursor()
        bs.execute("select bill_period_start from bills where bill_id='" + inputt + "'")
        billstart = bs.fetchall()
         
        be = connectss.cursor()
        be.execute("select bill_period_end from bills where bill_id='" + inputt + "'")
        billend = be.fetchall()

        rea = connectss.cursor()
        rea.execute("select previous_reading from bills where bill_id='" + inputt + "'")
        prereading = rea.fetchall()

        cur = connectss.cursor()
        cur.execute("select current_reading from bills where bill_id='" + inputt + "'")
        curreading = cur.fetchall()

        ene = connectss.cursor()
        ene.execute("select energy from bills where bill_id='" + inputt + "'")
        enereading = ene.fetchall()

        bil = connectss.cursor()
        bil.execute("select bill_balance from bills where bill_id='" + inputt + "'")
        bilbal = bil.fetchall()
        

        receiptPrinter = serial.Serial('/dev/ttyUSB0', 19200)
        hee = list(resultstat)
        hehee = str(hee)[2:-3]
        if hehee == "0":
            ReconnectionFee = str(int(22.41))
        else :
            ReconnectionFee = str(float(00.00))
        #datee = datetime
        billNumber = inputt
        tot=str(total)
        amountPaid = tot
        print(amountPaid)
        #print(datee)

        date = datetimee
        acc = list(accountNumbers)
        accountNumber = str(acc)[2:-3]
        #nam = list(names)
        #name = str(nam)[3:-4]
        add = list(addresss)
        address = str(add)[3:-4]
        trans = list(transNumbers)
        transNumber = str(trans)[2:-3]
        bilmo = list(billMonths)
        billMonth = str(bilmo)[3:-4]
        dueda = list(dueDates)
        dueDate = str(dueda)[16:-4]
        bilam = list(billAmounts)
        billAmount = str(bilam)[2:-3]
        credba = list(creditBalances)
        creditBalance = str(credba)[2:-3]
        bilst = list(billstart)
        BillPeriodStart = str(bilst)[16:-4]
        bilen = list(billend)
        BillPeriodEnd = str(bilen)[16:-4]
        brea = list(prereading)
        PreviousReading = str(brea)[3:-4]
        crea = list(curreading)
        CurrentReading = str(crea)[3:-4]
        energ = list(enereading)
        EnergyConsumed = str(energ)[3:-4]
        baal = list(bilbal)
        billBalance = str(baal)[2:-3]

        print(nameeee)
        print(accountNumber)
        print(address)
        print(transNumber)
        print(billMonth)
        print(dueDate)
        print(billAmount)
        print(creditBalance)
        print(date)
        print(billNumber)
        print(amountPaid)

        dataToReceipt  = "p$"
        dataToReceipt += date + "$"
        dataToReceipt += accountNumber+ "$"
        dataToReceipt += nameeee + "$"
        dataToReceipt += address + "$"
        dataToReceipt += transNumber + "$"
        dataToReceipt += billNumber + "$"
        dataToReceipt += billMonth + "$"
        dataToReceipt += BillPeriodStart + "$"
        dataToReceipt += BillPeriodEnd + "$"
        dataToReceipt += PreviousReading + "$"
        dataToReceipt += CurrentReading + "$"
        dataToReceipt += EnergyConsumed + "$"
        dataToReceipt += dueDate + "$"
        dataToReceipt += billAmount + "$"
        dataToReceipt += ReconnectionFee + "$"
        dataToReceipt += creditBalance + "$"
        dataToReceipt += billBalance + "$"
        dataToReceipt += amountPaid + "$"

        print(dataToReceipt)
        accept  = "a$"
        receiptPrinter.write(accept.encode())
        print("hamborjer")
        time.sleep(5)
        receiptPrinter.write(dataToReceipt.encode())
        print("hamdesal")
        
        canvas.update

        
        #now = time.time
        #elapsedTime = int(time.time()-now)
        #while elapsedTime < now:
           # self.master.deiconify()
           # window.destroy()
           # Window.initfirst(self)
            
#2019101396013
        
            
if __name__ == "__main__":
    root = Tk()
    app = Window(root)
    app.initfirst()
    root.mainloop()