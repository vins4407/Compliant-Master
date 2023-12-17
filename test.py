import tkinter
import customtkinter as ctk
from tkinter import Listbox, END, MULTIPLE, messagebox

def on_submit():
    selected_items = selected_option_listbox.get(0, tkinter.END)
    print("Selected Items:", selected_items)
    show_popup()

def show_popup():
    popup = ctk.CTk()
    popup.title("Options")

    window_width = 300
    window_height = 150

    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    popup.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    label = ctk.CTkLabel(popup, text="Choose an action:", font=("Arial", 14))
    label.pack(pady=10)

    download_button = ctk.CTkButton(popup, text="Download", command=download_action, font=("Arial", 12))
    download_button.pack(side="left", padx=10)

    hardening_button = ctk.CTkButton(popup, text="Start Hardening", command=start_hardening_action, font=("Arial", 12))
    hardening_button.pack(side="right", padx=10)

    popup.mainloop()

def download_action():
    print("Download action")

def start_hardening_action():
    print("Start Hardening action")

class DragDropListbox(Listbox):
    def __init__(self, master, other_listbox, list_name, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.other_listbox = other_listbox
        self.list_name = list_name
        self.bind('<Double-Button-1>', self.on_double_left_click)
        self.configure(font=("Arial", 12), selectbackground="#3498db", selectforeground="white")

    def on_double_left_click(self, event):
        cur_index = self.nearest(event.y)
        cur_item = self.get(cur_index)
        self.delete(cur_index)
        self.other_listbox.insert(END, cur_item)

app = ctk.CTk()
app.title("Rules")
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

window_width = 580
window_height = 600

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

welcome_label = ctk.CTkLabel(app, text="Welcome Root", font=("Arial", 24))
welcome_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

logout_button = ctk.CTkButton(app, text="Back")
logout_button.grid(row=0, column=2, padx=20, pady=20, sticky="e")

main_frame = ctk.CTkFrame(app)
main_frame.grid(row=1, column=0, columnspan=3)

left_frame = ctk.CTkFrame(main_frame)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

right_frame = ctk.CTkFrame(main_frame)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

label_available = ctk.CTkLabel(left_frame, text="Available Rules", font=("Helvetica", 12))
label_available.pack(pady=5)

label_selected = ctk.CTkLabel(right_frame, text="Selected Rules", font=("Helvetica", 12))
label_selected.pack(pady=5)

available_options = ["SSH", "TOR", "USB"]

available_option_listbox = DragDropListbox(left_frame, None, "available_options", selectmode=MULTIPLE)
selected_option_listbox = DragDropListbox(right_frame, available_option_listbox, "selected_options", selectmode=MULTIPLE)
available_option_listbox.other_listbox = selected_option_listbox

for option in available_options:
    available_option_listbox.insert(END, option)

available_option_listbox.pack(expand=True, fill="both")
selected_option_listbox.pack(expand=True, fill="both")

submit_button = ctk.CTkButton(app, text="Submit", command=on_submit, font=("Helvetica", 12))
submit_button.grid(row=2, column=1, pady=10)

app.mainloop()