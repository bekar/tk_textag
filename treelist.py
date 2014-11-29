#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

col_attrib = (
   #[ "id", "label", min-width, width, stretch, show ],
    ( "#0", "", 20, 20, 0, True ),
    ( "i", "i", 10, 10, 0, False ),
    ( "state", "state", 10, 10, 0, False ),
    ( "tag", "tag", 150, 200, 1, True ),
    ( "count", "count", 25, 50, 0, True )
)

cols = [ "i", "state", "tag", "count" ]

class TreeList(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.visible = True
        self.top=0
        self.makeWidgets()
        self.makePopUp()
        self.binding()


    def makeWidgets(self):
        bar=Frame(self)
        bar.pack(side='bottom')
        button_lst = (
            ( '+', self.push ),
            ( "-", self.pop ),
            ( "☑", self.selAll ),
            ( "ɐ", self.selInv ),
            ( "♻", self.refresh )
        )

        for t, f in button_lst:
            btn = Button(bar, text=t, takefocus=0, command=f)
            btn.pack(side='left', anchor='nw')

        # treeview
        tls=Frame(self)
        tls.pack(side='top', fill='both', expand=1)

        self.tree = ttk.Treeview(tls, columns=cols, displaycolumns=cols[2:])
        self.tree.config(selectmode='extended')

        # make header
        for i, txt, mwid, wid, streh, show in col_attrib:
            if not show: continue
            self.tree.heading(i, text=txt)
            self.tree.heading(i, command=lambda a=i: self.sortby(a, 0))
            self.tree.column(i, minwidth=mwid, width=wid, stretch=streh)

        # scrollbar
        vsb = ttk.Scrollbar(tls, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=lambda f, l: autoscroll(vsb, f, l))
        hsb = ttk.Scrollbar(tls, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=lambda f, l: autoscroll(hsb, f, l))

        # grid
        self.tree.grid(row=0, column=0, sticky='news')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        tls.columnconfigure(0, weight=1)
        tls.rowconfigure(0, weight=1)


    def binding(self):
        self.tree.bind('<Button-3>', self.call_popup)
        #self.tree.bind('<<TreeviewSelect>>', self.select)
        #self.tree.bind('<Button-1>', self.select)


    def call_popup(self, event):
        ex=event.x_root
        ey=event.y_root
        offset=19*1
        #print(ex, ey, offset)
        focus=ttk.Treeview.identify(self.tree, component='item', x=ex, y=ey-offset)
        if not focus: return
        self.tree.selection_set(focus)
        self.tree.focus(focus)
        self.tree.focus_set()
        self.popup.tk_popup(ex,ey)


    def makePopUp(self):
        popup = Menu(tearoff=0)
        popup.add_command(label="menu 1", command=lambda: rescan())

        subm = Menu(popup, tearoff=False)
        subm.add_command(label="submenu 1")
        subm.add_command(label="submenu 2")
        popup.add_cascade(label="menu 2", menu=subm, underline=0)

        popup.add_separator()
        popup.add_command(label="menu 3", command=self.article_properties)

        self.popup=popup


    def sortby(self, col, descending): #column click sort
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]

        data.sort(reverse=descending)
        for i, item in enumerate(data):
            self.tree.move(item[1], '', i)

        # switch the heading so that it will sort in the opposite direction
        self.tree.heading(col,
            command=lambda col=col: self.sortby(col, int(not descending)))


    def insert(self, i, data, pos=END, parent=''):
        state=""
        if parent:
            state=" ├─"
            count=data[1]
            obj=self.tree.item(parent)
            val=obj['values']
            count+=val[-1]
            self.tree.set(parent, 3, count)

        if data[-1]: state+='☑ '
        else: state+='☐ '

        row = [ i, data[2], state+data[0], data[1] ]
        id=self.tree.insert(parent, pos, value=row, open=True)#, text=data[0])
        self.top+=1
        return id


    def push(self):
        print("push called")
        row = [  str(self.top), 0, False ]
        self.insert(self.top, row)


    def pop(self):
        print("pop called")


    def selInv(self):
        print("selInv called")


    def selAll(self):
        print("selAll called")


    def refresh(self):
        print("refresh called")


    def article_properties(self):
        win=Toplevel()
        win.title("Properties")
        win.bind('<Key-Escape>', lambda event: win.destroy())
        Label(win, text="hello").pack()


    def clear_tree(self):
        x = self.tree.get_children()
        for item in x: self.tree.delete(item)
        self.top=0


def autoscroll(sbar, first, last):
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)


if __name__ == '__main__':
    root = Tk()

    tl=TreeList(root)
    tl.pack(fill=BOTH, expand=YES)
    #tl.grid(column=0, row=0)

    root.bind('<Key-Escape>', lambda e: exit())
    root.mainloop()
