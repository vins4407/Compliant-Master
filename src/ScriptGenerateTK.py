import tkinter as tk
from tkinter import filedialog, ttk
import json
import os
from CTkMessagebox import CTkMessagebox

def generateScript():
    with open('selectedFileName.txt', 'r') as file:
        selected_names = file.readlines()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "..", "data.json")
    script_file_path = os.path.join(current_dir,"..", "generated_scripts/My-Script.sh")



    with open(json_file_path, 'r') as file:
        data = json.load(file)

    with open(script_file_path, 'a') as my_script:
        for name in selected_names:
            name = name.strip()
            for key, value in data.items():
                if value['name'] == name:
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    exec_file_path = os.path.join(current_dir, "..", value['execFile'])
                    with open(exec_file_path, 'r') as execfile:
                        content = execfile.read()
                        my_script.write(content)
                    break

    def save_file():
        file = filedialog.asksaveasfile(mode='w', defaultextension=".sh")
        if file is None:
            return
        with open(script_file_path, 'r') as file_to_write:
            file.write(file_to_write.read())
        file.close()
        CTkMessagebox(message="Success! file downloaded successfully.",
                  icon="check", option_1="Done")


    save_file()
    os.remove(script_file_path)

