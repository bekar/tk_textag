#!/usr/bin/python

tag_list=[]

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

    #[ label, count, state, parent, object, show, dump ]
    tl.append([ "filesys", 0, 1, None, None, True, False ])
    tl.append([ "executable", 0, 1, "filesys", exe, True, False ])
    tl.append([ "infile", 0, 1, "filesys", infile, True, False ])
    tl.append([ "folder", 0, 1, "filesys", folder, True, False ])
    tl.append([ "title", 0, 1, None, title, True, False ])
    tl.append([ "code", 0, 1, None, code, True, False ])
