#!/usr/bin/python3

import os, sys
from tkinter import *
from tkinter import tix
import checklist as clist
import treelist as tlist

filepath=os.path.abspath(__file__)
fullpath=os.path.dirname(filepath)
sys.path.append(fullpath+"/..")

from vtk100_colors.main import *

def_color = [ "black", "white" ]

font_face = [
    "default", "bold", "faint", "italic", "underline", "blink", "rapid-blink",
    "negative", "hide", "strike-out"
]

tag_list = []

def load_tags(tl=tag_list):
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

    tl.append([ True, title, True, "title", 0 ])
    tl.append([ True, code, True, "code", 0 ])
    tl.append([ True, exe, True, "executable", 0 ])
    tl.append([ True, folder, True, "folder", 0 ])

class textag(vt100tk):
    def __init__(self, parent=None, txt_wig=None, cl_wig=None, string=None):
        vt100tk.__init__(self, txt_wig)
        self.cl=cl_wig
        self.ex_tmp=None
        self.cl.config(browsecmd=self.selectItem)
        self.stats = dict()
        if string: self.parser(string)
        cl2.loadTags(tag_list)
        cl3.loadTags(tag_list)
        self.loadTags(tag_list)

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
        elif 39 < tag < 48: self.attrib["bg"]=pallet8[tag-40]
        elif 29 < tag < 38: self.attrib["fg"]=pallet8[tag-30]
        elif 0 < tag < 10: self.attrib[font_face[tag]]=True
        else: self.attrib["unknown"]=tag
        if self.ex_tmp: self.attrib[self.ex_tmp]=int(tag[2:]); self.ex_tmp=None

    def makelabel(self, found):
        for i, tag in enumerate(tag_list):
            for attrib in tag[1]:
                if attrib == found:
                    tag_list[i][-1]+=1
                    return tag[-2];

        label=""
        for key in found:
            label += str(key)+":"
            label += str(self.attrib[key])

        tag_list.append([ True, [ found ], True, label, 1 ])
        return label;

    def de_code(self, fp, pre, cur):
        self.attrib = dict()
        label=vt100tk.de_code(self, fp, pre, cur)
        if self.attrib:
            label=self.makelabel(self.attrib)
            self.txtwig.tag_add(label, pre, cur)
            self.txtwig.tag_lower(label)
            self.txtwig.tag_config(label,
                    foreground = "black",
                    background = "white",
                    font = def_font,
                    underline = FALSE,
                    overstrike = FALSE
                )

    def loadTags(self, tlist):
        for tag in tlist:
            if tag[0]:
                self.cl.hlist.add(tag[-2], text="[ %s ] %d"%(tag[-2], tag[-1]))
                self.cl.setstatus(tag[-2], "on")

    def state_active(self, tag):
        self.txtwig.tag_raise(tag)

    def state_inactive(self, tag):
        self.txtwig.tag_lower(tag)

    def selectItem(self, item):
        status=self.cl.getstatus(item)
        print(item, status)
        if status == "off":
            self.txtwig.tag_raise(tag)
        else:
            self.txtwig.tag_lower(item)

        self.cl.hlist.selection_clear()

def tree_select(*events):
    sel=cl3.tree.selection()
    if not sel: return
    for item in sel:
        obj=cl3.tree.item(item)
        val=obj['values']
        if val[0] == '☑':
            state = '☐'
            ttag.state_active(val[1])
        else:
            state = '☑'
            ttag.state_inactive(val[1])

        cl3.tree.set(item, 0, state)


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

    clist.root=root
    cl2=clist.CheckList()

    clist.root=root
    cl3=tlist.TreeList()
    cl3.tree.bind('<Button-1>', tree_select)

    from subprocess import check_output
    string=check_output(sys.argv[1:], universal_newlines=True)
    ttag=textag(root, text, cl, string)

    text.config(width=50)
    cl3.config(width=25)

    text.pack(side=LEFT, expand=YES, fill=BOTH)
    cl3.pack(side=RIGHT, expand=YES, fill=BOTH)
    cl2.pack(side=RIGHT, expand=YES, fill=BOTH)
    cl.pack(side=RIGHT, expand=YES, fill=BOTH)

    #root.maxsize(root.winfo_screenwidth()-200, 200)
    root.bind('<Key-Escape>', lambda event: quit())
    root.mainloop()
