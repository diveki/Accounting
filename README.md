# Accounting
A python code that helps my personal accounting

This is a folder that aims to help the owner to retrieve data from a source (either excel sheet from hard drive or google sheet from given destination on google drive). It will tell the user who were paying rent and bills in a given year and month.

USAGE:

Open konyveles.py . Run the code and it will print out the bill for the tenants (they are located in an excel sheet in the same folder).

filepath - defines where the excel sheet is located on the hard drive 
sheetName - defines which sheet to use in the excel file
yearDate, monthDate - has to be given to retrieve the payed rent and bills for a given year and month
onlinePath - the googledrive link

DEFINED CLASSES

There are 4 classes defined in this code. 

Ingatlan - its a class to retrive the address and tenants of the property
Berlo - its a class to define a tenants name and retrive his bill and print it
Szamla - this is the bill that contains the payed rent and utility bills for the given year and month
SheetLoader - this class is responsible for loading the sheets either from hard drive or google drive
