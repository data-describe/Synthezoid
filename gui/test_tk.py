from tkinter import *
import json


def show_entry_fields():
    data = {
        "first_name": e1.get(),
        "last_name": e2.get()
    }
    #print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))
    with open('name.json', 'w') as f:
        json.dump(data, f, indent=4)
    e1.delete(0,END)
    e2.delete(0,END)


master = Tk()
Label(master, text="First Name").grid(row=0)
Label(master, text="Last Name").grid(row=1)

e1 = Entry(master)
e2 = Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

Button(master, text='Show', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)

mainloop( )