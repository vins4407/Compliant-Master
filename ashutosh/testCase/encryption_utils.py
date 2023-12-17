# encryption_utils.py
from cryptography.fernet import Fernet


def encrypt(data):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(data)
    return key + cipher_text


def save_to_file(data, file_path):
    with open(file_path, 'wb') as f:
        f.write(data)
