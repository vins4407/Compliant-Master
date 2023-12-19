import tkinter as tk
import customtkinter as ctk
from tkinter import Listbox, END, MULTIPLE, messagebox, ttk
import json
import subprocess
from CTkMessagebox import CTkMessagebox
from customtkinter import CTk, filedialog
import os
import zipfile
from helpers import *
from tkinter import StringVar

# Create Main Loop:

app = ctk.CTk()
app.title("Rules")
ctk.set_default_color_theme("green")
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

window_width = 650
window_height = 650

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")



# Tab-View

class MyTabView(ctk.CTkTabview):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)

        tab_font = ("Arial", 16, "bold")

        self.add("All")
        self.add("Hippa")
        self.add("certing")
        self.add("sebi")
        self.add("ISO")


        # self.checkbox_frames = {}
        # for tab_name in ["All", "Hippa", "certing", "sebi", "ISO"]:
        #     tab_frame = self.tab(tab_name)
        #     label = ctk.CTkLabel(tab_frame, text=tab_name, font=tab_font)
        #     label.pack(pady=5)

        #     label.bind("<ButtonRelease-1>", lambda event, tab_name=tab_name: self.on_tab_changed(event, tab_name))

        #     frame = ctk.CTkFrame(master=tab_frame)
        #     frame.pack(fill="both", expand=True)

        #     checkboxes_tab = []

        #     for i in range(9):
        #         checkbox_id = f"{tab_name}_Option_{i + 1}"
        #         checkbox_var = ctk.IntVar()
        #         checkbox = ctk.CTkCheckBox(frame, text=f"Option {i + 1}", variable=checkbox_var, font=("Arial", 14))
        #         checkbox.grid(row=i // 3, column=i % 3, padx=10, pady=15, sticky="w")

        #         if tab_name == "All":
        #             checkbox_var.set(1)
        #         elif tab_name == "Hippa" and (i + 1) in [1, 3]:
        #             checkbox_var.set(1)
        #         elif tab_name == "certing" and (i + 1) in [8, 9]:
        #             checkbox_var.set(1)
        #         elif tab_name == "sebi" and (i + 1) in [1, 8]:
        #             checkbox_var.set(1)
        #         elif tab_name == "ISO" and (i + 1) in [7, 9]:
        #             checkbox_var.set(1)

        #         checkboxes_tab.append(checkbox)

        #     checkboxes_list.append(checkboxes_tab)
        #     self.checkbox_frames[tab_name] = checkboxes_tab

def on_tab_changed(event, tab_name):
        current_tab_name = tab_name

        for tab_frame_name, checkbox_frame in self.checkbox_frames.items():
            for checkbox in checkbox_frame:
                checkbox_var = checkbox.var()

                if current_tab_name == "Hippa":
                    checkbox.grid()

                else:
                    if "_en" not in checkbox.tag:
                        checkbox.grid_remove()
                    else:
                        checkbox.grid()


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

# # Download zip/json/yaml file  

# def download_yaml(selected_items):
#     for selected_item in selected_items:
#         print(f"Downloading YAML for {selected_item}")
#         config_folder_path = "config"  # Replace with the actual path to your "config" folder

#     try:
#         # Prompt user for the destination path to save the zip file
#         destination_path = filedialog.askdirectory(title="Select Destination Folder")

#         if destination_path:
#             # Create a zip file named "config_archive.zip" in the selected destination
#             zip_file_path = os.path.join(destination_path, "config_archive.zip")

#             with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
#                 # Add all files and subdirectories from the Config folder to the zip archive
#                 for root, dirs, files in os.walk(config_folder_path):
#                     for file in files:
#                         file_path = os.path.join(root, file)
#                         arcname = os.path.relpath(file_path, config_folder_path)
#                         zip_file.write(file_path, arcname)

#             # Display a success message
#             CTkMessagebox(message="Success! Config folder zipped successfully.",
#                   icon="check", option_1="Done")

#     except Exception as e:
#         # Display an error message if something goes wrong
#         CTkMessagebox(title="Error", message=f"Something went wrong!!! \\n An error occurred: {str(e)}", icon="cancel")




# Fuctions

def hide_all_screens():
    for widget in app.winfo_children():
        widget.grid_forget()



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
        CTkMessagebox(title="Warning Message!", message="Unable to connect!", icon="warning", option_1="Cancel", option_2="Retry")
        return
    show_confirmation_screen(selected_items)


def show_confirmation_screen(selected_items):
    popup = ctk.CTk()
    popup.title("Confirmation")

    window_width = 300
    window_height = 200

    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    popup.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # def download_yaml_wrapper():
    #     popup.destroy()
    #     download_yaml(selected_items)
    #     popup.destroy()

    def harden_now_wrapper():
        popup.destroy()
        harden_now(selected_items)
        popup.destroy()


    label = ctk.CTkLabel(popup, text=f"Confirm action for {', '.join(selected_items)}", font=("Arial", 14))
    label.pack(pady=10)

    download_button = ctk.CTkButton(popup, text="Download Policy", command=zip_config_folder )
    download_button.pack( padx=10)

    hardening_button = ctk.CTkButton(popup, text="Start Hardening", command=harden_now_wrapper)
    hardening_button.pack( padx=10,pady=10)

    cancel_button = ctk.CTkButton(popup, text="Cancel",  command=popup.destroy )

    cancel_button.pack(pady=10)

    popup.mainloop()

def harden_now(selected_items):
    for selected_item in selected_items:
        print(f"Hardening NOW for {selected_item}")
        selected_id, selected_exec_file = find_selected_details(selected_item, data)
        execute_script_and_display_result(selected_exec_file)

def execute_script_and_display_result(exec_file):
    output_frame = ctk.CTkFrame(app, corner_radius=3)
    output_label=ctk.CTkLabel(output_frame,text="Script Execution Result", font=("Arial", 24))
    output_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
  # Set the parent window

    output_text = ctk.CTkTextbox(output_frame, wrap=ctk.WORD, width=500, height=300, font=("Arial", 12))
    output_text.grid(row=1, column=0, padx=20, pady=10, sticky="w")
    def show_frame():
        hide_all_screens()  
        output_frame.grid(row=0, column=0, padx=16, pady=20, rowspan=3, columnspan=3, sticky="nsew")
        app.update()
    
    show_frame()

    try:
        current_dir = os. getcwd()
        print(current_dir)
        scriptFile = current_dir + "/" + exec_file
        print(scriptFile)
        process = subprocess.run(['bash', exec_file], text=True, stdout=subprocess.PIPE, check=True)
        output_text.insert(ctk.END, process.stdout)
    except subprocess.CalledProcessError as e:
        output_text.insert(ctk.END, f"Error executing script:\n{e}")

    output_frame.grab_set()
      # Make the output window modal


def find_selected_details(selected_name, data):
    for id, details in data.items():
        if details['name'] == selected_name:
            return id, details.get('execFile', 'Exec file not found')
    return None, None



def on_double_left_click(event, source_listbox, destination_listbox):
    cur_index = source_listbox.nearest(event.y)
    cur_item = source_listbox.get(cur_index)
    source_listbox.delete(cur_index)
    destination_listbox.insert(tk.END, cur_item)

def exit():
    app.destroy()
    subprocess.run(["python3", "Dashboard.py", "--show-frame", "Options"])



# Read data from data.json
data = load_data('data.json')
sebi_names = [details["name"] for id, details in data.items() if "SEBI" in details["tag"]]
print(sebi_names)
certin_name = [details["name"] for id, details in data.items() if "CertIN" in details["tag"]]
print(certin_name)
hippa_name = [details["name"] for id, details in data.items() if "Hippa" in details["tag"]]
print(hippa_name)

# Draggable UI using Frames

main_frame = ctk.CTkFrame(app, corner_radius=20)
main_frame.grid(row=0, column=0, sticky="nsew")

welcome_label = ctk.CTkLabel(main_frame, text="Welcome Root", font=("Arial", 24))
welcome_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

logout_button = ctk.CTkButton(main_frame, text="exit", command=exit ,font=("Arial", 20),
)
logout_button.grid(row=0, column=2, padx=20, pady=20, sticky="e")


# options

selected_option = tk.StringVar()
options = ["ALL", "SEBI", "CertIN","Hippa"]

selected_option.set(options[0]) # Set default option (Optional)
Options_frame = ctk.CTkFrame(main_frame, corner_radius=20)


option1_button = ctk.CTkRadioButton(Options_frame, text=options[0] , variable=selected_option,  value=options[0])
option2_button = ctk.CTkRadioButton(Options_frame, text=options[1]  , variable=selected_option, value=options[1])
option3_button = ctk.CTkRadioButton(Options_frame, text=options[2]   ,variable=selected_option, value=options[2])


Options_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
option1_button.grid(row=1, column=0, pady=10)
option2_button.grid(row=1, column=1, pady=10)
option3_button.grid(row=1, column=2, pady=10)

option1_button.bind("<Button-1>", lambda event: get_selection(selected_option.get()))
option2_button.bind("<Button-1>", lambda event: get_selection(selected_option.get()))
option3_button.bind("<Button-1>", lambda event: get_selection(selected_option.get()))


def get_selection(selected_option):
    available_option_listbox.delete(0, tk.END)

    if selected_option=="SEBI":
        for details in sebi_names:
            available_option_listbox.insert(tk.END, f"{details}")
    elif selected_option=="CertIN":
        for details in certin_name:
            available_option_listbox.insert(tk.END, f"{details}")
    elif selected_option=="Hippa":
        for details in hippa_name:
            available_option_listbox.insert(tk.END, f"{details}")
    else:
        for id, details in data.items():
            available_option_listbox.insert(tk.END, f"{details['name']}")

# def get_selection(selected_option):
#     available_option_listbox.delete(0, tk.END)
#     print(selected_option)
#     if selected_option == "SEBI":
#         for details in [details for id, details in data.items() if "SEBI" in details["tag"]]:
#             available_option_listbox.insert(tk.END, f"{details['name']}")
#     elif selected_option == "CertIN":
#         for details in [details for id, details in data.items() if "CertIN" in details["tag"]]:
#             available_option_listbox.insert(tk.END, f"{details['name']}")
#     else:
#         for id, details in data.items():
#             available_option_listbox.insert(tk.END, f"{details['name']}")





Selection_frame = ctk.CTkFrame(main_frame)
Selection_frame.grid(row=1, column=0, columnspan=3, pady=60)

left_frame = ctk.CTkFrame(Selection_frame)
left_frame.grid(row=1, column=0, padx=10, pady=30, sticky="nsew")

right_frame = ctk.CTkFrame(Selection_frame)
right_frame.grid(row=1, column=1, padx=10, pady=30, sticky="nsew")

label_available = ctk.CTkLabel(left_frame, text="Available Rules", font=("Helvetica", 20))
label_available.pack(pady=5)

label_selected = ctk.CTkLabel(right_frame, text="Selected Rules", font=("Helvetica", 20))
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


submit_button = ctk.CTkButton(main_frame, text="Submit", command=lambda: on_submit(data, selected_option_listbox),     font=("Arial", 20))
submit_button.grid(row=2, column=1, pady=10)

app.mainloop()