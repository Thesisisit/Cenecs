from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk


def back(window):
    root.deiconify()
    window.destroy()





def final(x):
    window = Toplevel(root)
    x.withdraw()
    swidth = window.winfo_screenwidth()
    sheight = window.winfo_screenheight()
    window.geometry(f"{swidth}x{sheight}")
    load = Image.open("C:\\Users\\Electric-Post.png")
    load = load.resize((swidth, sheight), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    img = Label(window, image=render)
    img.image = render
    img.place(x=0, y=0)
    button = Button(window, text="Press BACK to Eject Money", bg="Green", fg="Black", command=lambda:back(window), font = ("TimesNewRoman 24"), justify="center")
    button.place(x=450, y=750)
    button = Button(window, text="Press OK to proceed", bg="Green", fg="Black", command=lambda: final(window), font = ("TimesNewRoman 24"), justify="center")
    button.place(x=1000, y=750)
    container1 = Frame(window, width=750, height=350, bg='#b6b6b6')
    container1.pack(fill=BOTH, padx= 800, ipady=50)
    container1.place(anchor=CENTER, relx=.48, rely=.5)
    window.bind('<Return>', lambda:final)


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        swidth = self.winfo_screenwidth()
        sheight = self.winfo_screenheight()

        load = Image.open("Electric-Post.png")
        load = load.resize((swidth, sheight), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        can = Canvas(self, height=100, width=20)
        can.place(relx=0.5, rely=0.5, anchor=CENTER)
        entry = Entry(can, font=("Calibri 100"), justify="center")
        entry.pack(ipady=3)
        entry.focus()
    def add_window(self,):
        window = Toplevel(root)
        Frame.deiconify
if __name__ == "__main__":
    root = Tk()
    app = Window(root)
    root.wm_title("CENECO PAYMENT MACHINE")
    root.geometry("1920x1080")
    button = Button(root,  text="Press ENTER to Confirm", bg="Green", fg="Black",width=20, command= Window.add_window, font = ("TimesNewRoman 24"), justify="center")
    button.place(x=750, y=650)
    #root.bind('<Return>', create_window)
    root.bind('<0>', final)
    root.mainloop()


