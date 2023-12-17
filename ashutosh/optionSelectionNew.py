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
        self.bind('<Double-Button-1>', lambda event: self.on_double_left_click(event))

    def on_double_left_click(self, event):
        cur_index = self.nearest(event.y)   
        cur_item = self.get(cur_index)
        self.delete(cur_index)
        self.other_listbox.insert(tk.END, cur_item)


def load_data(file_path):
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}


def find_selected_details(selected_name, data):
    for id, details in data.items():
        if details['name'] == selected_name:
            return id, details.get('execFile', 'Exec file not found')
    return None, None


def execute_script_and_display_result(exec_file):
    output_window = tk.Toplevel(root)
    output_window.title("Script Execution Result")
    output_window.geometry("600x400")
    output_window.transient(root)  # Set the parent window

    output_text = tk.Text(output_window, wrap=tk.WORD, width=50, height=10)
    output_text.pack(padx=10, pady=10)

    try:
        process = subprocess.run(['bash', exec_file], text=True, stdout=subprocess.PIPE, check=True)
        output_text.insert(tk.END, process.stdout)
    except subprocess.CalledProcessError as e:
        output_text.insert(tk.END, f"Error executing script:\n{e}")

    output_window.grab_set()  # Make the output window modal
    output_window.update_idletasks()


def show_confirmation_screen(selected_items):
    confirmation_window = tk.Toplevel(root)
    confirmation_window.title("Confirmation")
    confirmation_window.geometry("400x200")
    confirmation_window.transient(root)  # Set the parent window

    confirmation_label = tk.Label(confirmation_window, text=f"Confirm action for {', '.join(selected_items)}")
    confirmation_label.pack(pady=10)

    download_button = ttk.Button(confirmation_window, text="Download Yaml", command=lambda: download_yaml(selected_items))
    download_button.pack(pady=5)

    harden_button = ttk.Button(confirmation_window, text="Harden NOW!", command=lambda: harden_now(selected_items))
    harden_button.pack(pady=5)

    cancel_button = ttk.Button(confirmation_window, text="Cancel", command=confirmation_window.destroy)
    cancel_button.pack(pady=10)

    confirmation_window.grab_set()  # Make the confirmation window modal
    confirmation_window.update_idletasks()


def download_yaml(selected_items):
    for selected_item in selected_items:
        print(f"Downloading YAML for {selected_item}")


def harden_now(selected_items):
    for selected_item in selected_items:
        print(f"Hardening NOW for {selected_item}")
        selected_id, selected_exec_file = find_selected_details(selected_item, data)
        execute_script_and_display_result(selected_exec_file)


def on_double_left_click(event, source_listbox, destination_listbox):
    cur_index = source_listbox.nearest(event.y)
    cur_item = source_listbox.get(cur_index)
    source_listbox.delete(cur_index)
    destination_listbox.insert(tk.END, cur_item)


def on_submit(data, selected_option_listbox):
    selected_items = selected_option_listbox.get(0, tk.END)

    if not selected_items:
        messagebox.showinfo("No Selection", "Please select at least one item.")
        return

    show_confirmation_screen(selected_items)


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
submit_button = ttk.Button(root, text="Submit", command=lambda: on_submit(data, selected_option_listbox))
submit_button.pack(pady=10)

root.mainloop()
