import subprocess
import tkinter as tk
import customtkinter
from PIL import Image
from PIL import ImageTk
import os
import getpass


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()
app.title('Login')

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

window_width = 600
window_height = 600

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

def button_function():
    username = entry1.get()  # Get the entered username
    password = entry2.get()  # Get the entered password
    
        # Use sudo to execute a command that requires root privileges
    command = ["sudo", "-S", "-u", "root", "ls"]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate(input=password.encode())
        
    if process.returncode == 0:
            app.destroy()
            # If the command succeeds, the username and password are correct
            print("Root user detected. Proceeding with the Dashboard.")
            subprocess.run(["python3", "Dashboard.py"])
            app.destroy()



img1 = ImageTk.PhotoImage(Image.open("./assets/jojo.jpg"))
l1 = customtkinter.CTkLabel(master=app, image=img1)
l1.pack()

frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

l2 = customtkinter.CTkLabel(master=frame, text="PLease Verify you're Root", font=('Century Gothic', 20))
l2.place(x=50, y=45)

entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
entry1.place(x=50, y=110)

entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
entry2.place(x=50, y=165)

l3 = customtkinter.CTkLabel(master=frame, text="contact admin ?", font=('Century Gothic', 12))
l3.place(x=155, y=195)

button1 = customtkinter.CTkButton(master=frame, width=220, text="sumbit", command=button_function, corner_radius=6)
button1.place(x=50, y=240)

app.mainloop()
