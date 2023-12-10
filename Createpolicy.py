import customtkinter as ctk

class MyTabView(ctk.CTkTabview):
    def __init__(self, master, checkboxes_list, **kwargs):
        super().__init__(master, **kwargs)

        tab_font = ("Arial", 16, "bold")

        self.add("All")
        self.add("Hippa")
        self.add("Scan 1")
        self.add("Scan 2")
        self.add("Scan 3")

        self.checkbox_frames = {}
        for tab_name in ["All", "Hippa", "Scan 1", "Scan 2", "Scan 3"]:
            tab_frame = self.tab(tab_name)
            label = ctk.CTkLabel(tab_frame, text=tab_name, font=tab_font)
            label.pack(pady=5)

            label.bind("<ButtonRelease-1>", lambda event, tab_name=tab_name: self.on_tab_changed(event, tab_name))

            frame = ctk.CTkFrame(master=tab_frame)
            frame.pack(fill="both", expand=True)

            checkboxes_tab = []
            for i in range(9):
                checkbox_id = f"{tab_name}_Option_{i + 1}"
                checkbox_var = ctk.IntVar()
                checkbox = ctk.CTkCheckBox(frame, text=f"Option {i + 1}", variable=checkbox_var, font=("Arial", 14))
                checkbox.grid(row=i // 3, column=i % 3, padx=10, pady=15, sticky="w")

                if tab_name == "All":
                    checkbox_var.set(1)

                elif tab_name == "Hippa" and (i + 1) in [1, 3]:
                    checkbox_var.set(1)
                elif tab_name == "Scan 1" and (i + 1) in [8, 9]:
                    checkbox_var.set(1)
                elif tab_name == "Scan 2" and (i + 1) in [1, 8]:
                    checkbox_var.set(1)
                elif tab_name == "Scan 3" and (i + 1) in [7, 9]:
                    checkbox_var.set(1)

                checkboxes_tab.append(checkbox)

            checkboxes_list.append(checkboxes_tab)
            self.checkbox_frames[tab_name] = checkboxes_tab

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        welcome_label = ctk.CTkLabel(master=self, text="Welcome Root", font=("Arial", 24))
        welcome_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        logout_button = ctk.CTkButton(master=self, text="Logout", command=self.logout, font=("Arial", 14))
        logout_button.grid(row=0, column=1, padx=20, pady=20, sticky="e", columnspan=2)

        checkboxes = []
        self.tab_view = MyTabView(master=self, checkboxes_list=checkboxes)
        self.tab_view.grid(row=1, column=0, padx=20, pady=20, sticky="nsew", columnspan=3)

        submit_button = ctk.CTkButton(master=self, text="Submit", command=self.submit, font=("Arial", 14))
        submit_button.grid(row=2, column=0, padx=20, pady=10, columnspan=3)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = 500
        window_height = 500

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def logout(self):
        print("Logout clicked")

    def submit(self):
        print("Form submitted")

    def on_tab_changed(self, event, tab_name):
        current_tab_name = tab_name

        for tab_frame_name, checkbox_frame in self.checkbox_frames.items():
            for checkbox in checkbox_frame:
                checkbox_var = checkbox.var()

                if current_tab_name == "Hippa":
                    checkbox.grid()

                else:
                    if "_en" not in checkbox.tag:
                        checkbox.grid_remove()
                    else:
                        checkbox.grid()

if __name__ == "__main__":
    app = App()
    app.mainloop()
