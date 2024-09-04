import os
import numpy as np
import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from collections import deque

def file_to_video(file_path, frame_size=(640, 480), fps=30):
    print(f"Abriendo el archivo {file_path}...")

    with open(file_path, 'rb') as file:
        data = file.read()

    frame_bytes = frame_size[0] * frame_size[1] * 3  # RGB
    padding_size = (frame_bytes - len(data) % frame_bytes) % frame_bytes
    data_padded = data + b'\x00' * padding_size

    data_array = np.frombuffer(data_padded, dtype=np.uint8)
    frames = data_array.reshape(-1, frame_size[1], frame_size[0], 3)

    video_path = file_path + '.avi'
    print(f"Creando el archivo de video {video_path}...")

    fourcc = cv2.VideoWriter_fourcc(*'FFV1')  # Códec sin pérdida
    out = cv2.VideoWriter(video_path, fourcc, fps, frame_size)

    for frame in frames:
        out.write(frame)

    out.release()
    print(f"Archivo de video guardado en {video_path}")

def video_to_file(video_path, frame_size=(640, 480)):
    print(f"Abriendo el archivo de video {video_path}...")

    cap = cv2.VideoCapture(video_path)
    data = bytearray()
    frame_bytes = frame_size[0] * frame_size[1] * 3

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        data.extend(frame.flatten())

    cap.release()

    data_array = np.array(data, dtype=np.uint8)
    data_trimmed = data_array.tobytes().rstrip(b'\x00')

    output_file = os.path.splitext(video_path)[0]
    print(f"Guardando el archivo recuperado en {output_file}...")

    with open(output_file, 'wb') as file:
        file.write(data_trimmed)

    print(f"Archivo recuperado guardado en {output_file}")

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
        if action == '1':
            file_to_video(file_path)
        elif action == '2':
            video_to_file(file_path)
        else:
            print(f"Acción no reconocida: {action}")

if __name__ == "__main__":
    to_video_count = input("¿Cuántos archivos deseas convertir a video? ").strip()
    to_file_count = input("¿Cuántos archivos de video deseas convertir a archivo? ").strip()

    try:
        to_video_count = int(to_video_count)
        to_file_count = int(to_file_count)

        file_queue = deque()

        for i in range(to_video_count):
            print(f"Selecciona el archivo {i + 1} para convertir a video")
            file_path = select_file(f"Selecciona el archivo {i + 1} para convertir a video")
            if file_path:
                file_queue.append(('1', file_path))
            else:
                print(f'No se seleccionó ningún archivo {i + 1}')
                break

        for i in range(to_file_count):
            print(f"Selecciona el archivo {i + 1} para convertir a archivo")
            file_path = select_file(f"Selecciona el archivo {i + 1} para convertir a archivo")
            if file_path:
                file_queue.append(('2', file_path))
            else:
                print(f'No se seleccionó ningún archivo {i + 1}')
                break

        if file_queue:
            process_queue(file_queue)
        else:
            print("No hay archivos para procesar.")
    except ValueError:
        print("Número de archivos no válido. Debe ser un número entero.")
