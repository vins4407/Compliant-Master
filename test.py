import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import customtkinter

customtkinter.set_default_color_theme("green")

def logout():
    print("Logout clicked")
    app.destroy()

def button_click(responsibility):
    hide_all_screens()
    if responsibility == "Responsibility 1":
        show_screen_policy()
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

def hide_all_screens():
    for widget in app.winfo_children():
        widget.grid_forget()

def show_screen_policy():
    hide_all_screens()  
    frame_policy.grid(row=1, column=0, padx=160, pady=20, rowspan=3, columnspan=3, sticky="nsew")

app = ctk.CTk()
app.title("Welcome Root")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

window_width = 580
window_height = 600

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Background
pil_image = Image.open("./assets/jojo.jpg")
ctk_image = ctk.CTkImage(pil_image)
background_label = ctk.CTkLabel(app, image=ctk_image, text="", compound="center")  # Set text to an empty string and use "center" compound
background_label.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")




frame_policy = ctk.CTkFrame(master=app, corner_radius=20)

button_1 = ctk.CTkButton(
    master=frame_policy,
    text="Create Policy",
    corner_radius=8,
    width=200,
    height=30,
    font=("Arial", 20),
    border_spacing=10,
    command=lambda: subprocess.run(["python", "Createpolicy.py"]),
)
button_1.grid(row=1, column=0, padx=20, pady=20)

button_2 = ctk.CTkButton(
    master=frame_policy,
    text="Upload Policy",
    corner_radius=8,
    width=200,
    height=30,
    font=("Arial", 20),
    border_spacing=10,
)
button_2.grid(row=2, column=0, padx=20, pady=20)

image_path = "./assets/p1.png" 
image = Image.open(image_path)
image = ImageTk.PhotoImage(image)

image_label = ctk.CTkLabel(frame_policy, image=image)
image_label.grid(row=4, column=0, padx=0, pady=20)

welcome_label = ctk.CTkLabel(app, text="Welcome Root", font=("Arial", 24))
welcome_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

logout_button = ctk.CTkButton(app, text="Logout", command=logout)
logout_button.grid(row=0, column=2, padx=20, pady=20, sticky="e")

buttons_info = [
    {"name": "Start Hardening", "responsibility": "Responsibility 1"},
    {"name": "Check Compliant Status", "responsibility": "Responsibility 2"},
    {"name": "Reports", "responsibility": "Responsibility 3"},
    {"name": "Roll back", "responsibility": "Responsibility 4"},
    {"name": "Schedule task", "responsibility": "Responsibility 5"},
    {"name": "Full Scan", "responsibility": "Responsibility 6"},
]

for i, button_info in enumerate(buttons_info):
    button = ctk.CTkButton(app, text=button_info["name"], width=120, height=120, command=lambda resp=button_info["responsibility"]: button_click(resp))
    button.grid(row=i // 3 + 1, column=i % 3, padx=20, pady=20)


additional_button = ctk.CTkButton(app, text="System Info", command=lambda: button_click("Additional Responsibility"), width=445, height=110)
additional_button.grid(row=len(buttons_info) // 3 + 2, column=0, padx=20, pady=20, columnspan=3)

app.mainloop()
