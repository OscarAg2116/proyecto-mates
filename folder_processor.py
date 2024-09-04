import os
import shutil
import zipfile
import binascii  # Importar binascii para convertir a hexadecimal
from tkinter import Tk
from tkinter.filedialog import askdirectory

def select_folder() -> str:
    root = Tk()
    root.withdraw()
    folder_path = askdirectory(title="Selecciona la carpeta que quieres comprimir")
    root.destroy()
    return folder_path

def generate_password_from_folder_name(folder_name: str) -> str:
    return folder_name.replace(" ", "_")  # Se utiliza el nombre de la carpeta como contraseña, reemplazando espacios con guiones bajos

def rename_folder_to_hex(folder_path: str):
    folder_name = os.path.basename(folder_path)
    folder_dir = os.path.dirname(folder_path)
    folder_name_hex = binascii.hexlify(folder_name.encode()).decode()
    new_folder_path = os.path.join(folder_dir, folder_name_hex)
    os.rename(folder_path, new_folder_path)
    return new_folder_path

def compress_folder_to_multiple_zips(folder_path: str, output_path: str, password: str, max_files_per_zip: int = 50):
    folder_name = os.path.basename(folder_path)
    part_num = 1
    file_count = 0
    
    zip_filename = os.path.join(output_path, f"{folder_name}_part{part_num:03d}.zip")
    zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file_count >= max_files_per_zip:
                zipf.close()
                part_num += 1
                zip_filename = os.path.join(output_path, f"{folder_name}_part{part_num:03d}.zip")
                zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
                file_count = 0
            
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, folder_path)
            zipf.write(file_path, arcname)
            file_count += 1
    
    zipf.close()

def delete_folder(folder_path: str):
    shutil.rmtree(folder_path)

if __name__ == "__main__":
    folder_path = select_folder()
    
    if folder_path:
        password = generate_password_from_folder_name(os.path.basename(folder_path))
        print(f"Contraseña generada: {password}")
        
        renamed_folder_path = rename_folder_to_hex(folder_path)
        output_path = os.path.dirname(renamed_folder_path)
        
        compress_folder_to_multiple_zips(renamed_folder_path, output_path, password)
        
        delete_folder(renamed_folder_path)
        print("Carpeta comprimida y eliminada con éxito.")
    else:
        print("No se seleccionó ninguna carpeta.")
