import tkinter as tk
from tkinter import ttk
import json
import subprocess


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
    selected_items = selected_option_listbox.get(0, tk.END)

    for selected_name in selected_items:
        selected_name = selected_name  # Assuming you are showing only the name on the UI
        selected_id = None
        selected_exec_file = None

        for id, details in data.items():
            if details['name'] == selected_name:
                selected_id = id
                selected_exec_file = details.get('execFile', 'Exec file not found')
                break

        print(f"Selected ID for {selected_name}: {selected_id}")
        print(f"Exec File for {selected_name}: {selected_exec_file}")

        # Execute the selected_exec_file using subprocess
        execute_script(selected_exec_file)

def execute_script(exec_file):
    # Create a new window to display the output
    output_window = tk.Toplevel(root)
    output_window.title("Script Execution Result")

    output_text = tk.Text(output_window, wrap=tk.WORD, width=50, height=10)
    output_text.pack(padx=10, pady=10)

    # Execute the selected_exec_file using subprocess.run
    process = subprocess.run(['bash', exec_file], text=True, stdout=subprocess.PIPE)

    # Update the output_text widget with the process output
    output_text.insert(tk.END, process.stdout)

    # Update the window
    output_window.update_idletasks()


# Read data from data.json
with open('data.json') as f:    
    data = json.load(f)

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

# Submit button
submit_button = ttk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

root.mainloop()
