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
from ScriptGenerateTK  import *
from generatePolicy import *
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

def set_checkboxes(tab_name, i, checkbox_var):
    # Sample JSON data structure
    json_data = {
        "CISF": [
            {"value": 1, "name": "Value One"},
            {"value": 2, "name": "Value Two"},
            {"value": 3, "name": "Value Three"}
        ],
        "Hippa": [
            {"value": 1, "name": "Value One"},
            {"value": 2, "name": "Value Two"},
            {"value": 3, "name": "Value Three"},
            {"value": 4, "name": "Value Four"},
            {"value": 5, "name": "Value Five"}
        ],
        "Level3": [
            {"value": 1, "name": "Value One"},
            {"value": 2, "name": "Value Two"},
            {"value": 3, "name": "Value Three"},
            {"value": 4, "name": "Value Four"},
            {"value": 5, "name": "Value Five"},
            {"value": 6, "name": "Value Six"},
            {"value": 7, "name": "Value Seven"},
            {"value": 8, "name": "Value Eight"},
            {"value": 9, "name": "Value Nine"}
        ]
    }

    # Assuming tab_name is present in the JSON data
    if tab_name in json_data:
        # Check if (i + 1) is in the corresponding list for the tab_name
        if (i + 1) in [item["value"] for item in json_data[tab_name]]:
            checkbox_var.set(1)


# Tab-View
class MyTabView(ctk.CTkTabview):
    def _init_(self, master, checkboxes_list, json_data, **kwargs):
        super()._init_(master, **kwargs)
        self.json_data = json_data

        tab_font = ("Arial", 16, "bold")

        self.add("ALL")
        self.add("CISF")
        self.add("Hippa")
       

        self.checkbox_frames = {}
        for tab_name in ["CISF", "Hippa"]:
            tab_frame = self.tab(tab_name)
            label = ctk.CTkLabel(tab_frame, text=tab_name, font=tab_font)
            label.pack(pady=5)

            label.bind("<ButtonRelease-1>", lambda event, tab_name=tab_name: self.on_tab_changed(event, tab_name))

            frame = ctk.CTkFrame(master=tab_frame)
            frame.pack(fill="both", expand=True)

            checkboxes_tab = []

            for i, item in enumerate(json_data.get(tab_name, [])):
                checkbox_var = ctk.IntVar()
                checkbox = ctk.CTkCheckBox(frame, text=item["name"], variable=checkbox_var, font=("Arial", 14))
                checkbox.grid(row=i // 3, column=i % 3, padx=10, pady=15, sticky="w")
                checkboxes_tab.append(checkbox_var)

            self.checkbox_frames[tab_name] = checkboxes_tab

        # Set checkboxes initially when the view is created
        self.set_checkboxes("CISF")
        self.set_checkboxes("Hippa")
        

    def set_checkboxes(self, tab_name):
        checkboxes_tab = self.checkbox_frames.get(tab_name, [])

        for i, checkbox_var in enumerate(checkboxes_tab):
            set_checkboxes(tab_name, i, checkbox_var)


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



def download_Json(selected_items):
    for selected_item in selected_items:
        print(f"Downloading YAML for {selected_item}")

    try:
        # Prompt user for the destination path to save the zip file
        # destination_path = filedialog.askdirectory(title="Select Destination Folder")
        destination_path = os.getcwd()

        if destination_path:
                with open("selectedFileName.txt", "w") as file:
                # Write each selected item on a separate line
                    for item in selected_items:
                        file.write(f"{item}\n")


            # Display a success message
                CTkMessagebox(message="Success! folder downloaded successfully.",
                  icon="check", option_1="Done")

    except Exception as e:
        # Display an error message if something goes wrong
        CTkMessagebox(title="Error", message=f"Something went wrong!!! \\n An error occurred: {str(e)}", icon="cancel")




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
    generatePolicy(selected_items,"data.json","Policy.json")
    
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

    def download_Json_wrapper():
        popup.destroy()
        generatePolicy(selected_items,"data.json","Policy.json")
        popup.destroy()

    def harden_now_wrapper():
        popup.destroy()
        harden_now(selected_items)
        popup.destroy()


    label = ctk.CTkLabel(popup, text=f"Confirm action for {', '.join(selected_items)}", font=("Arial", 14))
    label.pack(pady=10)

    download_button = ctk.CTkButton(popup, text="Download Policy", command=download_Json_wrapper )
    download_button.pack( padx=10)
    
    download_button = ctk.CTkButton(popup, text="Generate Script", command=generateScript )
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
sebi_names = [details["name"] for id, details in data.items() if "1" in details["tag"]]
print(sebi_names)
certin_name = [details["name"] for id, details in data.items() if "2" in details["tag"]]
print(certin_name)
hippa_name = [details["name"] for id, details in data.items() if "3" in details["tag"]]
print(hippa_name)

# Draggable UI using Frames
json_data = {
            "CISF": [
                {"value": 1, "name": "SSH"},
                {"value": 2, "name": "TOR"},
                {"value": 3, "name": "TOR"}
            ],
            "Hippa": [
                {"value": 1, "name": "TOR"},
                {"value": 2, "name": "TOR2"},
                {"value": 3, "name": "TOR3"},
            ]
            
        }

main_frame = ctk.CTkFrame(app, corner_radius=20)
main_frame.grid(row=0, column=0, sticky="nsew")

welcome_label = ctk.CTkLabel(main_frame, text="Welcome Root", font=("Arial", 24))
welcome_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

logout_button = ctk.CTkButton(main_frame, text="exit", command=exit ,font=("Arial", 20),)
logout_button.grid(row=0, column=2, padx=150, pady=20, sticky="e")


        # OptionMenu
optionmenu_var = ctk.StringVar(value="Level 1")  # set initial value

def optionmenu_callback(choice):
    print("OptionMenu selected:", choice)

combobox = ctk.CTkOptionMenu(master=main_frame,
                                     values=["Level 2 "],
                                     command=optionmenu_callback,
                                     variable=optionmenu_var)
combobox.grid(row=1, column=0, padx=220, pady=10, sticky="w", columnspan=3)

checkboxes = []
tab_view = MyTabView(master=main_frame ,checkboxes_list=checkboxes, json_data=json_data)
tab_view.grid(row=2, column=0, padx=20, pady=20, sticky="nsew", columnspan=3)

submit_button = ctk.CTkButton(master=main_frame, text="Submit", command=submit, font=("Arial", 14))
submit_button.grid(row=3, column=0, padx=20, pady=10, columnspan=3)

rowconfigure(2, weight=1)
columnconfigure(0, weight=1)
columnconfigure(1, weight=1)
columnconfigure(2, weight=1)



def logout():
        print("Logout clicked")

def submit():
        selected_option = optionmenu_var.get()
        print("Selected Option:", selected_option)
        print("Form submitted")

def on_tab_changed( event, tab_name):
        tab_view.set_checkboxes(tab_name)





# options

# New frame for Options_frame
# Options_frame_container = ctk.CTkFrame(app)
# Options_frame_container.grid(row=2, column=0, padx=120, pady=10, sticky="nsew")

# # Options_frame inside Options_frame_container
# Options_frame = ctk.CTkFrame(Options_frame_container, corner_radius=0)
# Options_frame.grid(row=0, column=0, pady
#                    =0)

# selected_option = tk.StringVar()
# options = ["1", "2", "3"]

# selected_option.set(options[0])  # Set default option (Optional)
# option1_button = ctk.CTkRadioButton(Options_frame, text=options[0], variable=selected_option, value=options[0])
# option2_button = ctk.CTkRadioButton(Options_frame, text=options[1], variable=selected_option, value=options[1])
# option3_button = ctk.CTkRadioButton(Options_frame, text=options[2], variable=selected_option, value=options[2])

# option1_button.grid(row=0, column=0, pady=0)
# option2_button.grid(row=0, column=1, pady=10)
# option3_button.grid(row=0, column=2, pady=10)

# option1_button.bind("<Button-1>", lambda event: get_selection(selected_option.get()))
# option2_button.bind("<Button-1>", lambda event: get_selection(selected_option.get()))
# option3_button.bind("<Button-1>", lambda event: get_selection(selected_option.get()))


# def get_selection(selected_option):
#     available_option_listbox.delete(0, tk.END)

#     if selected_option=="1":
#         for details in sebi_names:
#             available_option_listbox.insert(tk.END, f"{details}")
#     elif selected_option=="2":
#         for details in certin_name:
#             available_option_listbox.insert(tk.END, f"{details}")
#     elif selected_option=="3":
#         for details in hippa_name:
#             available_option_listbox.insert(tk.END, f"{details}")
#     else:
#         for id, details in data.items():
#             available_option_listbox.insert(tk.END, f"{details['name']}")





# New frame for Selection_frame
Selection_frame_container = ctk.CTkFrame(app)
Selection_frame_container.grid(row=2, column=0, columnspan=3, padx= 0,pady=70)


Selection_frame = ctk.CTkFrame(Selection_frame_container)
Selection_frame.grid(row=0, column=0, pady=0)

left_frame = ctk.CTkFrame(Selection_frame)
left_frame.grid(row=1, column=0, padx=0, pady=30, sticky="nsew")

right_frame = ctk.CTkFrame(Selection_frame)
right_frame.grid(row=1, column=1, padx=0, pady=30, sticky="nsew")

label_available = ctk.CTkLabel(left_frame, text="Available Rules", font=("Helvetica", 20))
label_available.pack(pady=5)

label_selected = ctk.CTkLabel(right_frame, text="Selected Rules", font=("Helvetica", 20))
label_selected.pack(pady=5)



available_option_listbox = DragDropListbox(left_frame, None, "available_options", selectmode=MULTIPLE)
selected_option_listbox = DragDropListbox(right_frame, available_option_listbox, "selected_options", selectmode=MULTIPLE)
available_option_listbox.other_listbox = selected_option_listbox

# Populate available options listbox with names from data.json

print(selected_option_listbox)

for id, details in data.items():
    available_option_listbox.insert(tk.END, f"{details['name']}")

    
available_option_listbox.pack(expand=True, fill="both")
selected_option_listbox.pack(expand=True, fill="both")

# Bind the double click event to the DragDropListbox instances
available_option_listbox.bind('<Double-Button-1>', lambda event: on_double_left_click(event, available_option_listbox, selected_option_listbox))
selected_option_listbox.bind('<Double-Button-1>', lambda event: on_double_left_click(event, selected_option_listbox, available_option_listbox))


submit_button = ctk.CTkButton(Selection_frame, text="Submit", command=lambda: on_submit(data, selected_option_listbox),     font=("Arial", 20))
submit_button.grid(row=5, column=1, pady=10 )

app.mainloop()