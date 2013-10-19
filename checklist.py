#!/usr/bin/python3

from tkinter import *

class CheckList(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.makeWidgets()

    def makeWidgets(self):
        self.cstack = []

        self.frame_check=Frame(self)
        bar=Frame(self)

        self.frame_check.config(bg="white", bd=2)
        self.frame_check.config(width="100", height="100")

        self.label_stack=Label(self, anchor=W)
        self.top = IntVar()
        self.top.trace('w', self.status)
        self.top.set(0)

        self.button_pus=Button(bar, text="+", command=lambda: self.push())
        self.button_pop=Button(bar, text="-", command=self.pop)
        self.button_selAll=Button(bar, text="☑", command=self.selAll)
        self.button_selInv=Button(bar, text="ɐ", command=self.selInv)

        self.button_reset=Button(bar, text="♻", command=self.selInv)

        #packing
        self.button_pus.pack(side=LEFT, anchor=NW)
        self.button_pop.pack(side=LEFT, anchor=NW)
        self.button_selAll.pack(side=LEFT, anchor=NW)
        self.button_selInv.pack(side=LEFT, anchor=NW)
        self.button_reset.pack(side=LEFT, anchor=NW)

        bar.pack(side=TOP)
        self.label_stack.pack(side=BOTTOM, fill=X)
        self.frame_check.pack(side=BOTTOM, expand=YES, fill=BOTH)

    def status(self, *events):
        self.label_stack.config(text=str(self.top.get()))

    def selAll(self):
        for obj in self.cstack:
            obj.select()

    def selInv(self):
        for obj in self.cstack:
            obj.toggle()

    def packing(self):
        for item in stats:
            if item[1]==1 and item[2]!=0:
                add(self, "[ %s ] %d"%(item[0], item[0]))

    def add(self, label):
        t=self.top.get()
        self.insert(label, t)
        self.top.set(t+1)
        return t

    def insert(self, label, pos):
        obj=Checkbutton(self.frame_check, text=label, anchor=NW, font="DejaVuSansMono 10")
        self.cstack.insert(pos, obj)
        obj.pack(fill=BOTH)

    def push(self):
        t=self.top.get()
        self.add(str(t))

    def pop(self):
        t=self.top.get()-1
        if t<0: return
        self.cstack[t].pack_forget()
        del self.cstack[t]
        self.top.set(t)

    def selAll(self):
        for i in self.cstack:
            i.select()

if __name__ == "__main__" :
    root=Tk()
    cl=CheckList()
    cl.pack()
    root.bind('<Key-Escape>', lambda e: quit())
    root.mainloop()
