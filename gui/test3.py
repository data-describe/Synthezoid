import tkinter as tk
from tkinter import ttk

master = tk.Tk()
my_frame = tk.Frame()
my_frame.grid(row=0, column=1)
# create one set of widgets in a frame
for num in range(1, 6):
    tk.Label(master=my_frame).grid(row=0,column=num)
    tk.Entry(master=my_frame).grid(row=1, column=num)
def detect_selection(eventobject):
    the_selection = eventobject.widget.get()
    # hide all widgets
    for item in my_frame.winfo_children():
        item.grid_remove()
    show_idx__wigets = 6
    if the_selection == '3':
        change_labeltext(('a', 'b', 'c'), 6)
    if the_selection == '4':
        show_idx__wigets = 8
        change_labeltext(('d', 'e', 'f', 'g'), 8)
    if the_selection == '5':
        show_idx__wigets = 10
        change_labeltext(('h', 'i', 'j', 'k', 'l'), 10)
    # reveal only desired number of widgets
    show_widgets(show_idx__wigets)

def show_widgets(upto_widgetposition):
    for item in my_frame.winfo_children()[:upto_widgetposition]:
        item.grid()
def change_labeltext(labeltext, upto_widgetposition):
    for txt, item in zip(
        labeltext, my_frame.winfo_children()[:upto_widgetposition:2]):
        item['text'] = txt
combo = ttk.Combobox(master,
                     values=(3,4,5))
combo.grid(row=0, column=0, sticky='s')
combo.bind('<<ComboboxSelected>>', detect_selection)

master.mainloop()