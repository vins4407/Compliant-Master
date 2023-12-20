import customtkinter as ctk
import json
def set_checkboxes(tab_name, i, checkbox_var,json_data):
    # Sample JSON data structure

    # Assuming tab_name is present in the JSON data
    if tab_name in json_data:
        # Check if (i + 1) is in the corresponding list for the tab_name
        if (i + 1) in [item["value"] for item in json_data[tab_name]]:
            checkbox_var.set(1)



class MyTabView(ctk.CTkTabview):
    def __init__(self, master, checkboxes_list, json_data, **kwargs):
        super().__init__(master, **kwargs)
        self.json_data = json_data

        tab_font = ("Arial", 16, "bold")
        self.add("All")
        self.add("CISF")
        self.add("Hippa")
       
        self.checkbox_frames = {}
        for tab_name in ["All","CISF","Hippa"]:
            tab_frame = self.tab(tab_name)
            label = ctk.CTkLabel(tab_frame, text=tab_name, font=tab_font)
            label.pack(pady=5)

            label.bind("<ButtonRelease-1>", lambda event, tab_name=tab_name: self.on_tab_changed(event, tab_name))

            frame = ctk.CTkFrame(master=tab_frame)
            frame.pack(fill="both", expand=True)

            checkboxes_tab = []
            for key, policy in self.json_data.items():
                print(key)
                print(policy)
                tags = policy.get("tag", [])
                print(tags)
                print(tab_name)
                print(policy["name"])
                if tab_name in tags:
                    checkbox_var = ctk.IntVar()
                    checkbox = ctk.CTkCheckBox(frame, text=policy["name"], variable=checkbox_var, font=("Arial", 14))
                    checkbox.grid(row=int(key) // 3, column=int(key) % 3, padx=10, pady=15, sticky="w")
                    checkboxes_tab.append(checkbox_var)
                else:
                    checkbox_var = ctk.IntVar()
                    checkbox = ctk.CTkCheckBox(frame, text=policy["name"], variable=checkbox_var, font=("Arial", 14))
                    checkbox.grid(row=int(key) // 3, column=int(key) % 3, padx=10, pady=15, sticky="w")
                    checkboxes_tab.append(checkbox_var)



            #     # Check if the policy has tags CISF or Hippa


            # for i, item in enumerate(json_data.get(tab_name, [])):
            #     checkbox_var = ctk.IntVar()
            #     print(i)
            #     print(item)

            #     checkbox = ctk.CTkCheckBox(frame, text=item["name"], variable=checkbox_var, font=("Arial", 14))
            #     checkbox.grid(row=i // 3, column=i % 3, padx=10, pady=15, sticky="w")
            #     checkboxes_tab.append(checkbox_var)

            self.checkbox_frames[tab_name] = checkboxes_tab

        # Set checkboxes initially when the view is created
        self.set_checkboxes("CISF")
        self.set_checkboxes("Hippa")
        

    def set_checkboxes(self, tab_name):
        checkboxes_tab = self.checkbox_frames.get(tab_name, [])

        for i, checkbox_var in enumerate(checkboxes_tab):
            set_checkboxes(tab_name, i, checkbox_var,json_data)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

     
        def load_data(file_path):
            try:
                with open(file_path) as f:
                    return json.load(f)
            except FileNotFoundError:
                print(f"File not found: {file_path}")
                return {}


        json_data  = load_data('data.json')


        welcome_label = ctk.CTkLabel(master=self, text="Welcome Root", font=("Arial", 24))
        welcome_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        logout_button = ctk.CTkButton(master=self, text="Logout", command=self.logout, font=("Arial", 14))
        logout_button.grid(row=0, column=1, padx=20, pady=20, sticky="e", columnspan=2)

        # OptionMenu
        self.optionmenu_var = ctk.StringVar(value="Level 1")  # set initial value

        def optionmenu_callback(choice):
            set_checkboxes("All",)
            print("OptionMenu selected:", choice)

        combobox = ctk.CTkOptionMenu(master=self,
                                     values=["Level 1","Level 2"],
                                     command=optionmenu_callback,
                                     variable=self.optionmenu_var)
        combobox.grid(row=1, column=0, padx=220, pady=10, sticky="w", columnspan=3)

        checkboxes = []
        self.tab_view = MyTabView(master=self, checkboxes_list=checkboxes, json_data=json_data)
        self.tab_view.grid(row=2, column=0, padx=20, pady=20, sticky="nsew", columnspan=3)

        submit_button = ctk.CTkButton(master=self, text="Submit", command=self.submit, font=("Arial", 14))
        submit_button.grid(row=3, column=0, padx=20, pady=10, columnspan=3)

        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = 800
        window_height = 800

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def logout(self):
        print("Logout clicked")


    def submit(self):
        selected_option = self.optionmenu_var.get()
        print("Selected Option:", selected_option)
        print("Form submitted")

    def on_tab_changed(self, event, tab_name):
        self.tab_view.set_checkboxes(tab_name)

if __name__ == "__main__":
    app = App()
    app.mainloop()