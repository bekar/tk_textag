#!/usr/bin/python3.3

from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

#CURRENT_ITEM=None
list_col = [
    ["", "Tag", "#"],
    [10, 150, 30]
]

class TreeList(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.visible = True
        self.top=0
        self.makeWidgets()
        self.makePopUp()
        self.binding()

    def makeWidgets(self):
        lst=Frame(self)
        bar=Frame(self)

        # toolbar
        self.button_pus=Button(bar, text="+", command=lambda: self.push())
        self.button_pop=Button(bar, text="-")#, command=self.pop)
        self.button_selAll=Button(bar, text="☑")#, command=self.selAll)
        self.button_selInv=Button(bar, text="ɐ")#, command=self.selInv)
        self.button_reset=Button(bar, text="♻")#, command=self.selInv)

        # packing
        self.button_pus.pack(side=LEFT, anchor=NW)
        self.button_pop.pack(side=LEFT, anchor=NW)
        self.button_selAll.pack(side=LEFT, anchor=NW)
        self.button_selInv.pack(side=LEFT, anchor=NW)
        self.button_reset.pack(side=LEFT, anchor=NW)

        # treeview
        self.tree = ttk.Treeview(self, show="headings", columns=list_col[0])
        self.tree.config(selectmode='extended')
        #self.tree.config(height=8)

        # header
        for c, w in zip(list_col[0], list_col[1]):
            self.tree.heading(c, text=c, command=lambda col=c: self.sortby(col, 0))
            self.tree.column(c, width=w, minwidth=w)

        # scrollbar
        # vsb = Scrollbar(orient="vertical", command=self.tree.yview, takefocus=0)
        # hsb = Scrollbar(orient="horizontal", command=self.tree.xview, takefocus=0)
        # self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # grid
        #self.tree.grid(column=0, row=0, sticky='news', in_=self)
        self.tree.pack(fill=BOTH, expand=YES)
        # vsb.grid(column=1, row=0, sticky='ns', in_=self)
        # hsb.grid(column=0, row=1, sticky='ew', in_=self)

        bar.pack(side=BOTTOM, fill=BOTH, expand=YES)
        #lst.pack(side=TOP, fill=BOTH, expand=YES)


        # self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)

    def binding(self):
        self.tree.bind('<Button-3>', self.call_popup)
        #self.tree.bind('<<TreeviewSelect>>', self.select)
        #self.tree.bind('<Button-1>', self.select)

    def call_popup(self, event):
        global POP_SELECT
        ex=event.x_root
        ey=event.y_root
        offset=19*1
        #print(ex, ey, offset)
        self.popup.tk_popup(ex,ey)
        POP_SELECT=ttk.Treeview.identify(self.tree, component='item', x=ex, y=ey-offset)
        self.tree.selection_set(POP_SELECT)
        self.tree.focus(POP_SELECT)
        self.tree.focus_set()

    def makePopUp(self):
        popup = Menu(tearoff=0)
        popup.add_command(label="Rescan", command=lambda: rescan())
        popup.add_command(label="Built Report")

        popup.add_command(label="Copy Path", command=None)
        popup.add_checkbutton(label="Bad Marker")

        subm_export = Menu(popup, tearoff=False)
        subm_export.add_command(label="color to pdf", command=None)
        subm_export.add_command(label="xml to pdf")

        subm_export.add_separator()
        subm_export.add_command(label="More")
        popup.add_cascade(label="Export", menu=subm_export, underline=0)

        popup.add_separator()
        popup.add_command(label="Properties", command=self.article_properties)

        self.popup=popup

    def sortby(self, col, descending): #column click sort
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]

        data.sort(reverse=descending)
        for i, item in enumerate(data):
            self.tree.move(item[1], '', i)

        # switch the heading so that it will sort in the opposite direction
        self.tree.heading(col,
            command=lambda col=col: self.sortby(col, int(not descending)))

    def insert(self, data, pos='end'):
        if data[0]: state='☑'
        else: state='☐'
        row = [ state , data[1], data[2] ]
        select=self.tree.insert('', pos, value=row)
        self.top+=1

    def push(self):
        row = [ '☑', str(self.top), 0 ]
        self.insert(row)

    def loadTags(self, tlist):
        for i, tag in enumerate(tlist):
            if tag[0]:
                self.insert(tag[-3:])

    def article_properties(self):
        win=Toplevel()#padx=7, pady=7)
        win.title("Properties")
        win.bind('<Key-Escape>', lambda event: win.destroy())
        Label(win, text="hello").pack()

    def clear_tree(self):
        x = self.tree.get_children()
        for item in x: self.tree.delete(item)

    def select(self, *events):
        focus=self.tree.focus()
        if not focus: return
        sel=self.tree.item(focus)
        val=sel['values']
        if val[0] == '☑':
            state = '☐'
            tree_active(focus)
        else:
            state = '☑'
            tree_inactive(focus)

        self.tree.set(focus, 0, state)

def tree_active(focus): print(focus, "active")
def tree_inactive(focus): print(focus, "inactive")


if __name__ == '__main__':
    root = Tk()

    tl=TreeList()
    tl.pack(fill=BOTH, expand=YES)

    root.bind('<Key-Escape>', lambda e: exit())
    root.mainloop()
