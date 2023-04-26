import cv2
import numpy as np
import tkinter as tk
import os
import socket
import struct
import progressbar
import time
from dotenv import load_dotenv
from PIL import Image, ImageTk, ImageGrab
from datetime import datetime
from io import BytesIO


class ScreenShotApp:

    def __init__(self):
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0
        self.drawing = False
        self.screenshot = None
        self.screenshot_window = None
        self.canvas = None
        self.mode = "select"
        self.last_image_saved = None
        self.root = None
        self.ip = ''
        self.port = ''
        self.API_KEY = os.getenv('API_KEY')
        load_dotenv()
        self.ip = os.getenv('SERVER_IP')
        self.port = int(os.getenv('SERVER_PORT'))

    def save_in_remote_storage(self):
        self.screenshot_window.withdraw()
        self.root.deiconify()
        self.send_image()

    def calculate_buffer_size(self, image_size_bytes):
        MIN_BUFFER_SIZE = 1024
        MAX_BUFFER_SIZE = 32768
        BUFFER_SIZE_FACTOR = 0.05
        buffer_size = int(image_size_bytes * BUFFER_SIZE_FACTOR)
        buffer_size = max(MIN_BUFFER_SIZE, buffer_size)
        buffer_size = min(MAX_BUFFER_SIZE, buffer_size)
        return buffer_size

    def send_image(self):
        self.save_image_locally()
        img = Image.open(self.last_image_saved)
        buf = BytesIO()
        img.save(buf, format='PNG')
        img_bytes = buf.getvalue()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        file_len = len(img_bytes)
        buffer_size = self.calculate_buffer_size(file_len)

        print('img name :' + self.last_image_saved)
        sock.sendto(self.last_image_saved.encode('utf-8'), (self.ip, self.port))
        sock.sendto(struct.pack('<L', file_len), (self.ip, self.port))

        bar = progressbar.ProgressBar(max_value=file_len)

        for i in range(0, len(img_bytes), buffer_size):
            sock.sendto(img_bytes[i:i + buffer_size], (self.ip, self.port))
            bar.update(i)
        bar.finish()
        sock.close()

    def capture_screenshot(self):
        self.screenshot = ImageGrab.grab()
        return cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_RGB2BGR)

    def zoom_in(self):
        height, width = self.screenshot.shape[:2]
        self.screenshot = cv2.resize(self.screenshot, (int(width * 1.2), int(height * 1.2)), interpolation=cv2.INTER_LINEAR)
        self.update_canvas(self.screenshot)

    def zoom_out(self):
        height, width = self.screenshot.shape[:2]
        self.screenshot = cv2.resize(self.screenshot, (int(width * 0.8), int(height * 0.8)), interpolation=cv2.INTER_LINEAR)
        self.update_canvas(self.screenshot)

    def generate_file_name(self):
        d = datetime.today()
        return d.strftime("%d_%m_%Y-%H-%M-%S") + "_screenshot.png"

    def on_mouse_click(self, event):
        if event.type == tk.EventType.ButtonPress:
            self.x1, self.y1 = event.x, event.y
            self.drawing = True
        elif event.type == tk.EventType.ButtonRelease:
            self.x2, self.y2 = event.x, event.y
            self.drawing = False
            self.last_image_saved = self.generate_file_name()
            if self.mode == "select":
                cropped_screenshot = self.screenshot[self.y1:self.y2, self.x1:self.x2]
                if cropped_screenshot.size > 0:
                    self.update_screenshot(cropped_screenshot)
                    self.update_canvas(cropped_screenshot)
                else:
                    print("La imagen está vacía")

    def on_mouse_move(self, event):
        if self.drawing:
            self.x2, self.y2 = event.x, event.y
            img_copy = np.copy(self.screenshot)

            if self.mode == "select":
                cv2.rectangle(img_copy, (self.x1, self.y1), (self.x2, self.y2), (0, 0, 255), 2)
            elif self.mode == "draw":
                cv2.line(img_copy, (self.x1, self.y1), (self.x2, self.y2), (0, 255, 255), 2)
                self.screenshot = img_copy
                self.x1, self.y1 = self.x2, self.y2
            self.update_canvas(img_copy)

    def esperar(self): 
        # Retraso de 4 segundos
        for i in range(4, 0, -1):
            self.root.title(f"Esperando... {i}")
            self.root.update()
            time.sleep(1)

    def update_canvas(self, img):
        photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.image = photo
        # Cambiar el tamaño del canvas al de la imagen nueva
        self.canvas.config(width=img.shape[1], height=img.shape[0])
        # Actualizar el tamaño de la ventana
        y = img.shape[0]
        x = img.shape[1]

        self.screenshot_window.geometry(f"{x}x{y}")
        
    def update_screenshot(self, img):
        self.screenshot = img

    def toggle_mode(self):
        self.mode = "draw" if self.mode == "select" else "select"

    def save_image_locally(self) :
        self.last_image_saved = self.generate_file_name()
        cv2.imwrite(self.last_image_saved, self.screenshot)
        
    def open_screenshot_window(self):
        self.esperar()
        self.screenshot_window = tk.Toplevel(self.root)
        self.root.withdraw()
        self.screenshot_window.deiconify()
        # Configurar propiedades de la ventana
        self.screenshot_window.wm_attributes("-topmost", True)
        self.screenshot_window.wm_attributes("-disabled", False)

        self.screenshot_window.title("Captura de pantalla")
        self.screenshot_window.overrideredirect(1)
        button_frame = tk.Frame(self.screenshot_window)
        button_frame.pack(side=tk.LEFT, padx=5, pady=5)
        zoom_in_button = tk.Button(button_frame, text="Ampliar", command=self.zoom_in, width=10)
        zoom_in_button.pack(padx=5, pady=5)
        zoom_out_button = tk.Button(button_frame, text="Reducir", command=self.zoom_out, width=10)
        zoom_out_button.pack(padx=5, pady=5)
        draw_button = tk.Button(button_frame, text="Dibujar", command=self.toggle_mode, width=10)
        draw_button.pack(padx=5, pady=5)
        send_button = tk.Button(button_frame, text="Enviar", command=self.save_in_remote_storage, width=10)
        send_button.pack(padx=5, pady=5)
        save_button = tk.Button(button_frame, text="Guardar", command=self.save_image_locally, width=10)
        save_button.pack(padx=5, pady=5)
        close_button = tk.Button(button_frame, text="Cerrar", command=self.close_window, width=10)
        close_button.pack(padx=5, pady=5)
        self.screenshot = self.capture_screenshot()
        self.canvas = tk.Canvas(self.screenshot_window, width=self.screenshot.shape[1], height=self.screenshot.shape[0])
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.update_canvas(self.screenshot)

    def close_window(self):
        self.root.destroy()

    def main(self):
        self.root = tk.Tk()
        self.root.title("ScreenShot Vault")
        self.root.geometry("300x150+100+100")
        self.root.minsize(300, 200)
        self.root.attributes("-alpha", 0.9)
        screenshot_button = tk.Button(self.root, text="Captura", command=self.open_screenshot_window)
        screenshot_button.pack(padx=20, pady=20)
        self.root.mainloop()

if __name__ == "__main__":
    app = ScreenShotApp()
    app.main()