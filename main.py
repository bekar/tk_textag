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

    #tl.append([ "label", count, state, parent, object, show ])
    tl.append([ "filesys", 0, True, None, None, True ])
    tl.append([ "executable", 0, True, "filesys", exe, True ])
    tl.append([ "folder", 0, True, "filesys", folder, True ])
    tl.append([ "title", 0, True, None, title, True ])
    tl.append([ "code", 0, True, None, code, True ])

class textag(vt100tk):
    def __init__(self, parent, txt_wig, string=None):
        vt100tk.__init__(self, txt_wig)
        self.isapp=True
        self.ex_tmp=None
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
        elif 39 < tag < 48: self.attrib["bg"]=pallet8[tag-40]
        elif 29 < tag < 38: self.attrib["fg"]=pallet8[tag-30]
        elif 0 < tag < 10: self.attrib[font_face[tag]]=True
        else: self.attrib["unknown"]=tag
        if self.ex_tmp: self.attrib[self.ex_tmp]=int(tag[2:]); self.ex_tmp=None

    def counter(self, found):
        for tag in tag_list:
            if tag[-2] == None: continue
            for attrib in tag[-2]:
                if attrib == found:
                    tag[1]+=1
                    return tag[0]

        label=""
        for key in found:
            label += str(key)+":"
            label += str(self.attrib[key])

        tag_list.append([ label, 1, True, None, [ found ], True])
        return label;


    def _enter(self, event):
        self.txtwig.config(cursor="hand2")

    def _leave(self, event):
        self.txtwig.config(cursor="")

    def _click(self, event, text):
        ex=event.x_root
        ey=event.y_root
        tooltip = Menu(tearoff=0)
        tooltip.add_command(label=text)
        tooltip.tk_popup(ex,ey)

    def de_code(self, fp, pre, cur):
        self.attrib = dict()
        label=vt100tk.de_code(self, fp, pre, cur)
        if self.attrib:
            label=self.counter(self.attrib)
            self.txtwig.tag_add(label, pre, cur)
            self.txtwig.tag_lower(label)
            self.txtwig.tag_config(label,
                    foreground = "black",
                    background = "white",
                    font = def_font,
                    underline = FALSE,
                    overstrike = FALSE
                )
            self.txtwig.tag_bind(label, "<Enter>", self._enter)
            self.txtwig.tag_bind(label, "<Leave>", self._leave)
            self.txtwig.tag_bind(label, "<Button-1>", lambda e: self._click(e, label))

def loadTags(tlist):
    for tag in tlist:
        if tag[2]:
            if tag[-3]:
                c1label="   %-15s%d"%(tag[0], tag[1])
                print(tag[0], tag[-3])
                cl2.insert(tag[:3], parent=obj)
            else:
                c1label="%-18s%d"%(tag[0], tag[1])
                obj=cl2.insert(tag[:3])

            cl1.add(c1label)
            cl3.hlist.add(tag[0], text="[ %s ] %d"%(tag[0], tag[1]))
            cl3.setstatus(tag[0], "on")

def tree_select(*events):
    cl2.tree.update_idletasks()
    sel=cl2.tree.selection()
    # foc=cl2.tree.focus()
    # print(sel, foc)
    if not sel: return
    for item in sel:
        obj=cl2.tree.item(item)
        val=obj['values']
        if val[0] == '☑':
            state = '☐'
            ttag.txtwig.tag_raise(val[1])
        else:
            state = '☑'
            ttag.txtwig.tag_lower(val[1])
        print(val[1], state)
        cl2.tree.set(item, 0, state)

def selectItem(item):
    status=cl3.getstatus(item)
    print(item, status)
    if status == "off":
        ttag.txtwig.tag_raise(item)
    else:
        ttag.txtwig.tag_lower(item)

    cl3.hlist.selection_clear()

if __name__ == "__main__" :
    if len(sys.argv)<2:
         print("Argument(s) Missing", file=sys.stderr); exit(1);

    root=tix.Tk()
    root.title("textag")
    load_tags()

    text=Text(root, font=def_font)

    from subprocess import check_output
    string=check_output(sys.argv[1:], universal_newlines=True)
    ttag=textag(root, text, string)

    cl1=clist.CheckList()
    cl2=tlist.TreeList()
    #cl2.tree.bind('<Button-1>', lambda e: tree_select(e))
    cl2.tree.bind('<space>', tree_select)
    cl3=tix.CheckList(browsecmd=selectItem)
    cl3.autosetmode()

    loadTags(tag_list)
    text.config(width=50)

    text.pack(side=LEFT, expand=YES, fill=BOTH)
    cl3.pack(side=RIGHT, expand=YES, fill=BOTH)
    cl2.pack(side=RIGHT, expand=YES, fill=BOTH)
    cl1.pack(side=RIGHT, expand=YES, fill=BOTH)

    root.bind('<Key-Escape>', lambda event: quit())
    root.mainloop()
