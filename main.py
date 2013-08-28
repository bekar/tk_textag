#!/usr/bin/python3

import os, sys
from tkinter import *
from tkinter import tix

from vtk100_colors.main import *

def_color = [ "black", "white" ]

font_face = [
    "default", "bold", "faint", "italic", "underline", "blink", "rapid-blink",
    "negative", "hide", "strike-out"
]

class textag(vt100tk):
    def __init__(self, txt_wig, string=None):
        vt100tk.__init__(self, txt_wig)
        if string: self.parser(string)

    def tag_sgr(self, code, pre, cur):
        if not code: return
        tag=int(code)
        if tag == 0: return
        if   self.extend == 53: tag="bg"+code; # 38+5+code
        elif self.extend == 43: tag="fg"+code; # 48+5+code
        elif self.extend: self.extend+=tag; return; #2nd skip
        elif tag in [ 38, 48 ]: self.extend=tag; return;
        self.tag_me(tag) # extention hook
        self.txtwig.tag_add(tag, pre, cur)

    def tag_me(self, tag):
        if   self.extend: self.label.append(tag); self.extend=0;
        elif 39 < tag < 48: self.label.append("bg:"+pallet8[tag-40])
        elif 29 < tag < 38: self.label.append("fg:"+pallet8[tag-30])
        elif 0 < tag < 10: self.label.append(font_face[tag])
        elif self.extend==53: self.label.append("bg")
        elif self.extend==43: self.label.append("fg")
        else: self.label.append("unknown:"+str(tag))

    def de_code(self, fp, pre, cur):
        self.label = []
        vt100tk.de_code(self, fp, pre, cur)
        if self.label:
            global cl
            #id="cl"+str(self.tag_found)
            id = str(self.label)
            try:
                cl.hlist.add(id, text=id)
                cl.setstatus(id, "on")
            except Exception as e:
                cl.hlist.item_configure(id, col=0, text=id+"+")

            self.txtwig.tag_add(id, pre, cur)

def selectItem(item):
    e=root.event_info()#.Event()
    print(e)
    print(dir(e))
    #print(e[0].type)
    #print(tix.Event)
    #print(tix.Event.__doc__)
    #if tix.Event == "<ButtonRelease>":
    #    print("hello")
    #print(cl.event_info())
    #root.idea
    status=cl.getstatus(item)
    print(item, status)
    if status == "off":
        text.tag_config(item,
                        foreground = "black",
                        background = "white",
                        font = def_font,
                        underline = FALSE,
                        overstrike = FALSE,
        )
        text.tag_raise(item)
    else:
        text.tag_lower(item)

    cl.hlist.selection_clear()

def test_me(*event):
    print(event[0].type)

if __name__ == "__main__" :
    if len(sys.argv)<2:
         print("Argument(s) Missing", file=sys.stderr); exit(1);
    root=tix.Tk()

    #pan=PanedWindow(root)
    text=Text(root, font=def_font)
    #pan.add(text)

    frame=Frame(root)
    cl=tix.CheckList(frame, browsecmd=selectItem)#, exportselection=1)
    cl.hlist.config(background="#e2e2e2")
    #cl.hlist['background'] = "#e2e2e2"
    #pan.add(frame)

    from subprocess import check_output
    vtk=textag(text, check_output(sys.argv[1:], universal_newlines=True))
    #vtk=vt100tk(text, test_string)

    text.pack(side=LEFT, expand=YES, fill=BOTH)
    cl.pack(expand=YES, fill=BOTH)
    cl.autosetmode()
    frame.pack(side=RIGHT, expand=YES, fill=BOTH)
    #pan.pack(fill=BOTH, expand=YES)

    root.bind('<Key-Escape>', quit)
    #root.bind('<ButtonRelease>', test_me)
    root.mainloop()
