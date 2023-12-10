import subprocess
import customtkinter as ctk
from PIL import Image, ImageTk
import customtkinter

customtkinter.set_default_color_theme("green")

def logout():
    print("Logout clicked")

def button_click(responsibility):
    if responsibility == "Responsibility 1":
        subprocess.run(["python", "Policy.py"])
    elif responsibility == "Responsibility 2":
        print("Check Compliant Status clicked")
    elif responsibility == "Responsibility 3":
        print("Reports clicked")
    elif responsibility == "Responsibility 4":
        print("Roll back clicked")
    elif responsibility == "Responsibility 5":
        print("Schedule task clicked")
    elif responsibility == "Responsibility 6":
        print("Full Scan clicked")
    else:
        print(f"Additional Responsibility clicked: {responsibility}")

    app.destroy()

app = ctk.CTk()
app.title("Welcome Root")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

window_width = 580
window_height = 600

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

pil_image = Image.open("./assets/jojo.jpg")
background_image = ImageTk.PhotoImage(pil_image)

ctk_image = ctk.CTkImage(pil_image)

background_label = ctk.CTkLabel(app, image=ctk_image)
background_label.place(relwidth=1, relheight=1)

welcome_label = ctk.CTkLabel(app, text="Welcome Root", font=("Arial", 24))
welcome_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

logout_button = ctk.CTkButton(app, text="Logout", command=logout)
logout_button.grid(row=0, column=1, padx=20, pady=20, sticky="e", columnspan=2)

buttons_info = [
    {"name": "Start Hardining ", "responsibility": "Responsibility 1"},
    {"name": "Check Compliant Status", "responsibility": "Responsibility 2"},
    {"name": "Reports ", "responsibility": "Responsibility 3"},
    {"name": "Roll back ", "responsibility": "Responsibility 4"},
    {"name": "Schedule task ", "responsibility": "Responsibility 5"},
    {"name": "Full Scan", "responsibility": "Responsibility 6"},
]

for i, button_info in enumerate(buttons_info):
    button = ctk.CTkButton(app, text=button_info["name"], width=120, height=120, command=lambda resp=button_info["responsibility"]: button_click(resp))
    button.grid(row=i // 3 + 1, column=i % 3, padx=20, pady=20)

additional_button = ctk.CTkButton(app, text="System Info ", command=lambda: button_click("Additional Responsibility"), width=445, height=110)
additional_button.grid(row=len(buttons_info) // 3 + 2, column=0, padx=20, pady=20, columnspan=3)

app.mainloop()
