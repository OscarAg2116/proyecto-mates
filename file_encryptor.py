import os
from cryptography.fernet import Fernet
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from collections import deque

def generate_and_save_key(key_path: str) -> bytes:
    key = Fernet.generate_key()
    with open(key_path, 'wb') as key_file:
        key_file.write(key)
    return key

def load_key(key_path: str) -> bytes:
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"No se encontró el archivo de clave: {key_path}")
    with open(key_path, 'rb') as key_file:
        return key_file.read()

def encrypt_file(file_path: str, key: bytes):
    fernet = Fernet(key)
    encrypted_file_path = file_path + '.enc'

    print(f"Encriptando el archivo {file_path}...")

    with open(file_path, 'rb') as file:
        file_data = file.read()
        encrypted_data = fernet.encrypt(file_data)

    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    print(f'Archivo encriptado y guardado en {encrypted_file_path}')

def decrypt_file(file_path: str, key: bytes):
    fernet = Fernet(key)
    decrypted_file_path = os.path.splitext(file_path)[0]  # Elimina '.enc' del nombre del archivo

    print(f"Desencriptando el archivo {file_path}...")

    with open(file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception as e:
        print(f"Error durante la desencriptación: {str(e)}")
        return

    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

    print(f"Archivo desencriptado y guardado en {decrypted_file_path}")

def select_file(prompt: str) -> str:
    root = Tk()
    root.withdraw()
    root.iconify()  # Minimizar la ventana principal para evitar problemas con la ventana de selección
    file_path = askopenfilename(title=prompt)
    root.destroy()  # Asegúrate de destruir la ventana principal después de la selección
    return file_path

def process_queue(file_queue: deque):
    while file_queue:
        action, file_path = file_queue.popleft()
        key_path = file_path + ('.enc.key' if action == 'e' else '.key')
        if action == 'e':
            key = generate_and_save_key(key_path)
            encrypt_file(file_path, key)
        elif action == 'd':
            key = load_key(key_path)
            decrypt_file(file_path, key)
        else:
            print(f"Acción no reconocida: {action}")

if __name__ == "__main__":
    encrypt_count = input("¿Cuántos archivos deseas encriptar? ").strip()
    decrypt_count = input("¿Cuántos archivos deseas desencriptar? ").strip()

    try:
        encrypt_count = int(encrypt_count)
        decrypt_count = int(decrypt_count)

        file_queue = deque()

        for i in range(encrypt_count):
            print(f"Selecciona el archivo {i + 1} para encriptar")
            file_path = select_file(f"Selecciona el archivo {i + 1} para encriptar")
            if file_path:
                file_queue.append(('e', file_path))
            else:
                print(f'No se seleccionó ningún archivo {i + 1}')
                break

        for i in range(decrypt_count):
            print(f"Selecciona el archivo {i + 1} para desencriptar")
            file_path = select_file(f"Selecciona el archivo {i + 1} para desencriptar")
            if file_path:
                file_queue.append(('d', file_path))
            else:
                print(f'No se seleccionó ningún archivo {i + 1}')
                break

        if file_queue:
            process_queue(file_queue)
        else:
            print("No hay archivos para procesar.")
    except ValueError:
        print("Número de archivos no válido. Debe ser un número entero.")
