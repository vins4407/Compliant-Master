import json
import tkinter as tk
from tkinter import Label, Entry, Button, Checkbutton, Scrollbar, messagebox

def add_entry():
    new_id = id_entry.get()
    new_name = name_entry.get()
    new_tags = [var.get() for var in tag_vars if var.get()]
    new_execFile = execFile_entry.get()

    # Read existing data.json
    with open("data.json", "r") as file:
        data = json.load(file)

    # Add new entry
    data[new_id] = {
        "name": new_name,
        "tag": new_tags,
        "execFile": new_execFile
    }

    # Write back to data.json
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    # Clear entry fields after submission
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    execFile_entry.delete(0, tk.END)

    # Show successful submission notification
    messagebox.showinfo("Success", "Entry submitted successfully!")

# Create the main window
root = tk.Tk()
root.title("Data Entry Form")
root.minsize(600, 600)

# ID Entry
Label(root, text="ID:").grid(row=0, column=0, pady=10, sticky=tk.W)
id_entry = Entry(root)
id_entry.grid(row=0, column=1, pady=10)

# Name Entry
Label(root, text="Name:").grid(row=1, column=0, pady=10, sticky=tk.W)
name_entry = Entry(root)
name_entry.grid(row=1, column=1, pady=10)

# Tag Entry with Checkbuttons
Label(root, text="Tag:").grid(row=2, column=0, pady=10, sticky=tk.W)
tag_vars = []
for i, tag in enumerate(["SEBI", "CertIN", "Hippa"]):
    var = tk.IntVar()
    tag_vars.append(var)
    Checkbutton(root, text=tag, variable=var).grid(row=2, column=i+1, pady=10)

# execFile Entry
Label(root, text="execFile:").grid(row=3, column=0, pady=10, sticky=tk.W)
execFile_entry = Entry(root)
execFile_entry.grid(row=3, column=1, pady=10)

# Submit Button
submit_button = Button(root, text="Submit", command=add_entry)
submit_button.grid(row=4, column=0, columnspan=3, pady=10)

# Run the Tkinter event loop
root.mainloop()