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

tag_list = dict()

def load_tags():
    title = [
       { "fg": "red", "bold": True, "underline": True }
    ]
    code = [
        { "fg": "blue", "italic": True }
    ]
    exe = [
        { "fg": "green", "bold": True }
    ]
    folder = [
        { "fg": "blue", "bold": True }
    ]

    global tag_list
    tag_list[" Title "] =  [ 0, title ]
    tag_list[" code "] =  [ 0, code ]
    tag_list[" executable "] =  [ 0, exe ]
    tag_list[" folder "] =  [ 0, folder ]


class textag(vt100tk):
    def __init__(self, parent=None, txt_wig=None, cl_wig=None, string=None):
        vt100tk.__init__(self, txt_wig)
        self.cl=cl_wig
        self.ex_tmp=None
        self.cl.config(browsecmd=self.selectItem)
        self.stats = dict()
        if string: self.parser(string)

    def tag_sgr(self, code, pre, cur):
        if not code: return
        tag=int(code)
        if tag == 0: return
        if   self.extend == 53: tag="bg"+code; # 48+5+code
        elif self.extend == 43: tag="fg"+code; # 38+5+code
        elif self.extend: self.extend+=tag; return; #2nd skip
        elif tag in [ 38, 48 ]: self.extend=tag; return;
        self.tag_me(tag) # extention hook
        self.txtwig.tag_add(tag, pre, cur)

    def tag_me(self, tag):
        #print("tag", tag, self.ex_tmp)
        if   self.extend==53: self.ex_tmp="bg"; self.extend=0;
        elif self.extend==43: self.ex_tmp="fg"; self.extend=0;
        elif 39 < tag < 48: self.label["bg"]=pallet8[tag-40]
        elif 29 < tag < 38: self.label["fg"]=pallet8[tag-30]
        elif 0 < tag < 10: self.label[font_face[tag]]=True
        else: self.label["unknown"]=tag
        if self.ex_tmp: self.label[self.ex_tmp]=int(tag[2:]); self.ex_tmp=None

    def makelabel(self, label):
        for key in tag_list:
            for tag in tag_list[key][1]:
                if tag == label:
                   return (tag_list[key][0], key)

        id = " "
        for key in self.label:
            id += str(key)+":"
            id += str(self.label[key])
            id += " "

        return (0, id)

    def de_code(self, fp, pre, cur):
        self.label = dict()
        vt100tk.de_code(self, fp, pre, cur)
        if self.label:
            wflag, id = self.makelabel(self.label)
            try:
                self.cl.hlist.add(id, text="[%s] 1"%id)
                self.cl.setstatus(id, "on")
                self.stats[id]=1
            except Exception as e:
                self.stats[id]+=1
                self.cl.hlist.item_configure(id, col=0, text="[%s] %s"%(id,str(self.stats[id])))

            self.txtwig.tag_add(id, pre, cur)
            if wflag > 0:
                self.printag(id, self.txtwig.get(pre,cur))

    def printag(self, id, text):
        print(id, text)

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
            self.txtwig.tag_config(item,
                    foreground = "black",
                    background = "white",
                    font = def_font,
                    underline = FALSE,
                    overstrike = FALSE,
                )
            self.txtwig.tag_raise(item)
        else:
            self.txtwig.tag_lower(item)

        self.cl.hlist.selection_clear()

if __name__ == "__main__" :
    if len(sys.argv)<2:
         print("Argument(s) Missing", file=sys.stderr); exit(1);

    root=tix.Tk()
    root.title("textag")
    load_tags()

    text=Text(root, font=def_font)

    cl=tix.CheckList()
    cl.hlist.config(background="#e5e5e5")
    cl.autosetmode()

    from subprocess import check_output
    string=check_output(sys.argv[1:], universal_newlines=True)
    vtk=textag(root, text, cl, string)
    text.pack(side=LEFT, expand=YES, fill=BOTH)
    cl.pack(side=RIGHT, expand=YES, fill=BOTH)
    root.bind('<Key-Escape>', lambda event: quit())
    root.mainloop()
