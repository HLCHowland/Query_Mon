from tkinter import *
from tkinter.filedialog import askopenfilename
import csv
import requests, os, pickle, sys, datetime, time, random, select, re
from bs4 import BeautifulSoup

#   Open's up the file and prints out what's in it.
with open("queries.pickle", "rb") as fp:
    queries = pickle.load(fp)


#   Button for the selection of the query
def addItem():
    add = e1.get()
    list.insert('end', add)
    e1.delete(0, 'end')

def removeItem():
    dele = e2.get()
    for i in dele[::-1]:
        list.delete(i)
    e2.delete(0, 'end')

root = Tk()
root.title("Queries")
root.geometry('480x450')

#   Add Query
label = Label(root, text='Add Query', font=('Helvetica', 14, 'bold'))
label.grid(row=2, column=8)
e1 = Entry(root)
e1.grid(row=3, column=8)

button = Button(root, text='Add', command=addItem)
button.grid(row=4, column=8)

#   Delete Query
label = Label(root, text='Delete Query', font=('Helvetica', 14, 'bold'))
label.grid(row=6, column=8)
e2 = Entry(root)
e2.grid(row=7, column=8)

button = Button(root, text='Delete', command=removeItem)
button.grid(row=8, column=8)

#   Listbox
label1 = Label(root, text='Available Queries', font=('Helvetica', 18, 'bold'))
label1.grid(row=0, column=0, padx=10, pady=20)

list = Listbox(root, height=18, width=15, border=0)
list.grid(row=2, column=0, columnspan=3, rowspan=10, pady=1, padx=5)
for q in queries:
    list.insert(END, q)

#   ScrollBar
scrollbar = Scrollbar(root)
scrollbar.grid(row=2, column=3, padx=40)


#   Moving the scrollbar (NOT WORKING!)
# list.config(yscrollcommand=scrollbar.set)
# scrollbar.config(command=list.yview)

root.mainloop()