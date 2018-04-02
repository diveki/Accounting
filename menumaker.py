#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 18:18:51 2018

@author: diveki
"""

from tkinter import *
from tkinter import messagebox as msg

def notdone():
    print('action not implemented')


class MenuClass(Frame):
    menubarItems = {}
    def __init__(self, parent = None):
        Frame.__init__(self, parent, relief = RAISED, bd = 2, width=1000, height=500)
        self.pack(expand=YES, fill=BOTH)
        self.button = {}
        self.buttonList = {}
        self.menuItems = self.initialize()
        self.initializeMenuBar()     

    def initializeMenuBar(self):
        self.menubarFrame = Frame(self, relief = RAISED, bd=2)
        self.menubarFrame.pack(side=TOP, fill=X)
        self.createMenu()
     #   self.updateMenu(self.button['File'], self.buttonList['File'], menuitem=[['Save as...', notdone, 0]])
        self.createMenuButton(self.menubarFrame, 'Edit', 0)
        self.createMenuButton(self.menubarFrame, 'Tools', 0)
         
    def createMenu(self) :
        for key in self.menuItems:
            self.button[key] = Menubutton(self.menubarFrame, text = key,  underline=0)
            self.button[key].pack(side=LEFT)
            self.buttonList[key] = Menu(self.button[key])
            self.updateMenu(self.button[key], self.buttonList[key], self.menuItems[key])

    def fillMenu(self, bb, name, func, under):
        bb.add_command(label=name, command = func, underline = under)
        
    def updateMenu(self, button, buttonlist, menuitem):
        for (name, func, under) in menuitem:
            self.fillMenu(buttonlist, name, func, under)
            button.config(menu=buttonlist)
    
    def createMenuButton(self, parent, name, under):
        self.button[name] = Menubutton(parent, text = name, underline = under)
        self.button[name].pack(side=LEFT)
        self.buttonList[name]=Menu(self.button[name])
    
    def initialize(self):
        menuItems = {'File': [['New file...', notdone, 0],
                              ['Open...', notdone, 0],
                              ['Save as...', notdone, 0], 
                              ['Close', self.master.destroy, 0]
                              ]
                   #  'Edit': [['Copy', notdone, 0],
                   #           ['Cut', notdone, 0],
                   #           ['Paste', notdone, 0]
                   #           ]
                    }
        return menuItems  
        
class Quitter(Frame):
    def __init__(self, parent = None):
        self.parent = parent
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text = 'Quit', command = self.quitter)
        widget.pack(side=LEFT, expand=YES)
        
        
    def quitter(self):
        ans = msg.askokcancel('Verify quit', 'Do you really want to exit?')
        if ans:
            return self.master.destroy()

class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.makewidgets()
        self.settext(text=text)
    
    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text = text
    
    def settext(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, END)#'1.0')
        self.text.focus()

class DropdownMenu(Frame):
    def __init__(self, parent=None, opt=[], textVar = StringVar, setnull = '', command=None):
        self.setnull = setnull
        self.command = command
        Frame.__init__(self, parent)
        self.variable = textVar
        if opt:
            self._myoptions = opt
        else:
            self.startDropdown()
        self.makewidgets()
    
    def makewidgets(self):
        self.option = OptionMenu(self, self.variable, *self._myoptions, command = self.command)
        self.option.pack()
    
    def startDropdown(self):
        self._myoptions = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    

class LabeledDropdown(DropdownMenu):
    def __init__(self, parent=None, text = '', textVar = StringVar, opt=[], setnull='', command=None):
        Frame.__init__(self, parent)
        self.command = command
        w = Label(self, text = text)
        w.pack(side=LEFT)
        self.dm = DropdownMenu(parent=self, opt=opt, textVar = textVar, setnull=setnull, command=self.command)
        self.dm.pack(side=LEFT)
        #self.dmvalue = self.dm.getOM()

class DoubleLabel(Frame):
    def __init__(self, parent=None, keyText='', textVar = StringVar):#, valueText=''):
        Frame.__init__(self, parent)
        self.dbltext = textVar
        #self.dbltext.set(valueText)
        ll = Label(self, text = keyText)
        ll.pack(side=LEFT)
        self.ll1 = Label(self, textvariable = self.dbltext, bg='white')
        self.ll1.pack(side=LEFT)
        #self.dbltext.trace('w', )
    def setDblabel(self, value):
        self.dbltext.set(value)
        
class myRadioButton(Frame):
    def __init__(self, parent=None, var=StringVar):
        Frame.__init__(self, master=parent)
        self.modes = self.initModes()
        self.var = var
        self.makeWidgets(parent)
    
    def initModes(self):
        container = [('One', '1', self.demoFunc),
                     ('Two', '2', self.demoFunc),
                     ('Three', '3', self.demoFunc)]
        return container
    
    def makeWidgets(self, parent):
        for text, mode, com in self.modes:
            self.rb = Radiobutton(parent, text = text, variable=self.var, value=mode, indicatoron=0, command = com)
            self.rb.pack()
    
    def demoFunc(self):
        pick = self.var.get()
        print('you pressed: ', pick) 
    
class Demo(Frame):
    _ldyear = ['2016', '2017', '2018']
    _ldmonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    def __init__(self, parent = None):
        MenuClass(parent = parent).pack()
        frame1 = Frame(parent)
        LabeledDropdown(parent=frame1, text='Year', opt=Demo._ldyear, setnull='2018').pack(side=LEFT, anchor='w')
        LabeledDropdown(parent=frame1, text='Month', opt=Demo._ldmonths, setnull='March').pack(side=LEFT, anchor='w')
        LabeledDropdown(parent=frame1, text='Property', opt=['Bartok', 'Tabor', 'Garazs', 'Csillagter'], setnull='Bartok').pack(side=LEFT, anchor='w')
        frame1.pack(side=TOP, fill=BOTH)

        frame2 = Frame(parent)
        DoubleLabel(parent=frame2, keyText='Address', valueText='Bartok').pack(side=TOP, anchor='e')
        DoubleLabel(parent=frame2, keyText='Tenant', valueText='Valaki').pack(side=TOP, anchor='e')
        frame2.pack(side=TOP, fill=BOTH, pady=1)
        
        ScrolledText(parent = parent, text = 'Hello world').pack(side=TOP)
        Quitter(parent).pack(side=BOTTOM, anchor='e')

if __name__ == '__main__':
    root = Tk()
    #MenuClass(parent = root)
    #Quitter(root).pack(side=RIGHT)
    Demo(root)
    root.mainloop()
 
    