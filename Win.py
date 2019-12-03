from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.master.destroy
        swidth = self.winfo_screenwidth()
        sheight = self.winfo_screenheight()
        master.wm_title("CENECO PAYMENT MACHINE")
        master.geometry("1920x1080")
        load = Image.open("Electric-Post.png")
        load = load.resize((swidth, sheight), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)
        
    def initfirst(self):
        can = Canvas(self, height=100, width=20)
        can.place(relx=0.5, rely=0.5, anchor=CENTER)
        button1 = Button(self,  text="Press ENTER to Confirm", bg="Green", fg="Black",width=20, command=lambda:Window.nextwindow(self),font = ("TimesNewRoman 24"), justify="center")
        button1.place(x=750, y=650)
        self.master.bind('<Return>',lambda x:Window.nextwindow(self))
        entry = Entry(can, font=("Calibri 100"), justify="center")
        entry.pack(ipady=3)
        entry.focus()
        # if state !=0:
            
    def nextwindow(self):
        window = Toplevel(self)
        Window(window)
        self.master.withdraw()
        window.focus_force()
        button1 = Button(window, text="Press BACK to Eject Money", bg="Green", fg="Black", command=lambda :Window.back(self,window), font = ("TimesNewRoman 24"), justify="center")
        button1.place(x=450, y=750)
        button2 = Button(window, text="Press OK to proceed", bg="Green", fg="Black", command=lambda: Window.final(self,window), font = ("TimesNewRoman 24"), justify="center")
        button2.place(x=1000, y=750)
        window.bind('<Return>',lambda y:Window.final(self,window))
        window.bind('<g>', lambda y:Window.back(self,window))

    def back(self,window):
        self.master.deiconify()
        window.destroy()
        Window.initfirst(self)
    def backtosecond(self,window):
        window.destroy()
        Window.nextwindow(self)
    def final(self,prevwindow):
        window = Toplevel(self)
        Window(window)
        window.focus_force()
        prevwindow.destroy()
        window.bind('<Return>',lambda y:Window.back(self,window))
        button = Button(window, text="Press back to first", bg="Green", fg="Black", command=lambda :Window.back(self,window), font = ("TimesNewRoman 24"), justify="center")
        button.place(x=450, y=750)
        button = Button(window, text="Press here to proceed to 2nd", bg="Green", fg="Black", command=lambda: Window.backtosecond(self,window), font = ("TimesNewRoman 24"), justify="center")
        button.place(x=1000, y=750)
