# import customtkinter as ctk
# import json
# import tkinter as tk
# from tkinter import Listbox, END, MULTIPLE, messagebox, ttk
# import json
# import subprocess
# from CTkMessagebox import CTkMessagebox
# from customtkinter import CTk, filedialog
# import os
# import zipfile
# from helpers import *
# from tkinter import StringVar
# from ScriptGenerateTK  import *
# from generatePolicy import *


# def set_checkboxes(tab_name, i, checkbox_var,json_data):
#     # Sample JSON data structure

#     # Assuming tab_name is present in the JSON data
#     if tab_name in json_data:
#         # Check if (i + 1) is in the corresponding list for the tab_name
#         if (i + 1) in [item["value"] for item in json_data[tab_name]]:
#             checkbox_var.set(1)

# # def download_Json(selected_items):
# #     for selected_item in selected_items:
# #         print(f"Downloading YAML for {selected_item}")

# #     try:
# #         # Prompt user for the destination path to save the zip file
# #         # destination_path = filedialog.askdirectory(title="Select Destination Folder")
# #         destination_path = os.getcwd()

# #         if destination_path:
# #                 with open("selectedFileName.txt", "w") as file:
# #                 # Write each selected item on a separate line
# #                     for item in selected_items:
# #                         file.write(f"{item}\n")


# #             # Display a success message
# #                 CTkMessagebox(message="Success! folder downloaded successfully.",
# #                   icon="check", option_1="Done")

# #     except Exception as e:
# #         # Display an error message if something goes wrong
# #         CTkMessagebox(title="Error", message=f"Something went wrong!!! \\n An error occurred: {str(e)}", icon="cancel")




# # Fuctions

# def hide_all_screens():
#     for widget in app.winfo_children():
#         widget.grid_forget()



# def load_data(file_path):
#     try:
#         with open(file_path) as f:
#             return json.load(f)
#     except FileNotFoundError:
#         print(f"File not found: {file_path}")
#         return {}


# def on_submit(data, selected_option_list):
    

#     destination_path = os.getcwd()

#     try:
#         # Prompt user for the destination path to save the zip file
#         # destination_path = filedialog.askdirectory(title="Select Destination Folder")
#         destination_path = os.getcwd()

#         if destination_path:
#                 with open("selectedFileName.txt", "w") as file:
#                 # Write each selected item on a separate line
#                     for item in selected_option_list:
#                         file.write(f"{item}\n")


#             # Display a success message
#                 CTkMessagebox(message="Success! file downloaded successfully.",
#                   icon="check", option_1="Done")

#     except Exception as e:
#         # Display an error message if something goes wrong
#         CTkMessagebox(title="Error", message=f"Something went wrong!!! \\n An error occurred: {str(e)}", icon="cancel")

#     if not selected_option_list:
#         CTkMessagebox(title="Warning Message!", message="Unable to connect!", icon="warning", option_1="Cancel", option_2="Retry")
#         return
#     show_confirmation_screen(selected_option_list,data)


# def show_confirmation_screen(selected_items,json_data):
#     popup = ctk.CTk()
#     popup.title("Confirmation")

#     window_width = 300
#     window_height = 200

#     screen_width = popup.winfo_screenwidth()
#     screen_height = popup.winfo_screenheight()

#     x_position = (screen_width - window_width) // 2
#     y_position = (screen_height - window_height) // 2

#     popup.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

#     def download_Json_wrapper():
#         popup.destroy()
#         generateJson(selected_items,"/home/vinayak1506/Desktop/Compliant-Master/data.json","/home/vinayak1506/Desktop/Compliant-Master/generated_policy/Policy.json")

#     def harden_now_wrapper():
#         popup.destroy()
#         harden_now(selected_items,json_data)



#     download_button = ctk.CTkButton(popup, text="Download Policy", command=download_Json_wrapper )
#     download_button.pack( padx=10,pady=10)
    
#     download_button = ctk.CTkButton(popup, text="Generate Script", command=generateScript )
#     download_button.pack( padx=10,pady=10)


#     hardening_button = ctk.CTkButton(popup, text="Start Hardening", command=harden_now_wrapper)
#     hardening_button.pack( padx=10,pady=10)

#     cancel_button = ctk.CTkButton(popup, text="Cancel",  command=popup.destroy )
#     cancel_button.pack(pady=10)

#     popup.mainloop()

    


    
# def harden_now(selected_items,json_data):
#     for selected_item in selected_items:
#         print(f"Hardening NOW for {selected_item}")
#         selected_id, selected_exec_file = find_selected_details(selected_item, json_data)
#         execute_script_and_display_result(selected_exec_file)

# def execute_script_and_display_result(exec_file):
#     output_frame = ctk.CTkFrame(app, corner_radius=3)
#     output_label=ctk.CTkLabel(output_frame,text="Script Execution Result", font=("Arial", 24))
#     output_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
#   # Set the parent window

#     output_text = ctk.CTkTextbox(output_frame, wrap=ctk.WORD, width=500, height=300, font=("Arial", 12))
#     output_text.grid(row=1, column=0, padx=20, pady=10, sticky="w")
#     def show_frame():
#         hide_all_screens()  
#         output_frame.grid(row=0, column=0, padx=16, pady=20, rowspan=3, columnspan=3, sticky="nsew")
#         app.update()
    
#     show_frame()

#     try:
#         current_dir = os. getcwd()
#         scriptFile = current_dir + "/" + exec_file
#         process = subprocess.run(['bash', exec_file], text=True, stdout=subprocess.PIPE, check=True)
#         output_text.insert(ctk.END, process.stdout)
#     except subprocess.CalledProcessError as e:
#         output_text.insert(ctk.END, f"Error executing script:\n{e}")

#     output_frame.grab_set()
#       # Make the output window modal


# def find_selected_details(selected_name, json_data):
#     for id, details in json_data.items():
#         if details['name'] == selected_name:
#             return id, details.get('execFile', 'Exec file not found')
#     return None, None



# def on_double_left_click(event, source_listbox, destination_listbox):
#     cur_index = source_listbox.nearest(event.y)
#     cur_item = source_listbox.get(cur_index)
#     source_listbox.delete(cur_index)
#     destination_listbox.insert(tk.END, cur_item)

# def exit():
#     app.destroy()
#     subprocess.run(["python3", "Dashboard.py", "--show-frame", "Options"])



# selected_options=[]


# class MyTabView(ctk.CTkTabview):
#     def __init__(self, master, checkboxes_list, json_data, **kwargs):
#         super().__init__(master, **kwargs)
#         self.json_data = json_data

#         tab_font = ("Arial", 16, "bold")
#         self.add("All")
#         self.add("CISF")
#         self.add("Hippa")
       
#         self.checkbox_frames = {}
#         for tab_name in ["All","CISF","Hippa"]:
#             tab_frame = self.tab(tab_name)
#             label = ctk.CTkLabel(tab_frame, text=tab_name, font=tab_font)
#             label.pack(pady=5)

#             label.bind("<ButtonRelease-1>", lambda event, tab_name=tab_name: self.on_tab_changed(event, tab_name))

#             frame = ctk.CTkFrame(master=tab_frame)
#             frame.pack(fill="both", expand=True)

#             checkboxes_tab = []
#             for key, policy in self.json_data.items():
#                 tags = policy.get("tag", [])
#                 if tab_name in tags:
#                     checkbox_var = ctk.IntVar()
#                     checkbox = ctk.CTkCheckBox(frame, text=policy["name"], variable=checkbox_var, font=("Arial", 14))
#                     checkbox.grid(row=int(key) // 3, column=int(key) % 3, padx=10, pady=15, sticky="w")
#                     checkboxes_tab.append(checkbox_var)
#                     selected_options.append(policy["name"])
#                 else:
#                     if "1" in tags:
#                         checkbox_var = ctk.IntVar()
#                         checkbox = ctk.CTkCheckBox(frame, text=policy["name"], variable=checkbox_var, font=("Arial", 14))
#                         checkbox.grid(row=int(key) // 3, column=int(key) % 3, padx=10, pady=15, sticky="w")
#                         checkboxes_tab.append(checkbox_var)
#                         checkbox_var.set(1)
#                         selected_options.append(policy["name"])



#                     elif "2" in tags:
#                         checkbox_var = ctk.IntVar()
#                         checkbox = ctk.CTkCheckBox(frame, text=policy["name"], variable=checkbox_var, font=("Arial", 14))
#                         checkbox.grid(row=int(key) // 3, column=int(key) % 3, padx=10, pady=15, sticky="w")
#                         checkboxes_tab.append(checkbox_var)
#                         checkbox_var.set(1)
#                         selected_options.append(policy["name"])



                        

#             self.checkbox_frames[tab_name] = checkboxes_tab

#         # Set checkboxes initially when the view is created
#         self.set_checkboxes("CISF")
#         self.set_checkboxes("Hippa")
        

#     def set_checkboxes(self, tab_name):
#         checkboxes_tab = self.checkbox_frames.get(tab_name, [])
#         for i, checkbox_var in enumerate(checkboxes_tab):
#             set_checkboxes(tab_name, i, checkbox_var,self.json_data)

#     def clear_checkboxes(self):
#         for checkboxes_tab in self.checkbox_frames.values():
#             for checkbox_var in checkboxes_tab:
#                 checkbox_var.set(0)



# class App(ctk.CTk):
#     def __init__(self):
#         super().__init__()

     
#         def load_data(file_path):
#             try:
#                 with open(file_path) as f:
#                     return json.load(f)
#             except FileNotFoundError:
#                 print(f"File not found: {file_path}")
#                 return {}


#         json_data  = load_data('/home/vinayak1506/Desktop/sih/Compliant-Master/data.json')


#         welcome_label = ctk.CTkLabel(master=self, text="Welcome Root", font=("Arial", 24))
#         welcome_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

#         logout_button = ctk.CTkButton(master=self, text="Logout", command=self.logout, font=("Arial", 14))
#         logout_button.grid(row=0, column=1, padx=20, pady=20, sticky="e", columnspan=2)

#         # OptionMenu
#         self.optionmenu_var = ctk.StringVar(value="Level 1")  # set initial value

#         def optionmenu_callback():
#             self.tab_view.clear_checkboxes()
#             print("OptionMenu selected:")

#         combobox = ctk.CTkOptionMenu(master=self,
#                                      values=["Level 1","Level 2"],
#                                      command=lambda value: optionmenu_callback(value),
#                                      variable=self.optionmenu_var)
#         combobox.grid(row=1, column=0, padx=220, pady=10, sticky="w", columnspan=3)

#         checkboxes = []
#         self.tab_view = MyTabView(master=self, checkboxes_list=checkboxes, json_data=json_data)
#         self.tab_view.grid(row=2, column=0, padx=20, pady=20, sticky="nsew", columnspan=3)

#         submit_button = ctk.CTkButton(master=self, text="Submit", command=lambda: on_submit(json_data, selected_options ),  font=("Arial", 14))
#         submit_button.grid(row=3, column=0, padx=20, pady=10, columnspan=3)

#         self.rowconfigure(2, weight=1)
#         self.columnconfigure(0, weight=1)
#         self.columnconfigure(1, weight=1)
#         self.columnconfigure(2, weight=1)

#         screen_width = self.winfo_screenwidth()
#         screen_height = self.winfo_screenheight()

#         window_width = 800
#         window_height = 800

#         x_position = (screen_width - window_width) // 2
#         y_position = (screen_height - window_height) // 2

#         self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

#     def logout(self):
#         print("Logout clicked")


#     def on_submit(self):
#         selected_option = self.optionmenu_var.get()
#         print("Selected Option:", selected_options)
#         print("Form submitted")


#     def on_tab_changed(self, event, tab_name):
#         self.tab_view.set_checkboxes(tab_name)






# if __name__ == "__main__":
#     app = App()
#     app.mainloop()