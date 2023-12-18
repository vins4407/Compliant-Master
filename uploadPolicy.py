import tkinter as tk
from tkinter import filedialog, messagebox
import os
import zipfile
from cryptography.fernet import Fernet
import hashlib
import json
import shutil

# Use a custom key (replace with your own key)
custom_key = b'iC3NK3fUm-WfXJpu-EEUPvuhRG_FaG_czpjhKSsB4tM='
cipher = Fernet(custom_key)


def compute_file_hash(file_path, block_size=65536):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        for buffer in iter(lambda: file.read(block_size), b''):
            hasher.update(buffer)
    return hasher.hexdigest()


def encrypt_data(data, cipher):
    return cipher.encrypt(data.encode())


def decrypt_data(encrypted_data, cipher):
    return cipher.decrypt(encrypted_data).decode()


def zip_config_folder():
    config_folder_path = "config"  # Replace with the actual path to your "config" folder

    try:
        # Prompt user for the destination path to save the zip file
        destination_path = filedialog.askdirectory(title="Select Destination Folder")

        if destination_path:
            zip_file_path = os.path.join(destination_path, "config_archive.zip")
            hashes_file_path = os.path.join(config_folder_path, "hashes.json")

            # Generate hashes and create hashes.json file
            file_hashes = {}
            for root, dirs, files in os.walk(config_folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, config_folder_path)
                    file_hashes[arcname] = compute_file_hash(file_path)

            with open(hashes_file_path, 'w') as hash_file:
                json.dump(file_hashes, hash_file)

            encrypted_hashes = encrypt_data(json.dumps(file_hashes), cipher)

            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(config_folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, config_folder_path)
                        zip_file.write(file_path, arcname=arcname)
                zip_file.writestr("encrypted_hashes.bin", encrypted_hashes)

            messagebox.showinfo("Success", "Config folder zipped successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def unzip_and_verify():
    try:
        zip_file_path = filedialog.askopenfilename(title="Select Zip File", filetypes=[("Zip files", "*.zip")])

        if zip_file_path:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                encrypted_hashes_bin = zip_ref.read("encrypted_hashes.bin")
                extract_path = filedialog.askdirectory(title="Select Destination Folder to Extract")

                if extract_path:
                    decrypted_hashes_json = decrypt_data(encrypted_hashes_bin, cipher)
                    decrypted_hashes = json.loads(decrypted_hashes_json)

                    for arcname, expected_hash in decrypted_hashes.items():
                        file_path = os.path.join(extract_path, arcname)
                        if os.path.isfile(file_path):
                            computed_hash = compute_file_hash(file_path)
                            if computed_hash != expected_hash:
                                messagebox.showerror("Error", "Hash verification failed. Data integrity compromised.")
                                return

                    config_folder_path = os.path.join(extract_path, "config")
                    shutil.rmtree(config_folder_path, ignore_errors=True)

                    zip_ref.extractall(extract_path)
                    messagebox.showinfo("Success", "Zip file uploaded and config folder extracted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


window = tk.Tk()
window.title("Download and Upload Page")
window.geometry("600x600")

canvas = tk.Canvas(window, width=600, height=600, bg="white")
canvas.pack()

download_button = tk.Button(canvas, text="Download Now!", command=zip_config_folder)
download_button.place(relx=0.3, rely=0.5, anchor="center")

upload_button = tk.Button(canvas, text="Upload Now!", command=unzip_and_verify)
upload_button.place(relx=0.7, rely=0.5, anchor="center")

window.mainloop()
