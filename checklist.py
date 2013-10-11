#!/usr/bin/python3

import os, sys
from tkinter import *

class checklist(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.makeWidgets()
        self.bindings()

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

    def bindings(self):
        root.bind('<Key-a>', lambda e: self.push())
        root.bind('<Key-d>', lambda e: self.pop())
        root.bind('<Control-a>', lambda e: self.selAll())
        root.bind('<Control-i>', lambda e: self.selInv())

    def selAll(self):
        for obj in self.cstack:
            obj.select()

    def selInv(self):
        for obj in self.cstack:
            obj.toggle()

    # def countplus(self, id):
    #     self.cstack[self.top.get()].config(text=

    def add(self, label):
        t=self.top.get()
        obj=Checkbutton(self.frame_check, text=label, anchor=NW)
        self.cstack.append(obj)
        self.top.set(t+1)
        obj.pack(fill=BOTH)
        return t
        # obj.bind("<Button-1>", lambda e: obj.config(bg="blue"))
        # obj.bind("<Enter>", None)
        # obj.bind("<Leave>", None)
        # obj.bind("<FocusIn>", None)
        # obj.bind("<FocusOut>", None)

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
    cl=checklist()
    cl.pack()
    root.bind('<Key-Escape>', lambda e: quit())
    root.mainloop()
