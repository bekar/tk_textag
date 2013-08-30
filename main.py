#!/usr/bin/python3

import os, sys
from tkinter import *
from tkinter import tix

filepath=os.path.abspath(__file__)
fullpath=os.path.dirname(filepath)
sys.path.append(fullpath+"/..")

if __name__ == '__main__':
    from vtk100_colors import *
else:
    from lib.vtk100_colors import *

def_color = [ "black", "white" ]

font_face = [
    "default", "bold", "faint", "italic", "underline", "blink", "rapid-blink",
    "negative", "hide", "strike-out"
]

class textag(Frame, vt100tk):
    def __init__(self, parent=None, txt_wig=None, string=None):
        Frame.__init__(self, parent)
        self.cl=tix.CheckList(self, browsecmd=self.selectItem)
        self.cl.hlist.config(background="#e5e5e5")
        self.cl.pack(expand=YES, fill=BOTH)
        self.cl.autosetmode()
        self.pack(side=RIGHT, expand=YES, fill=BOTH)
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
            #id="cl"+str(self.tag_found)
            id = str(self.label)
            try:
                self.cl.hlist.add(id, text=id)
                self.cl.setstatus(id, "on")
            except Exception as e:
                self.cl.hlist.item_configure(id, col=0, text=id+"+")

            self.txtwig.tag_add(id, pre, cur)

    def selectItem(self, item):
        # e=root.event_info()#.Event()
        # print(e)
        # print(dir(e))
        # print(e[0].type)
        # print(tix.Event)
        # print(tix.Event.__doc__)
        # print(cl.event_info())
        status=self.cl.getstatus(item)
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

        self.cl.hlist.selection_clear()

if __name__ == "__main__" :
    if len(sys.argv)<2:
         print("Argument(s) Missing", file=sys.stderr); exit(1);
    root=tix.Tk()

    text=Text(root, font=def_font)

    from subprocess import check_output
    string=check_output(sys.argv[1:], universal_newlines=True)
    vtk=textag(root, text, string)
    text.pack(side=LEFT, expand=YES, fill=BOTH)

    root.bind('<Key-Escape>', quit)
    root.mainloop()
