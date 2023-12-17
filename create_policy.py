import tkinter as tk
import customtkinter as ctk
from tkinter import Listbox, END, MULTIPLE, messagebox, ttk
import json
import subprocess



# Create Main Loop:

app = ctk.CTk()
app.title("Rules")
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

window_width = 580
window_height = 600

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")



# Drag UI
class DragDropListbox(Listbox):
    def __init__(self, master, other_listbox, list_name, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.other_listbox = other_listbox
        self.list_name = list_name
        self.bind('<Double-Button-1>', self.on_double_left_click)
        self.configure(font=("Arial", 12), selectbackground="#3498db", selectforeground="white")

    def on_double_left_click(self, event):
        cur_index = self.nearest(event.y)
        cur_item = self.get(cur_index)
        self.delete(cur_index)
        self.other_listbox.insert(END, cur_item)



# Fuctions
def load_data(file_path):
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}

def on_submit(data, selected_option_listbox):
    selected_items = selected_option_listbox.get(0, tk.END)
    
    print("Selected Items:", selected_items)
    if not selected_items:
        messagebox.showinfo("No Selection", "Please select at least one item.")
        return

    show_confirmation_screen(selected_items)


def show_confirmation_screen(selected_items):
    popup = ctk.CTk()
    popup.title("Confirmation")

    window_width = 300
    window_height = 150

    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    popup.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    label = ctk.CTkLabel(popup, text=f"Confirm action for {', '.join(selected_items)}", font=("Arial", 14))
    label.pack(pady=10)

    download_button = ctk.CTkButton(popup, text="Download Policy", command=lambda: download_yaml(selected_items))
    download_button.pack(side="left", padx=10)

    hardening_button = ctk.CTkButton(popup, text="Start Hardening", command=lambda: harden_now(selected_items))
    hardening_button.pack(side="right", padx=10)

    cancel_button = ctk.CTkButton(popup, text="Cancel", command=popup.destroy )
    cancel_button.pack(pady=10)

    popup.mainloop()



def download_yaml(selected_items):
    for selected_item in selected_items:
        print(f"Downloading YAML for {selected_item}")

def harden_now(selected_items):
    for selected_item in selected_items:
        print(f"Hardening NOW for {selected_item}")
        selected_id, selected_exec_file = find_selected_details(selected_item, data)
        execute_script_and_display_result(selected_exec_file)

def find_selected_details(selected_name, data):
    for id, details in data.items():
        if details['name'] == selected_name:
            return id, details.get('execFile', 'Exec file not found')
    return None, None

def execute_script_and_display_result(exec_file):
    output_window = tk.Toplevel(app)
    output_window.title("Script Execution Result")
    output_window.geometry("600x400")
    output_window.transient(app)  # Set the parent window

    output_text = tk.Text(output_window, wrap=tk.WORD, width=50, height=10)
    output_text.pack(padx=10, pady=10)

    try:
        process = subprocess.run(['bash', exec_file], text=True, stdout=subprocess.PIPE, check=True)
        output_text.insert(tk.END, process.stdout)
    except subprocess.CalledProcessError as e:
        output_text.insert(tk.END, f"Error executing script:\n{e}")

    output_window.grab_set()  # Make the output window modal
    output_window.update_idletasks()


def on_double_left_click(event, source_listbox, destination_listbox):
    cur_index = source_listbox.nearest(event.y)
    cur_item = source_listbox.get(cur_index)
    source_listbox.delete(cur_index)
    destination_listbox.insert(tk.END, cur_item)


# Read data from data.json
data = load_data('data.json')


# Draggable UI using Frames


welcome_label = ctk.CTkLabel(app, text="Welcome Root", font=("Arial", 24))
welcome_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

logout_button = ctk.CTkButton(app, text="Back")
logout_button.grid(row=0, column=2, padx=20, pady=20, sticky="e")

main_frame = ctk.CTkFrame(app)
main_frame.grid(row=1, column=0, columnspan=3)

left_frame = ctk.CTkFrame(main_frame)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

right_frame = ctk.CTkFrame(main_frame)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

label_available = ctk.CTkLabel(left_frame, text="Available Rules", font=("Helvetica", 12))
label_available.pack(pady=5)

label_selected = ctk.CTkLabel(right_frame, text="Selected Rules", font=("Helvetica", 12))
label_selected.pack(pady=5)



available_option_listbox = DragDropListbox(left_frame, None, "available_options", selectmode=MULTIPLE)
selected_option_listbox = DragDropListbox(right_frame, available_option_listbox, "selected_options", selectmode=MULTIPLE)
available_option_listbox.other_listbox = selected_option_listbox

# Populate available options listbox with names from data.json
for id, details in data.items():
    available_option_listbox.insert(tk.END, f"{details['name']}")


available_option_listbox.pack(expand=True, fill="both")
selected_option_listbox.pack(expand=True, fill="both")

# Bind the double click event to the DragDropListbox instances
available_option_listbox.bind('<Double-Button-1>', lambda event: on_double_left_click(event, available_option_listbox, selected_option_listbox))
selected_option_listbox.bind('<Double-Button-1>', lambda event: on_double_left_click(event, selected_option_listbox, available_option_listbox))


submit_button = ttk.Button(app, text="Submit", command=lambda: on_submit(data, selected_option_listbox))
submit_button.grid(row=2, column=1, pady=10)

app.mainloop()