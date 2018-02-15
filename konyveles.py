#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 15:01:15 2018

@author: diveki
"""

import os
import pandas as pd

path = '.'
filename = 'Bevetel 2017.xlsx'
filepath = os.path.join(path, filename)
sheetName = 'HelloStreet'
yearDate = '2017'
monthDate = 'January'
onlinePath=''

subsetDate = yearDate + '-' + monthDate


class Ingatlan:
    _addresses = {
                'Bartok': 'HelloStreet',
                }
    def __init__(self, pid):
        self.pid = pid
        self.address = self.setAddress(pid)
    def setAddress(self, pid):
        return Ingatlan._addresses.get(pid)
    def getTenants(self, sh):
        self.tenants = list(sh['Befizeto neve'].unique())
    

class Berlo:
    def __init__(self, address, berlo):
        self.address = address
        self.berlo = berlo
    def __str__(self):
        return self.berlo
    def getSzamla(self, tenants, data):
        self.szamla = Szamla(tenants, self.address, data)
        self.szamla.createSzamla()
    def printSzamla(self):
        self.szamla.printSzamla([self.berlo])
        

class Szamla:
    def __init__(self, berlok, address, data):
        self.szamla = pd.DataFrame()
        self.tenant = berlok
        self.address = address
        self.data = data
    def getBills(self, colname = 'Bevetel leirasa', tenancyfee = 'Berleti dij'):
        tmp = self.data.loc[self.data[colname] != tenancyfee]
        return tmp.groupby(colname)[["Osszeg (Ft)"]].sum()
    def getNumberOfTenants(self):
        return len(self.tenant)
    def getPayDate(self, person):
        dt = self.szamla[self.szamla['Befizeto neve'] == person]['Datum'].unique()
        dt = pd.to_datetime(dt)
        dt = dt.strftime('%Y-%B-%d')[0]
        return dt
    def getTenancyFee(self, colname = 'Bevetel leirasa', tenancyfee = 'Berleti dij'):
        tfee = self.data.loc[self.data[colname] == tenancyfee]
        tfee.reset_index(level=0, inplace=True)
        return tfee
    def getTenantSzamla(self, person):
        return self.szamla[self.szamla['Befizeto neve'] == person]
    def createSzamla(self, col = 'Bevetel leirasa', tf = 'Berleti dij', nameCol = 'Befizeto neve'):
        rezsi = self.getBills(colname = col, tenancyfee = tf)
        for person in self.tenant:
            tmp = round(rezsi / self.getNumberOfTenants())
            if person == self.tenant[-1] and self.getNumberOfTenants() > 1:
                tmp = rezsi - self.szamla.groupby(col).sum()
            tmp[nameCol] = person
            self.szamla = pd.concat([self.szamla, tmp])        
        self.szamla.reset_index(level=0, inplace=True)
        berlet = self.getTenancyFee(colname=col, tenancyfee = tf)
        berlet.reset_index(level=0, inplace=True)
        self.szamla = pd.merge(berlet[['Datum', 'Ingatlan', nameCol]], self.szamla)
        self.szamla = pd.concat([self.szamla, berlet])
    def printSzamla(self, name):
        for person in name:
            print(person)
            bill = self.getTenantSzamla(person)
            text = "\n\nSzamla %s reszere\n" % person
            text = text + "-" * 40 + '\n'
            text = text + 'Ingatlan cime: %s\n' % self.address
            text = text + 'Fizetes teljesitese: %s\n' % self.getPayDate(person)
            text = text + "-" * 40 + '\n\n'
            for item in bill['Bevetel leirasa'].values:
                val = bill[bill['Bevetel leirasa'] == item]['Osszeg (Ft)'].values
                text = '%s ** %-15s \t\t %15s' % (text, item, str(val[0]) + ' Ft\n')
            text = text + "-" * 40 + '\n'
            text = text + '%-15s \t\t %15s Ft\n\n' % ('TOTAL:', bill['Osszeg (Ft)'].sum())
                #text = text + '** ' + item + '\t\t' + str(val[0]) + ' Ft\n' 
            
            print(text)
            

class SheetLoader():
    """
    This class is loading the data sheet.
    id = Bartok, Tabor, Rakoczi, Csillagter
    """
    def __init__(self, ingatlan, year = 2017, month = 'March', source = 'offline', sourcePath = '', columns = ['Ingatlan', 'Bevetel leirasa', 'Befizeto neve', 'Osszeg (Ft)']):
        self.date = str(year) + '-' + month        
        self.data = self.loadData(ingatlan, source, sourcePath)
        self.subset = self.subSetData(columns)
    def loadData(self, ing, src, srcPath):
        if src != 'offline':
            import onlineSheetsData
            data1 = onlineSheetsData.getOnlineData(spreadID=srcPath, sheetID=ing.address)            
            data1.set_index('Datum', inplace=True)
            data1.index = pd.to_datetime(data1.index, dayfirst=True)
            data1['Osszeg (Ft)'] = data1['Osszeg (Ft)'].apply(float)
        else:
            try:
                shname = ing.address.replace('/','')
                data1 = pd.read_excel(srcPath, sheet_name=shname, index_col=None, usecols='D:H')
                data1.set_index('Datum', inplace=True)
                data1['Osszeg (Ft)'] = data1['Osszeg (Ft)'].apply(float)
            except:
                print('Bad filepath')
        return data1
    def subSetData(self, cols):
        print('hello')
        return self.data[self.date][cols]
        
        
if __name__ == '__main__':
    ing = Ingatlan('Bartok')
    datash = SheetLoader(ing, source = 'offline', sourcePath = onlinePath, year=yearDate, month=monthDate)
#    datash = SheetLoader(ing, source = 'offline', sourcePath = filepath, year=yearDate, month=monthDate)
    ing.getTenants(datash.subset)
    berlok = [Berlo(ing.address, name) for name in ing.tenants]
    for person in berlok:
        person.getSzamla(ing.tenants, datash.subset)
        person.printSzamla()
#    sz.createSzamla()
#    sz.printSzamla()    
                    