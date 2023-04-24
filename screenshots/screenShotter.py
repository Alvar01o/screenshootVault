import cv2
import numpy as np
import tkinter as tk
import os
import socket
import struct
import progressbar
from dotenv import load_dotenv
from PIL import Image, ImageTk, ImageGrab
from datetime import datetime 
from io import BytesIO

# Variables globales
x1, y1, x2, y2 = 0, 0, 0, 0
drawing = False
screenshot = None
screenshot_window = None
canvas = None
mode = "select"
last_image_saved = None
root = None
ip = ''
port = ''
API_KEY = os.getenv('API_KEY')


def save_in_remote_storage():
    global screenshot_window, root
    screenshot_window.withdraw()
    root.deiconify()
    send_image()

def calculate_buffer_size(image_size_bytes): 
    # Definir los límites del tamaño del buffer en bytes
    MIN_BUFFER_SIZE = 1024       # 1 KB
    MAX_BUFFER_SIZE = 32768  # 32 KB

    # Establecer un factor de relación entre el tamaño del buffer y el tamaño de la imagen
    BUFFER_SIZE_FACTOR = 0.05    # Por ejemplo, 5% del tamaño de la imagen
    
    # Calcular el tamaño del buffer en función del tamaño de la imagen y el factor de relación
    buffer_size = int(image_size_bytes * BUFFER_SIZE_FACTOR)
    
    # Asegurar que el tamaño del buffer esté dentro de los límites permitidos
    buffer_size = max(MIN_BUFFER_SIZE, buffer_size)
    buffer_size = min(MAX_BUFFER_SIZE, buffer_size)
    
    return buffer_size


def send_image():
    global last_image_saved, ip, port
    # Abrir la imagen y convertirla en bytes
    img = Image.open(last_image_saved)
    buf = BytesIO()
    img.save(buf, format='PNG')
    img_bytes = buf.getvalue()

    # Crear un socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    file_len = len(img_bytes)
    buffer_size = calculate_buffer_size(file_len)

    # Enviar el nombre del archivo como un string
    print('img name :'+ last_image_saved)
    sock.sendto(last_image_saved.encode('utf-8'), (ip, port))

    # Enviar el tamaño de la imagen como un entero (4 bytes)
    sock.sendto(struct.pack('<L', file_len), (ip, port))

    bar = progressbar.ProgressBar(max_value=file_len)

    # Enviar la imagen en paquetes de 4096 bytes
    for i in range(0, len(img_bytes), buffer_size):
        sock.sendto(img_bytes[i:i+buffer_size], (ip, port))
        bar.update(i)
    # Cerrar el socket
    bar.finish()
    sock.close()


def capture_screenshot():
    global screenshot
    screenshot = ImageGrab.grab()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def zoom_in():
    global screenshot
    height, width = screenshot.shape[:2]
    screenshot = cv2.resize(screenshot, (int(width * 1.2), int(height * 1.2)), interpolation=cv2.INTER_LINEAR)
    update_canvas(screenshot)

def zoom_out():
    global screenshot
    height, width = screenshot.shape[:2]
    screenshot = cv2.resize(screenshot, (int(width * 0.8), int(height * 0.8)), interpolation=cv2.INTER_LINEAR)
    update_canvas(screenshot)

def send_file():
    send_image()
    
def close_window():
    root.destroy()
    
def generate_file_name():
    d = datetime.today()
    return d.strftime("%d_%m_%Y-%H-%M-%S") + "_screenshot.png"

def on_mouse_click(event):
    global x1, y1, x2, y2, drawing, last_image_saved, screenshot

    if event.type == tk.EventType.ButtonPress:
        x1, y1 = event.x, event.y
        drawing = True

    elif event.type == tk.EventType.ButtonRelease:
        x2, y2 = event.x, event.y
        drawing = False

        if mode == "select":
            cropped_screenshot = screenshot[y1:y2, x1:x2]
            last_image_saved = generate_file_name()
            if not cropped_screenshot is None:
                cv2.imwrite(last_image_saved, cropped_screenshot)
            else:
                print("La imagen está vacía")

def on_mouse_move(event):
    global x1, y1, x2, y2, screenshot

    if drawing:
        x2, y2 = event.x, event.y
        img_copy = np.copy(screenshot)

        if mode == "select":
            cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 0, 255), 2)
        elif mode == "draw":
            cv2.line(img_copy, (x1, y1), (x2, y2), (0, 255, 255), 2)  # Líneas amarillas
            screenshot = img_copy
            x1, y1 = x2, y2
        update_canvas(img_copy)

def update_canvas(img):
    global canvas
    photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    canvas.image = photo

def toggle_mode():
    global mode
    mode = "draw" if mode == "select" else "select"

def open_screenshot_window():
    global screenshot, canvas, screenshot_window, root
    
    screenshot_window = tk.Toplevel(root)
    root.withdraw()
    screenshot_window.deiconify()

    screenshot_window.title("Captura de pantalla")
    screenshot_window.overrideredirect(1)  # Oculta la cabecera de la ventana
    button_frame = tk.Frame(screenshot_window)
    button_frame.pack(side=tk.LEFT, padx=5, pady=5)
    zoom_in_button = tk.Button(button_frame, text="Ampliar", command=zoom_in, width=10)
    zoom_in_button.pack(padx=5, pady=5)
    zoom_out_button = tk.Button(button_frame, text="Reducir", command=zoom_out, width=10)
    zoom_out_button.pack(padx=5, pady=5)
    draw_button = tk.Button(button_frame, text="Dibujar", command=toggle_mode, width=10)
    draw_button.pack(padx=5, pady=5)
    save_button = tk.Button(button_frame, text="Enviar", command=save_in_remote_storage, width=10)
    save_button.pack(padx=5, pady=5)
    close_button = tk.Button(button_frame, text="Cerrar", command=close_window, width=10)
    close_button.pack(padx=5, pady=5)
    screenshot = capture_screenshot()
    canvas = tk.Canvas(screenshot_window, width=screenshot.shape[1], height=screenshot.shape[0])
    canvas.pack()
    canvas.bind("<Button-1>", on_mouse_click)
    canvas.bind("<ButtonRelease-1>", on_mouse_click)
    canvas.bind("<B1-Motion>", on_mouse_move)
    update_canvas(screenshot)

def main():
    global root
    root = tk.Tk()
    root.title("ScreenShot Vault")
    root.geometry("300x150+100+100")
    root.minsize(300, 200)  # Establece un tamaño mínimo para la ventana
    root.attributes("-alpha", 0.9)
    # Carga la imagen en un objeto PhotoImage
    cameraImg = tk.PhotoImage(file="images/camera.png")
    # Reduce el tamaño de la imagen a la mitad
    imagen_reducida = cameraImg.subsample(8, 8)
    screenshot_button = tk.Button(root, text="Captura", command=open_screenshot_window)
    screenshot_button.pack(padx=20, pady=20)
    root.mainloop()

if __name__ == "__main__":
    load_dotenv()
    ip = os.getenv('SERVER_IP')
    port = int(os.getenv('SERVER_PORT'))
    main()
