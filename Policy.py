import customtkinter
from PIL import Image, ImageTk
import os
import subprocess

file_path = os.path.dirname(os.path.realpath(__file__))
print(file_path)
image_1 = customtkinter.CTkImage(Image.open(file_path + "/assets/create.png"), size=(35, 35))
image_2 = customtkinter.CTkImage(Image.open(file_path + "/assets/upload.png"), size=(40, 40))

app = customtkinter.CTk()
app.title("Policy Management")
app_width, app_height = 400, 300


screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x_position = (screen_width - app_width) // 2
y_position = (screen_height - app_height) // 2

app.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")

frame = customtkinter.CTkFrame(master=app, corner_radius=20)
frame.pack(pady=20, padx=20, fill="both", expand=True)

def create_policy_clicked():
    subprocess.run(["python3", "create_policy.py"])

button_1 = customtkinter.CTkButton(
    master=frame,
    image=image_1,
    text="Create Policy",
    corner_radius=8,
    width=200,
    height=30,
    font=("Arial", 20),
    border_spacing=10,
    command=create_policy_clicked,
)
button_1.pack(padx=20, pady=20)

button_2 = customtkinter.CTkButton(
    master=frame,
    image=image_2,
    text="Upload Policy",
    corner_radius=8,
    width=200,
    height=30,
    font=("Arial", 20),
    border_spacing=10,
)
button_2.pack(padx=20, pady=20)

app.mainloop()
