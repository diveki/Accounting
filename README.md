# Accounting
A python code that helps my personal accounting

This is a folder that aims to help the owner to retrieve data from a source (either excel sheet from hard drive or google sheet from given destination on google drive). It will tell the user who were paying rent and bills in a given year and month.

############
## USAGE:
############

###################
COMMAND LINE USAGE:
###################

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

#####################
GUI USAGE:
#####################

Run konyvelesgui.py to start the GUI interface of the accounting program. You can adjust the input values like the Year, Month, Code name of the appartement and whether you want to retrieve the data from online (google sheet) or hard disk. After setting these parameters up, you can choose the name of the tenant and press Run to get the corresponding bill description.

PRE-SETUP:
In konyvelesgui.py preset:
onlinePath - for the corresponding googlesheet addresses
localPath  - path to the excel sheets on your hard drive, including the excel sheet name too
startYear  - which year should be the defualt to appear when you start the gui
startSource- whether online or offline mode should be the default when you start the gui
welcomeText- the text that is displayed in the text widget when you start the gui

DEFINED CLASSES:
There are two objects defined in the konyvelesgui.py:
customRadio - it is a custom made radio button widget that inherits the main features from gui.myRadioButton. The object initializes what should the radio button text be and what function should it call when pressed. It simple calls a function that returns the value of the radio button. 

Demo         - this is the main gui object that is collecting all kinds of widgets and makes sure that when parameters are set up, the right functions are called. 

############
## HELPER OBJECTS:
############

#######################
MENUMAKER.PY
#######################

This file is creating basic GUI widgets that can be reused in other applications. The following objects are defined:

MenuClass	-	this is a generalized Menu bar object. It creates a File item with some content in it. The only content that has a meaningful definition is the Close function. When clicking on it, it closes the parent gui object. 
It has methods to add new Menu items with new content (that is how the Edit item is created in the konyvelesgui.py file). 

Quitter		-	a button that is quitting the parent GUI object when clicked. 

ScrolledText	-	a general GUI object that combines a scrollbar with a Text object. 

DropdownMenu	-	a simple OptionMenu widget that is pre defining its textvariable and a command action if needed

LabeledDropdown	-	a text label widget combined with a DropdownMenu object

DoubleLabel	-	two text labels next to each other, one serves as a description of the content of the other label (which has a white background) and the second label's content can be adjusted

myRadioButton	-	a radiobutton widget that can have several options and corresponding command actions

Demo 		-	test object where the previously defined objects are collected and tested.

#######################
onlineSheetsData.PY
#######################

This file is a modified version of what google suggest to use as an interaction with google sheets. It has two functions:

get_credentials()	-	deals with authentication
getOnlineData()		-	a function that takes the address of the google sheet and the sheetName we want to use. It is set to retrieve the D to H columns.





