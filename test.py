import customtkinter as ctk
import os
import time
import subprocess  # Added subprocess module for cross-platform file opening

class BackupRollbackApp(ctk.CTk):
    def __init__(self, directory_path):
        super().__init__()

        self.directory_path = directory_path

        # Set the title in the middle
        title_label = ctk.CTkLabel(master=self, text="Backup and RollBack", font=("Arial", 24))
        title_label.grid(row=0, column=0, columnspan=3, pady=0)

        # Create a 5x3 table with labels and buttons
        labels = ["File Name", "Time", "Button"]
        for col, label_text in enumerate(labels):
            label = ctk.CTkLabel(master=self, text=label_text, font=("Arial", 16, "bold"))
            label.grid(row=1, column=col, padx=10, pady=10)

        # Read .txt filenames from the specified directory and display them in the "File Name" column
        file_data = self.get_file_data()
        for row, (file_name, modification_time) in enumerate(file_data, start=2):
            file_label = ctk.CTkLabel(master=self, text=file_name, font=("Arial", 14))
            file_label.grid(row=row, column=0, padx=10, pady=15, sticky="w")

            time_label = ctk.CTkLabel(master=self, text=modification_time, font=("Arial", 14))
            time_label.grid(row=row, column=1, padx=10, pady=15, sticky="w")

            button = ctk.CTkButton(master=self, text=f"Open {row - 1}", command=lambda row=row: self.button_action(row))
            button.grid(row=row, column=2, padx=10, pady=15, sticky="e")

        # Configure column weights
        for col in range(3):
            self.columnconfigure(col, weight=1)

        self.rowconfigure(0, weight=1)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = 600
        window_height = 500

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def get_file_data(self):
        try:
            file_data = []
            # List all files in the specified directory and filter only .txt files
            txt_files = [file for file in os.listdir(self.directory_path) if file.endswith(".txt")]
            for file_name in txt_files:
                file_path = os.path.join(self.directory_path, file_name)
                modification_time = time.ctime(os.path.getmtime(file_path))
                file_data.append((file_name, modification_time))
            return file_data
        except Exception as e:
            print(f"Error: {e}")
            return []

    def button_action(self, row):
        file_name = self.get_file_data()[row - 2][0]
        self.open_file(file_name)

    def open_file(self, file_name):
        try:
            # Get the file path based on the file name
            file_path = os.path.join(self.directory_path, file_name)

            # Open the file with the default associated program
            subprocess.run(["xdg-open", file_path])
        except Exception as e:
            print(f"Error opening file: {e}")

if __name__ == "__main__":
    # Specify the path to the directory containing .txt files
    directory_path = "Backup&Rollback"

    app = BackupRollbackApp(directory_path)
    app.mainloop()