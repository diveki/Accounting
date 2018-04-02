#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 21:18:07 2018

@author: diveki
"""

import konyveles as konyv
import menumaker as gui
from tkinter import *

# definitions
onlinePath={'2018':'1kivk-7e3c5Z_eCikSpwKwt8jloDATuFj3DwsD_KSTXo',
            '2017':'1sgOmKyfbrZUvBuwI1STE47XCksK7h4PQ5Hmibe-0-ps',
            '2016':'1m1MyT_x2dui3RPc8EZEBFMkCQwHXEty4N3VRKOKsmMs'
        }
localPath={'2017':'Bevetel 2017.xlsx',
           '2016':'Bevetel2016.xlsx'
       }

startYear = '2017'
startSource = 'offline'
welcomeText = 'Set the inputs and press Run'
_addressPid = list(konyv.Ingatlan._addresses.keys())

class customRadio(gui.myRadioButton):
    def initModes(self):
        container = [('Online', 'online', self.returnValue),
                     ('Offline', 'offline', self.returnValue)]
        return container
    
    def returnValue(self):
        return(self.var.get())
    


class Demo(Frame):
    _ldyear = ['2016', '2017', '2018']
    _ldmonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    def __init__(self, parent = None, src='online', year=''):
        self.initYear = year
        self.source = src
        if src == 'online':
            self.sourcePath = onlinePath[year]
        if src == 'offline':
            self.sourcePath = localPath[year]
        self.initStringVars(parent)
        self.initKonyvClasses()
        
        self.propAddressVar.set(self.getPropertyAddress())
        self.tenantVar.set(self.ingatlan.tenants[0])
        self.makeDemowidgets(parent)
        
    def initStringVars(self, parent):
        self.propVar = StringVar(parent)
        self.yearVar = StringVar(parent)
        self.monthVar = StringVar(parent)
        self.radioVar = StringVar(parent)
        self.propAddressVar = StringVar(parent)
        self.tenantVar = StringVar(parent)
        
        self.propVar.set(_addressPid[0])
        self.yearVar.set(self.initYear)
        self.monthVar.set(Demo._ldmonths[0])
        self.radioVar.set(self.source)
        
    def initKonyvClasses(self):
        self.ingatlan = konyv.Ingatlan(self.propVar.get())
        self.datash = konyv.SheetLoader(self.ingatlan, source = self.source, sourcePath = self.sourcePath, year=self.yearVar.get(), month=self.monthVar.get())
        self.ingatlan.getTenants(self.datash.subset)
        
    def getPropertyAddress(self):
        return self.ingatlan.address
        
    def makeDemowidgets(self, parent):
        self.menuBar = gui.MenuClass(parent = parent)
        self.menuBar.pack()
        self.initMenuBar()
        self.frame1 = Frame(parent)
        self.yeardrop = gui.LabeledDropdown(parent=self.frame1, text='Year', textVar = self.yearVar, opt=Demo._ldyear, command=self.updateWidgets)
        self.yeardrop.pack(side=LEFT, anchor='w')
        self.monthdrop = gui.LabeledDropdown(parent=self.frame1, text='Month', textVar = self.monthVar, opt=Demo._ldmonths, command=self.updateWidgets)
        self.monthdrop.pack(side=LEFT, anchor='w')
        self.propdrop = gui.LabeledDropdown(parent=self.frame1, text='Property', opt=_addressPid, textVar=self.propVar, command=self.setPropAddressVar)
        self.propdrop.pack(side=LEFT, anchor='w')
        self.rb = customRadio(parent=self.frame1, var=self.radioVar)
        self.rb.pack(side=BOTTOM)
        self.frame1.pack(side=TOP, fill=BOTH)

        self.frame2 = Frame(parent)
        self.addressdl = gui.DoubleLabel(parent=self.frame2, textVar = self.propAddressVar, keyText='Address')#, valueText=self.getPropertyAddress())
        self.addressdl.pack(side=TOP, anchor='e')
        self.tenantdrop = gui.LabeledDropdown(parent=self.frame2, text='Tenants', opt=self.ingatlan.tenants, textVar=self.tenantVar, command=None)
        self.tenantdrop.pack(side=TOP, anchor='e')
        self.runButton = Button(self.frame2, text='Run', command = self.runCommand)
        self.runButton.pack(side=TOP, anchor='e')
        self.frame2.pack(side=TOP, fill=BOTH, pady=1)
        
        self.stext = gui.ScrolledText(parent = parent, text = welcomeText)
        self.stext.pack(side=TOP)
        gui.Quitter(parent).pack(side=BOTTOM, anchor='e')
        
    def setPropAddressVar(self, *args):
        self.initKonyvClasses()
        self.propAddressVar.set(self.getPropertyAddress())
        self.updateTenantList()
    
    def updateTenantList(self):
        new_choices = self.ingatlan.tenants
        self.tenantdrop.dm.option['menu'].delete(0, 'end')
        for choice in new_choices:
            self.tenantdrop.dm.option['menu'].add_command(label=choice, command=lambda value=choice: self.tenantVar.set(value))
        self.tenantVar.set(new_choices[0])

    def runCommand(self):
        self.source = self.radioVar.get()
        self.setSourcePath()
        self.initKonyvClasses()
        self.person = konyv.Berlo(self.ingatlan.address, self.tenantVar.get())
        self.person.getSzamla(self.ingatlan.tenants, self.datash.subset)
        self.person.printSzamla()
        
        self.stext.text.delete('1.0', END)
        self.stext.text.insert('1.0', self.person.szamla.text)
        self.stext.text.mark_set(INSERT, END)#'1.0')
        self.stext.text.focus()
    
    def setSourcePath(self, *args):
        if self.rb.var.get() == 'online':
            self.sourcePath = onlinePath[self.yearVar.get()]
        elif self.rb.var.get() == 'offline':
            self.sourcePath = localPath[self.yearVar.get()]
    
    def updateWidgets(self, *args):
        self.source = self.rb.var.get()
        self.setSourcePath()
        try:
            self.setPropAddressVar()
        except:
            messagebox.showerror('', 'An input is invalid!') 
        else:
            self.updateTenantList()
    
    def initMenuBar(self):
        edit_items=[('Edit', 'Copy', self.onCopy, 0), ('Edit', 'Cut', self.onCut, 2), ('Edit', 'Paste', self.onPaste, 0), ('Edit', 'Select all', self.onSelectAll, 0)]
        for bar, item, func, under in edit_items:
            self.menuBar.updateMenu(self.menuBar.button[bar], self.menuBar.buttonList[bar], menuitem=[[item, func, under]])
        
    def onPaste(self):
        try:
            text = self.stext.selection_get(selection='CLIPBOARD')
        except:
            messagebox.showerror('', 'Nothing to paste')
            return
        self.stext.text.insert(INSERT, text)
        self.stext.text.tag_remove(SEL, '1.0', END)
        self.stext.text.tag_add(SEL, INSERT+'-%dc' % len(text), INSERT)
        self.stext.text.see(INSERT)
    
    def onCopy(self):
        if not self.stext.text.tag_ranges(SEL):
            messagebox.showerror('', 'Nothing selected')
        else:
            text = self.stext.text.get(SEL+'.first', SEL+'.last')
            self.stext.clipboard_clear()
            self.stext.clipboard_append(text)
    
    def onCut(self):
        if not self.stext.text.tag_ranges(SEL):
            messagebox.showerror('', 'Nothing selected')
        else:
            self.onCopy()
            self.onDelete()
    
    def onSelectAll(self):
        self.stext.text.tag_add(SEL, '1.0', END+'-1c')
        self.stext.text.mark_set(INSERT, '1.0')
        self.stext.text.see(INSERT)
    
    def onDelete(self):
        if not self.stext.text.tag_ranges(SEL):
            messagebox.showerror('', 'Nothing selected')
        else:
            self.stext.text.delete(SEL+'.first', SEL+'.last')
        

if __name__ == '__main__':
    root = Tk()
    #MenuClass(parent = root)
    #Quitter(root).pack(side=RIGHT)
    a=Demo(root, src=startSource, year = startYear)
    root.mainloop()
 


