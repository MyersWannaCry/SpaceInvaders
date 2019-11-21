from tkinter import *
#================Input.txt======================
t =  open('scoreboard.txt' , 'r')
#=================Window_Name================
top = Tk()
top.title("Scoreboard")
top.geometry("200x250")
L = Label(top, text = t.read(), font=("Arial Bold", 20) )

#===============Exit============================
def exit ():
    top.destroy()
#==================Button=====================
E = Button(top, text="Quit", command= exit)

E.place(x = 100, y = 200)
L.pack()
top.mainloop()
t.close()
