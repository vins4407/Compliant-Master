import tkinter as tk
from tkinter import messagebox
import json
import customtkinter as ctk
from tkinter import Listbox, END, MULTIPLE, messagebox, ttk
import subprocess
from CTkMessagebox import CTkMessagebox
from customtkinter import CTk, filedialog
import os
import zipfile
from helpers import *
from tkinter import StringVar
from ScriptGenerateTK  import *
from generatePolicy import *



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


def on_submit(data, selected_option_list):
    

    destination_path = os.getcwd()

    try:
        # Prompt user for the destination path to save the zip file
        # destination_path = filedialog.askdirectory(title="Select Destination Folder")
        destination_path = os.getcwd()

        if destination_path:
                with open("selectedFileName.txt", "w") as file:
                # Write each selected item on a separate line
                    for item in selected_option_list:
                        file.write(f"{item}\n")


            # Display a success message
                CTkMessagebox(message="Success! file downloaded successfully.",
                  icon="check", option_1="Done")

    except Exception as e:
        # Display an error message if something goes wrong
        CTkMessagebox(title="Error", message=f"Something went wrong!!! \\n An error occurred: {str(e)}", icon="cancel")

    if not selected_option_list:
        CTkMessagebox(title="Warning Message!", message="Unable to connect!", icon="warning", option_1="Cancel", option_2="Retry")
        return
    show_confirmation_screen(selected_option_list,data)



def show_confirmation_screen(selected_items,json_data):
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
        generateJson(selected_items,"data.json","Policy.json")

    def harden_now_wrapper():
        popup.destroy()
        harden_now(selected_items,json_data)



    download_button = ctk.CTkButton(popup, text="Download Policy", command=download_Json_wrapper )
    download_button.pack( padx=10,pady=10)
    
    download_button = ctk.CTkButton(popup, text="Generate Script", command=generateScript )
    download_button.pack( padx=10,pady=10)


    hardening_button = ctk.CTkButton(popup, text="Start Hardening", command=harden_now_wrapper)
    hardening_button.pack( padx=10,pady=10)

    cancel_button = ctk.CTkButton(popup, text="Cancel",  command=popup.destroy )
    cancel_button.pack(pady=10)

    popup.mainloop()

def harden_now(selected_items,json_data):
    for selected_item in selected_items:
        print(f"Hardening NOW for {selected_item}")
        selected_id, selected_exec_file = find_selected_details(selected_item, json_data)
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
        scriptFile = current_dir + "/" + exec_file
        process = subprocess.run(['bash', exec_file], text=True, stdout=subprocess.PIPE, check=True)
        output_text.insert(ctk.END, process.stdout)
    except subprocess.CalledProcessError as e:
        output_text.insert(ctk.END, f"Error executing script:\n{e}")

    output_frame.grab_set()
      # Make the output window modal


def find_selected_details(selected_name, json_data):
    for id, details in json_data.items():
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



class CustomBox(tk.Canvas):
    def __init__(self, master, index, name, exec_file, is_special_case, callback):
        super().__init__(master, width=150, height=60, bg='white', highlightthickness=0)
        self.index = index
        self.name = name
        self.exec_file = exec_file
        self.is_special_case = is_special_case
        self.selected = False
        self.create_rectangle(5, 5, 145, 55, outline='black', width=2)
        self.create_text(75, 30, text=name, width=140)

        self.info_button = tk.Button(self, text="i", command=self.show_info, font=("Arial", 8, "bold"))
        if self.is_special_case == 'yes':
            self.info_button.place(relx=1, rely=0, anchor="ne")

        self.bind("<Button-1>", self.toggle_color)
        self.callback = callback

    def toggle_color(self, event):
        self.selected = not self.selected
        self.set_color()
        self.callback(self)

    def set_color(self):
        if self.selected:
            self.configure(bg='green')
        else:
            self.configure(bg='white')

 
    def show_info(self):
        if self.is_special_case == 'yes':
            messagebox.showinfo("Box Information", f"This is a special case: {self.name}")
            self.info_button.place(relx=1, rely=0, anchor="ne")

            info_window = tk.Toplevel(self)
            info_window.title("Box Information")

            if self.name == "Secure IP Tables":
                description_label = tk.Label(info_window, text="This will only allow incoming traffic on the specified ports.")
                description_label.pack(pady=5)

                # Input field for comma-separated choices of ports
                port_entry_label = tk.Label(info_window, text="Enter ports (comma-separated):")
                port_entry_label.pack(pady=5)

                port_var = tk.StringVar()
                port_entry = tk.Entry(info_window, textvariable=port_var)
                port_entry.pack(pady=5)

                submit_button = tk.Button(info_window, text="Submit", command=lambda: self.update_iptable_script(port_var.get(), info_window))
                submit_button.pack(pady=5)

            else:
                description_label = tk.Label(info_window, text="No special information available for this box.")
                description_label.pack(pady=5)

    def update_iptable_script(self, ports, info_window):
        # Update the script with the selected ports
        new_script = f"""hardenIpTables1(){{
    # Flush existing rules
    sudo iptables -F

    # Set default policies to DROP
    sudo iptables -P INPUT DROP
    sudo iptables -P FORWARD DROP
    sudo iptables -P OUTPUT ACCEPT

    sudo iptables -A INPUT -p tcp --dports {ports} -j ACCEPT

    
    # Allow loopback traffic
    sudo iptables -A INPUT -i lo -j ACCEPT
    sudo iptables -A OUTPUT -o lo -j ACCEPT

    # Allow custom incoming ports
    sudo iptables -A INPUT -p tcp --dports {ports} -j ACCEPT

    # Display the rules
    sudo iptables -L INPUT -n
}}

hardenIpTables1
"""
        # Update the script file (you may want to adjust the path accordingly)
        script_file_1 = os.getcwd()

        script_file_path = "config/B_scripts/hardenIpTables1.sh"
        with open(script_file_path, "w") as script_file:
            script_file.write(new_script)

        # Inform the user
        messagebox.showinfo("Script Updated", "Script has been updated with the selected ports.")

        # Close the info window
        info_window.destroy()


class GUI:
    def __init__(self, master, data):
        self.master = master
        self.data = data
        self.custom_boxes = []
        self.selected_objects = []
        self.filtered_data = data

        filter_frame = ttk.Frame(master)
        filter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.tag_var = tk.StringVar()
        self.tag_var.set("All")

        tag_label = ttk.Label(filter_frame, text="Select Tag:")
        tag_label.grid(row=0, column=0, padx=5, pady=5)

        tag_combobox = ttk.Combobox(filter_frame, textvariable=self.tag_var, values=["All"] + list(set(tag for details in data.values() for tag in details["tag"])))
        tag_combobox.grid(row=0, column=1, padx=5, pady=5)

        filter_button = tk.Button(filter_frame, text="Apply Filter", command=self.apply_filter)
        filter_button.grid(row=0, column=2, padx=5, pady=5)

        select_all_button = tk.Button(filter_frame, text="Select All", command=self.select_all)
        select_all_button.grid(row=0, column=3, padx=5, pady=5)

        deselect_all_button = tk.Button(filter_frame, text="Deselect All", command=self.deselect_all)
        deselect_all_button.grid(row=0, column=4, padx=5, pady=5)

        self.canvas_frame = ttk.Frame(master)
        self.canvas_frame.grid(row=1, column=0, padx=10, pady=10)

        for index, details in data.items():
            custom_box = CustomBox(self.canvas_frame, index, details["name"], details["execFile"], details.get("isSpecialCase", False), self.on_box_click)
            self.custom_boxes.append(custom_box)
            custom_box.grid(row=len(self.custom_boxes)//3, column=len(self.custom_boxes)%3, padx=10, pady=10)

        submit_button = tk.Button(master, text='Submit', command=lambda:on_submit(data, self.selected_objects),)
        submit_button.grid(row=2, column=0, pady=10)

        self.exec_files = []

    def on_box_click(self, clicked_box):
        if clicked_box.selected:
            self.selected_objects.append(clicked_box.name)
            self.exec_files.append(clicked_box.exec_file)
        else:
            self.selected_objects.remove(clicked_box.name)
            self.exec_files.remove(clicked_box.exec_file)

    def apply_filter(self):
        selected_tag = self.tag_var.get()
        if selected_tag == "All":
            self.filtered_data = self.data
        else:
            self.filtered_data = {index: details for index, details in self.data.items() if selected_tag in details["tag"]}
        
        self.refresh_boxes()

    def refresh_boxes(self):
        for box in self.custom_boxes:
            box.destroy()

        for index, details in self.filtered_data.items():
            custom_box = CustomBox(self.canvas_frame, index, details["name"], details["execFile"], details.get("isSpecialCase", False), self.on_box_click)
            self.custom_boxes.append(custom_box)
            custom_box.grid(row=len(self.custom_boxes)//3, column=len(self.custom_boxes)%3, padx=10, pady=10)

    def select_all(self):
        for box in self.custom_boxes:
            box.selected = True
            box.set_color()
            self.on_box_click(box)

    def deselect_all(self):
        for box in self.custom_boxes:
            box.selected = False
            box.set_color()
            self.on_box_click(box)





def main():
    # Load data from JSON file
    with open("data.json", "r") as json_file:
        data = json.load(json_file)

    root = tk.Tk()
    root.title("Custom Color Boxes Selector")

    gui = GUI(root, data)

    root.mainloop()

if __name__ == "__main__":
    main()