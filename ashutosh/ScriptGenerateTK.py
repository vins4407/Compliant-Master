import tkinter as tk
from tkinter import filedialog, ttk
import json
import os

def on_click():
    with open('selectedFileName.txt', 'r') as file:
        selected_names = file.readlines()

    with open('data.json', 'r') as file:
        data = json.load(file)

    with open('My-Script.sh', 'a') as my_script:
        for name in selected_names:
            name = name.strip()
            for key, value in data.items():
                if value['name'] == name:
                    with open(value['execFile'], 'r') as execfile:
                        content = execfile.read()
                        my_script.write(content)
                    break

    def save_file():
        file = filedialog.asksaveasfile(mode='w', defaultextension=".sh")
        if file is None:
            return
        with open('My-Script.sh', 'r') as file_to_write:
            file.write(file_to_write.read())
        file.close()

    save_file()
    os.remove('My-Script.sh')

app = tk.Tk()
app.geometry('200x100')

frame = ttk.Frame(app, padding='10')
frame.pack()

button = ttk.Button(frame, text='Create Script', command=on_click)
button.pack(pady=20)

app.mainloop()