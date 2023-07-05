import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
import os
import time
from UDPClient import UDPClient
from dotenv import load_dotenv
from PIL import Image, ImageTk, ImageGrab

import sys
sys.path.append('.')

class ScreenShotApp:

    def __init__(self):
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0
        self.drawing = False
        self.client = UDPClient()
        self.screenshot = None
        self.screenshot_window = None
        self.screenshot_button = None
        self.canvas = None
        self.mode = "select"
        self.root = None
        self.API_KEY = os.getenv('API_KEY')
        load_dotenv()


    def save_in_remote_storage(self):
        self.send_image()

    def send_image(self):
        self.save_image_locally()
        self.client.send_file()
        
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


    def on_mouse_click(self, event):
        if event.type == tk.EventType.ButtonPress:
            self.x1, self.y1 = event.x, event.y
            self.drawing = True
        elif event.type == tk.EventType.ButtonRelease:
            self.x2, self.y2 = event.x, event.y
            self.drawing = False
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
        
    def update_screenshot(self, img):
        self.screenshot = img

    def toggle_mode(self):
        self.mode = "draw" if self.mode == "select" else "select"

    def save_image_locally(self) :
        self.client.generate_file_name()
        cv2.imwrite(self.client.get_last_image_saved(), self.screenshot)
        
    def open_screenshot_window(self):
        self.screenshot_button.config(state='disabled')
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
        self.screenshot = self.capture_screenshot()
        self.save_image_locally()
        self.save_in_remote_storage()

if __name__ == "__main__":
    app = ScreenShotApp()
    app.main()