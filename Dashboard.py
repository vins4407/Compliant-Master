import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import customtkinter
import sys
from helpers import *

customtkinter.set_default_color_theme("green")
app = ctk.CTk()
app.title("Welcome Root")
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

window_width = 600
window_height = 600


x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")


def logout():
    print("Logout clicked")
    app.destroy()

def go_back_to_dashboard():
    hide_all_screens()  
    main_frame.grid(row=0, column=0, padx=19, pady=20, rowspan=2, columnspan=2, sticky="nsew")

    
# Reveal the dashboard content here

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
    Options_frame.grid(row=2, column=0, padx=160, pady=20, rowspan=3, columnspan=3, sticky="nsew")
    app.update()

def create_policy():
    app.destroy()
    subprocess.run(["python3", "create_policy.py"])
    app.destroy()

# Frame-Main
main_frame = ctk.CTkFrame(app, corner_radius=20)
main_frame.grid(row=0, column=0, sticky="nsew")


# Background
pil_image = Image.open("./assets/jojo.jpg")
ctk_image = ctk.CTkImage(pil_image)
background_label = ctk.CTkLabel(main_frame, image=ctk_image, text="", compound="center")
background_label.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")

welcome_label = ctk.CTkLabel(main_frame, text="Welcome Root", font=("Arial", 24))
welcome_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

logout_button = ctk.CTkButton(main_frame, text="Logout", command=logout)
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
    button = ctk.CTkButton(main_frame, text=button_info["name"], width=120, height=120, command=lambda resp=button_info["responsibility"]: button_click(resp))
    button.grid(row=i // 3 + 1, column=i % 3, padx=20, pady=20)

additional_button = ctk.CTkButton(main_frame, text="System Info", command=lambda: button_click("Additional Responsibility"), width=445, height=110)
additional_button.grid(row=len(buttons_info) // 3 + 2, column=0, padx=20, pady=20, columnspan=3)

#frames-Option

Options_frame = ctk.CTkFrame(master=app, corner_radius=20)

file_path = os.path.dirname(os.path.realpath(__file__))
print(file_path)
image_1 = customtkinter.CTkImage(Image.open(file_path + "/assets/create.png"), size=(35, 35))
image_2 = customtkinter.CTkImage(Image.open(file_path + "/assets/upload.png"), size=(40, 40))


back_button = ctk.CTkButton(
    master=Options_frame,
    text="Back to Dashboard",
    corner_radius=8,
    width=200,
    height=30,
    font=("Arial", 20),
    border_spacing=10,
)
back_button.grid(row=0, column=0, padx=20, pady=20)
back_button.configure(command=go_back_to_dashboard)


button_1 = ctk.CTkButton(
    master=Options_frame,
    image=image_1,
    text="Create Policy",
    corner_radius=8,
    width=200,
    height=30,
    font=("Arial", 20),
    border_spacing=10,
    command=create_policy,
)
button_1.grid(row=1, column=0, padx=20, pady=20)

button_2 = ctk.CTkButton(
    master=Options_frame,
    image=image_2,
    text="Upload Policy",
    corner_radius=8,
    width=200,
    height=30,
    font=("Arial", 20),
    border_spacing=10,
    command=unzip_and_verify
)
button_2.grid(row=2, column=0, padx=20, pady=20)



if __name__ == "__main__":
    # Check if the command-line argument is provided
    if "--show-frame" in sys.argv and "Options" in sys.argv:
        show_screen_policy()  # Show the Options frame
    else:
        # Your existing main loop code here
        app.mainloop()


app.mainloop()
