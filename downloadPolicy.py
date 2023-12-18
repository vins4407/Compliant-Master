import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import zipfile

def zip_config_folder():
    config_folder_path = "config"  # Replace with the actual path to your "config" folder

    try:
        # Prompt user for the destination path to save the zip file
        destination_path = filedialog.askdirectory(title="Select Destination Folder")

        if destination_path:
            # Create a zip file named "config_archive.zip" in the selected destination
            zip_file_path = os.path.join(destination_path, "config_archive.zip")

            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add all files and subdirectories from the Config folder to the zip archive
                for root, dirs, files in os.walk(config_folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, config_folder_path)
                        zip_file.write(file_path, arcname)

            # Display a success message
            messagebox.showinfo("Success", "Config folder zipped successfully!")
    except Exception as e:
        # Display an error message if something goes wrong
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
window = tk.Tk()
window.title("Download Page")
window.geometry("600x600")

# Create a canvas
canvas = tk.Canvas(window, width=600, height=600, bg="white")
canvas.pack()

# Create a button in the middle of the canvas
button = tk.Button(canvas, text="Download Now!", command=zip_config_folder)
button.place(relx=0.5, rely=0.5, anchor="center")

# Start the Tkinter event loop
window.mainloop()
