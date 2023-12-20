import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import subprocess

def get_existing_rules():
    try:
        result = subprocess.run(['sudo','iptables', '-L', '-n', '--line-numbers'], capture_output=True, text=True)
        existing_rules = result.stdout
        return existing_rules
    except Exception as e:
        return f"Error retrieving existing rules: {str(e)}"

def remove_existing_rules():
    try:
        subprocess.run(['sudo','iptables', '-F'])
        return "Existing rules removed successfully."
    except Exception as e:
        return f"Error removing existing rules: {str(e)}"

def generate_script(ports):
    script_content = f"""
#!/bin/bash

echo ""

# Allow specified ports
IFS=',' read -ra PORTS <<< "{ports}"
for port in "${{PORTS[@]}}"; do
    iptables -A INPUT -p tcp -m tcp --dport $port -m state --state NEW,ESTABLISHED -j ACCEPT
done

# Allow loopback interface
iptables -A INPUT -i lo -j ACCEPT

# Drop all other incoming traffic
iptables -A INPUT -j DROP
"""

    return script_content

def on_next():
    entered_ports = port_entry.get()
    if not entered_ports:
        messagebox.showwarning("Warning", "Please enter ports.")
        return

    script_content = generate_script(entered_ports)
    script_text.config(state=tk.NORMAL)
    script_text.delete('1.0', tk.END)
    script_text.insert(tk.END, script_content)
    script_text.config(state=tk.DISABLED)

    existing_rules_text.delete('1.0', tk.END)
    existing_rules_text.insert(tk.END, get_existing_rules())

    notebook.select(1)  # Select the second page

def on_download_script():
    file_path = filedialog.asksaveasfilename(defaultextension=".sh", filetypes=[("Shell Script", "*.sh")])
    if file_path:
        script_content = generate_script(port_entry.get())
        with open(file_path, 'w') as script_file:
            script_file.write(script_content)
        messagebox.showinfo("Download Script", "Firewall script downloaded successfully!")

def on_harden_now():
    script_content = generate_script(port_entry.get())
    with open('firewall_script.sh', 'w') as script_file:
        script_file.write(script_content)
    messagebox.showinfo("Harden Now", "Firewall rules applied successfully!")

def on_remove_rules():
    result = remove_existing_rules()
    messagebox.showinfo("Remove Existing Rules", result)
    existing_rules_text.delete('1.0', tk.END)
    existing_rules_text.insert(tk.END, get_existing_rules())

root = tk.Tk()
root.title("Firewall Configuration")
root.geometry("800x600")  # Set a larger size

# Page 1
notebook = ttk.Notebook(root)

page1 = tk.Frame(notebook)
notebook.add(page1, text='Firewall Configuration')

tk.Label(page1, text="Existing iptables rules:").pack(pady=10)

existing_rules_text = tk.Text(page1, height=10, width=80, state=tk.NORMAL)
existing_rules_text.pack(pady=10)

remove_rules_button = tk.Button(page1, text="Remove Existing Rules", command=on_remove_rules)
remove_rules_button.pack(pady=10)

# Page 2
page2 = tk.Frame(notebook)
notebook.add(page2, text='Configure Firewall')

tk.Label(page2, text="Enter ports (comma-separated):").pack(pady=10)

port_entry = tk.Entry(page2)
port_entry.pack(pady=10)

next_button = tk.Button(page2, text="Next", command=on_next)
next_button.pack(pady=10)

# Page 3
page3 = tk.Frame(notebook)
notebook.add(page3, text='Actions')

script_text = tk.Text(page3, height=10, width=80, state=tk.DISABLED)
script_text.pack(pady=10)

download_button = tk.Button(page3, text="Download Script", command=on_download_script)
download_button.pack(pady=10)

harden_button = tk.Button(page3, text="Harden Now", command=on_harden_now)
harden_button.pack(pady=10)

notebook.pack(expand=1, fill="both")

# Initial display of existing rules
existing_rules_text.insert(tk.END, get_existing_rules())

root.mainloop()
