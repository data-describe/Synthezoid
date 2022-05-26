#!/usr/bin/python
#######################################################################################
#######################################################################################
#
#	Name: sdg_gui.py
#	Usage: python sdg_gui.py
#	Description: Creates GUI for SDG
#
#
#
#
#	Modification Log:
#	2019-08-14			Annie Castner				Initial creation
#
#######################################################################################


import tkinter as tk
from tkinter import ttk
import json
from sdg import main as sdg


class dictionary(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.fields = []
        self.final_data = []
        self.create_widgets()
        self.grid(column=0, sticky="NEWS")

    def create_widgets(self):
        self.add_field()
        self.add_data_field = ttk.Button(self, text="add field", command=self.add_field)
        self.add_data_field.bind("<Return>", self.add_field)
        self.add_data_field.grid(row=len(self.fields), column=0, padx=4, pady=6, sticky="W")
        self.add_save_button = ttk.Button(self, text='Submit', command=self.save_schema)
        self.add_save_button.bind("<Return>", self.save_schema)
        self.add_save_button.grid(row=len(self.fields), column=6, padx=4, pady=6, sticky="W")

    def save_schema(self):
        for i in self.fields:
            data = {
                "name": i['field'].get(),
                "type": i['dropdown'].get()
            }
            for j in i['parameters']:
                data[j] = i[j+'_val'].get()
            self.final_data.append(data.copy())
        self.final_final = {
            "fields": self.final_data
        }

        with open('../data/input_data/schema.json', 'w') as f:
            json.dump(self.final_final, f, indent=4)

    def detect_selection(self, event):
        the_selection = event.widget.get()
        n = len(self.fields) - 1
        # TODO cat labels overlap fix
        # TODO better way for if then?
        # for item in self.winfo_children():
        #     item.grid_remove()
        if the_selection == 'name':
            self.fields[n]['parameters'] = ['name type']
        if the_selection == 'date':
            self.fields[n]['parameters'] = ['start date', 'end date', 'date type']
        if the_selection == 'categorical':
            self.fields[n]['parameters'] = ['categories', 'distribution']
        if the_selection == 'integer':
            self.fields[n]['parameters'] = ['max', 'min', 'distribution']
        self.show_widgets(self.fields[n]['parameters'], len(self.fields[n]['parameters']))

    def show_widgets(self, labeltext, upto_widgetposition):
        n = len(self.fields) - 1
        for txt, item in zip(
                labeltext, range(upto_widgetposition)):
            self.fields[n][txt+'_val'] = tk.StringVar(self)
            self.fields[n][txt+'_lab'] = tk.Label(self, text=txt).grid(row=len(self.fields) - 1, column=8+4*item, columnspan=1, sticky="W")
            self.fields[n][txt] = tk.Entry(self, textvariable=self.fields[n][txt+'_val']).grid(row=len(self.fields) - 1, column=10 + 4*item, columnspan=1, sticky="W")


    def add_field(self):
        self.fields.append({})
        n = len(self.fields)-1
        self.fields[n]['field_name'] = tk.StringVar(self)
        self.fields[n]['label'] = tk.Label(self, text="Field Name").grid(row=n)
        self.fields[n]['field'] = ttk.Entry(self, textvariable=self.fields[n]['field_name'])
        self.fields[n]['field'].grid(row=n, column=3, columnspan=1, padx=2, pady=6, sticky="NEWS")
        self.fields[n]['data_type'] = tk.StringVar(self)
        self.fields[n]['choices'] = ('name', 'date', 'categorical', 'integer')
        self.fields[n]['dropdown'] = ttk.Combobox(self, values=self.fields[n]['choices'])
        self.fields[n]['data_label'] = tk.Label(self, text="Data Type").grid(row=n, column=5)
        self.fields[n]['dropdown'].grid(row=n, column=6, columnspan=1, padx=4, pady=6, sticky="NEWS")
        self.fields[n]['dropdown'].bind('<<ComboboxSelected>>', self.detect_selection)

        if n:
            self.add_data_field.grid(row=n + 1, column=0, padx=2, pady=6, sticky="W")
            self.add_save_button.grid(row=n + 1, column=6, padx=2, pady=6, sticky="W")


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Synthetic Data Generator")
    app = dictionary(master=root)
    app.mainloop()
    #sdg()
