#!/usr/bin/python3

import os, sys
from tkinter import *

filepath=os.path.abspath(__file__)
fullpath=os.path.dirname(filepath)
sys.path.append(fullpath)

sys.path.append(fullpath+"/..")

import treelist as tlist

from vtk100_colors.main import *

def_color = [ "black", "white" ]

font_face = [
    "default", "bold", "faint", "italic", "underline", "blink", "rapid-blink",
    "negative", "hide", "strike-out"
]

tag_list = []

def importags(tl=tag_list):
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
    infile = [
        { "fg": "green" }
    ]

    #[ label, count, state, parent, object, show ]
    tl.append([ "filesys", 0, True, None, None, True ])
    tl.append([ "executable", 0, True, "filesys", exe, True ])
    tl.append([ "infile", 0, True, "filesys", infile, True ])
    tl.append([ "folder", 0, True, "filesys", folder, True ])
    tl.append([ "title", 0, True, None, title, True ])
    tl.append([ "code", 0, True, None, code, True ])

class textag(vt100tk):
    def __init__(self, parent, txt_wig, string=None):
        vt100tk.__init__(self, txt_wig)
        self.isapp=True
        self.ex_tmp=None
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

    def reset_count(self):
        for tag in tag_list:
            tag[1]=0

def loadTags(tlist, cl):
    root_id=leaf_id=None
    for i, tag in enumerate(tlist):
        if not tag[-1]: continue # show bit
        if tag[-3]:
            if tag[1]==0: continue
            leaf_id=cl.insert(i, tag[:3], parent=root_id)
        else:
            if leaf_id:
                obj=cl.tree.item(leaf_id)
                val=obj['values']
                change=val[1].replace("├", "└")
                cl.tree.set(leaf_id, 1, change)
                leaf_id=None
            if root_id:
                obj=cl.tree.item(root_id)
                val=obj['values']
                if val[-1]==0:
                    cl.tree.delete(root_id)
            root_id=cl.insert(i, tag[:3])

    obj=cl.tree.item(root_id)
    val=obj['values']
    if val[-1]==0:
        cl.tree.delete(root_id)

def tree_select(*events):
    #cl.tree.update_idletasks()
    sel=cl.tree.selection()
    # foc=cl.tree.focus()
    # print(sel, foc)
    if not sel: return
    for item in sel:
        toggle_select(item)
        nodes=cl.tree.get_children(item)
        for n in nodes:
            toggle_select(n)

def toggle_select(item):
    obj=cl.tree.item(item)
    val=obj['values']
    #☒
    tag=tag_list[val[0]]
    if tag[2]:
        state=val[1].replace('☑', '☐')
        if tag[-2]:
            ttag.txtwig.tag_raise(tag[0])
        tag[2]=False
    else:
        state=val[1].replace('☐', '☑')
        if tag[-2]:
            ttag.txtwig.tag_lower(tag[0])
        tag[2]=True

    print(state)
    cl.tree.set(item, 1, state)
    return tag[2]

if __name__ == "__main__" :
    if len(sys.argv)<2:
         print("Argument(s) Missing", file=sys.stderr); exit(1);

    root=Tk()
    root.title("textag")
    importags()

    text=Text(root, font=def_font)

    from subprocess import check_output
    string=check_output(sys.argv[1:], universal_newlines=True)
    ttag=textag(root, text, string)

    cl=tlist.TreeList()
    cl.tree.bind('<Button-1>', lambda e: tree_select(e))
    cl.tree.bind('<space>', tree_select)

    loadTags(tag_list, cl)

    text.pack(side=LEFT, expand=YES, fill=BOTH)
    cl.pack(side=RIGHT, expand=YES, fill=BOTH)

    root.bind('<Key-Escape>', lambda event: quit())
    root.mainloop()
