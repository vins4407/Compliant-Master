import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

class CustomBox(tk.Canvas):
    def __init__(self, master, index, name, exec_file, is_special_case, callback):
        super().__init__(master, width=150, height=60, bg='white', highlightthickness=0)
        self.index = index
        self.name = name
        self.exec_file = exec_file
        self.is_special_case = is_special_case
        self.selected = False
        self.create_rectangle(5, 5, 145, 55, outline='black', width=2)
        self.create_text(75, 30, text=name, width=140)

        self.info_button = tk.Button(self, text="i", command=self.show_info, font=("Arial", 8, "bold"))
        if self.is_special_case == 'yes':
            self.info_button.place(relx=1, rely=0, anchor="ne")

        self.bind("<Button-1>", self.toggle_color)
        self.callback = callback

    def toggle_color(self, event):
        self.selected = not self.selected
        self.set_color()
        self.callback(self)

    def set_color(self):
        if self.selected:
            self.configure(bg='green')
        else:
            self.configure(bg='white')

    def show_info(self):
        if self.is_special_case == 'yes':
            messagebox.showinfo("Box Information", f"This is a special case: {self.name}")
            self.info_button.place(relx=1, rely=0, anchor="ne")

        else:
            messagebox.showinfo("Box Information", f"No special information for: {self.name}")

class GUI:
    def __init__(self, master, data):
        self.master = master
        self.data = data
        self.custom_boxes = []
        self.selected_objects = []
        self.filtered_data = data

        filter_frame = ttk.Frame(master)
        filter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.tag_var = tk.StringVar()
        self.tag_var.set("All")

        tag_label = ttk.Label(filter_frame, text="Select Tag:")
        tag_label.grid(row=0, column=0, padx=5, pady=5)

        tag_combobox = ttk.Combobox(filter_frame, textvariable=self.tag_var, values=["All"] + list(set(tag for details in data.values() for tag in details["tag"])))
        tag_combobox.grid(row=0, column=1, padx=5, pady=5)

        filter_button = tk.Button(filter_frame, text="Apply Filter", command=self.apply_filter)
        filter_button.grid(row=0, column=2, padx=5, pady=5)

        select_all_button = tk.Button(filter_frame, text="Select All", command=self.select_all)
        select_all_button.grid(row=0, column=3, padx=5, pady=5)

        deselect_all_button = tk.Button(filter_frame, text="Deselect All", command=self.deselect_all)
        deselect_all_button.grid(row=0, column=4, padx=5, pady=5)

        self.canvas_frame = ttk.Frame(master)
        self.canvas_frame.grid(row=1, column=0, padx=10, pady=10)

        for index, details in data.items():
            custom_box = CustomBox(self.canvas_frame, index, details["name"], details["execFile"], details.get("isSpecialCase", False), self.on_box_click)
            self.custom_boxes.append(custom_box)
            custom_box.grid(row=len(self.custom_boxes)//3, column=len(self.custom_boxes)%3, padx=10, pady=10)

        submit_button = tk.Button(master, text='Submit', command=self.submit)
        submit_button.grid(row=2, column=0, pady=10)

        self.exec_files = []

    def on_box_click(self, clicked_box):
        if clicked_box.selected:
            self.selected_objects.append(clicked_box.name)
            self.exec_files.append(clicked_box.exec_file)
        else:
            self.selected_objects.remove(clicked_box.name)
            self.exec_files.remove(clicked_box.exec_file)

    def apply_filter(self):
        selected_tag = self.tag_var.get()
        if selected_tag == "All":
            self.filtered_data = self.data
        else:
            self.filtered_data = {index: details for index, details in self.data.items() if selected_tag in details["tag"]}
        
        self.refresh_boxes()

    def refresh_boxes(self):
        for box in self.custom_boxes:
            box.destroy()

        for index, details in self.filtered_data.items():
            custom_box = CustomBox(self.canvas_frame, index, details["name"], details["execFile"], details.get("isSpecialCase", False), self.on_box_click)
            self.custom_boxes.append(custom_box)
            custom_box.grid(row=len(self.custom_boxes)//3, column=len(self.custom_boxes)%3, padx=10, pady=10)

    def select_all(self):
        for box in self.custom_boxes:
            box.selected = True
            box.set_color()
            self.on_box_click(box)

    def deselect_all(self):
        for box in self.custom_boxes:
            box.selected = False
            box.set_color()
            self.on_box_click(box)

    def submit(self):
        print(f"Selected objects: {self.selected_objects}")
        print(f"Selected exec files: {self.exec_files}")

def main():
    # Load data from JSON file
    with open("data.json", "r") as json_file:
        data = json.load(json_file)

    root = tk.Tk()
    root.title("Custom Color Boxes Selector")

    gui = GUI(root, data)

    root.mainloop()

if __name__ == "__main__":
    main()
