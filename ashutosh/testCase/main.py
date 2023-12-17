# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import subprocess
from ui_components import DragDropListbox, load_data, execute_script_and_display_result, show_confirmation_screen, on_double_left_click, on_submit, harden_now

# Read data from data.json
data = load_data('data.json')

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

# Populate available options listbox with names from data.json
for id, details in data.items():
    available_option_listbox.insert(tk.END, f"{details['name']}")

available_option_listbox.pack(side=tk.LEFT)
selected_option_listbox.pack(side=tk.RIGHT)

# Bind the double click event to the DragDropListbox instances
available_option_listbox.bind('<Double-Button-1>', lambda event: on_double_left_click(event, available_option_listbox, selected_option_listbox))
selected_option_listbox.bind('<Double-Button-1>', lambda event: on_double_left_click(event, selected_option_listbox, available_option_listbox))

# Submit button
submit_button = ttk.Button(root, text="Submit", command=lambda: on_submit(root, data, selected_option_listbox))
submit_button.pack(pady=10)

root.mainloop()
