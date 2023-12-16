import tkinter as tk
from tkinter import ttk
import json

class DragDropListbox(tk.Listbox):
    def __init__(self, master, other_listbox, list_name, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.other_listbox = other_listbox
        self.list_name = list_name
        self.bind('<Double-Button-1>', self.on_double_left_click)

    def on_double_left_click(self, event):
        cur_index = self.nearest(event.y)
        cur_item = self.get(cur_index)
        self.delete(cur_index)
        self.other_listbox.insert(tk.END, cur_item)

def on_submit():
    print(selected_option_listbox.get(0, tk.END))

# Read data from data.json
with open('data.json') as f:
    data = json.load(f)

# Extract keys from the data dictionary
available_options = list(data.keys())

root = tk.Tk()
root.geometry("600x400")

main_frame = ttk.Frame(root)
main_frame.pack(pady=10)

left_frame = ttk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, padx=10)

right_frame = ttk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, padx=10)

# Create DragDropListbox instances in the correct order
available_option_listbox = DragDropListbox(left_frame, None, "available_options")
selected_option_listbox = DragDropListbox(right_frame, available_option_listbox, "selected_options")
available_option_listbox.other_listbox = selected_option_listbox

# Populate available options listbox with keys from data.json
for option in available_options:
    available_option_listbox.insert(tk.END, option)

available_option_listbox.pack(side=tk.LEFT)
selected_option_listbox.pack(side=tk.RIGHT)

# Submit button
submit_button = ttk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

root.mainloop()
