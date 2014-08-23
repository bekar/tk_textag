#!/usr/bin/env python3

import os, sys
import webbrowser
from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkFont

filepath = os.path.abspath(__file__)
fullpath = os.path.dirname(filepath)
sys.path.append(fullpath)
sys.path.append(fullpath+"/..")

import treelist as tlist
from vtk100_colors import main as vt
from tk_tooltip.main import ToolTip

font_face = (
    "default", "bold", "faint", "italic", "underline", "blink",
    "rapid-blink", "negative", "hide", "strike-out"
)

tag_list = []

def importags(tl=tag_list):
    exec(open("tag.dump").read())

class TexTag(vt.VT100):
    def __init__(self, txtwig=None, string=None):
        if txtwig and string:
            self.txtwig = txtwig
            self.loadTags(txtwig)
            self.parser(txtwig, string)

    def loadTags(self, txtwig):
        vt.VT100.loadTags(self, txtwig)
        self.tooltip = ToolTip(txtwig,
                               delay=100,
                               state="disabled",
                               follow_mouse=1
        )
        self.tooltip.motion()

    def tagSGR(self, code):
        tag = vt.VT100.tagSGR(self, code)
        if not tag: return

        if type(tag) is str:
            self.attrib[tag[-2:]] = tag[:-2]
            return

        if tag > 256: self.attrib["xx"] = tag
        elif 39 < tag < 48: self.attrib["bg"] = self.pallet8[tag-40]
        elif 29 < tag < 38: self.attrib["fg"] = self.pallet8[tag-30]
        elif 0 < tag < 10: self.attrib[font_face[tag]] = True

    def _enter(self, event, text):
        self.txtwig.config(cursor="hand2")
        self.tooltip.configure(state="normal", text=text)
        self.tooltip._schedule()

    def _leave(self, event):
        self.txtwig.config(cursor="")
        self.tooltip._unschedule()
        self.tooltip._hide()
        self.tooltip.configure(state="disable")

    def _click(self, event, label, text=None):
        ex = event.x_root
        ey = event.y_root
        if label == "url":
            webbrowser.open(text)
            return

        pop = Menu(tearoff=0)
        pop.add_command(label=label, background="lightyellow", state="disable")
        pop.add_checkbutton(label="Verifed")
        pop.add_command(label="Remove")
        pop.tk_popup(ex, ey)

    def counter(self, found):
        if "xx" in found: xx = found["xx"]
        else: xx = 0

        for tag in tag_list:
            if not tag[-3]: continue # if parent
            if isinstance(tag[-3], int):
                if xx == tag[-3]:
                    tag[1] += 1
                    return tag[0], xx
                continue

            for attrib in tag[-3]:
                if attrib == found:
                    tag[1] += 1
                    return tag[0], xx

        label = ""
        for key in found:
            label += str(key) + ":"
            label += str(self.attrib[key])

        tag_list.append([ label, 1, True, None, [ found ], True, False])
        return label, xx;

    def de_code(self, fp):
        self.attrib = dict()
        vt.VT100.de_code(self, fp)

        if self.attrib:
            label, xx = self.counter(self.attrib)
            self.txtwig.tag_add(label, self.pre, self.cur)
            self.txtwig.tag_lower(label)
            self.txtwig.tag_config(label,
                    foreground = "black",
                    background = "white",
                    font = self.txtwig['font'],
                    underline = 'false',
                    overstrike = 'false'
                )
            text = self.txtwig.get(self.pre, self.cur)
            # TODO: tooltip <Enter>, <Leave> overrid
            self.txtwig.tag_bind(label, "<Enter>", lambda e: self._enter(e, label))
            self.txtwig.tag_bind(label, "<Leave>", self._leave)
            self.txtwig.tag_bind(label, "<Button-1>", lambda e: self._click(e, label, text))

    def clean_all(self):
        # for tag in self.txtwig.tag_names():
        #     self.txtwig.tag_remove(tag, "1.0", "end")

        for tag in tag_list:
            tag[1] = 0

        self.txtwig.delete("1.0", "end")

def loadTags(tlist, cl):
    # TODO: multi-level tree (recursive)
    #[ label, count, state, parent, object, show, dump ]
    root_id = leaf_id = None
    for i, tag in enumerate(tlist):
        if not tag[-2]: continue # show bit
        if tag[-4]:
            if tag[1] == 0: continue # count
            leaf_id = cl.insert(i, tag[:3], parent=root_id)
        else: # if root
            if leaf_id:
                obj = cl.tree.item(leaf_id)
                val = obj['values']
                change = val[2].replace("├", "└")
                cl.tree.set(leaf_id, 2, change)
                leaf_id = None
            if root_id:
                obj = cl.tree.item(root_id)
                val = obj['values']
                if val[-1] == 0:
                    cl.tree.delete(root_id)
            root_id=cl.insert(i, tag[:3])

    # clear root
    obj = cl.tree.item(root_id)
    val = obj['values']

    if val[-1] == 0:
        cl.tree.delete(root_id)

    for tag in tag_list:
        tag[1] = 0

def tree_select(*events):
    #cl.tree.update_idletasks()
    sel = cl.tree.selection()
    # foc=cl.tree.focus()
    # print(sel, foc)
    if not sel: return
    for item in sel:
        toggle_select(item)
        nodes = cl.tree.get_children(item)
        for n in nodes:
            toggle_select(n)

def toggle_select(item):
    obj = cl.tree.item(item)
    val = obj['values']
    # ☒
    # TODO: state handle
    # return

    tag = tag_list[val[0]]
    if tag[2]: # if state
        state = val[2].replace('☑', '☐')
        if tag[-3]:
            ttag.txtwig.tag_raise(tag[0])
        tag[2] = False #filp state
    else:
        state = val[2].replace('☐', '☑')
        if tag[-3]:
            ttag.txtwig.tag_lower(tag[0])
        tag[2] = True # filp state

    print(state)
    cl.tree.set(item, 1, tag[2])
    cl.tree.set(item, 2, state)

    return tag[2]

if __name__ == "__main__" :
    if len(sys.argv)<2:
         print("Argument(s) Missing", file=sys.stderr); exit(1);

    root = Tk()
    root.title("textag")

    # NOTE: fix this
    import tagmap as tag
    tag_list = tag.tag_list
    importags = tag.importags
    importags()

    f = tkFont.Font(family="DejaVuSansMono", size=11)
    text = Text(font=f)

    from subprocess import check_output
    string = check_output(sys.argv[1:], universal_newlines=True)
    ttag = TexTag(text, string)

    cl = tlist.TreeList()
    cl.tree.bind('<Button-1>', lambda e: tree_select(e))
    cl.tree.bind('<space>', tree_select)

    loadTags(tag_list, cl)

    text.pack(side='left', expand=1, fill='both')
    cl.pack(side='right', expand=1, fill='both')

    root.bind('<Key-Escape>', lambda e: root.quit())
    root.bind('<Control-c>', lambda e: ttag.clean_all())

    root.mainloop()
