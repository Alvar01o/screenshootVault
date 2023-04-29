import tkinter as tk

class MiAplicacion:
    def __init__(self, master):
        self.master = master
        self.master.overrideredirect(1)  # Elimina la cabecera
        self.master.geometry("300x300")  # Tamaño de la ventana

        # Crea un panel transparente en la parte inferior
        panel_inferior = tk.Frame(self.master, bg="", highlightthickness=0)
        panel_inferior.pack(side=tk.BOTTOM, fill=tk.X)

        # Crea 3 botones alineados a la izquierda y sin padding
        boton1 = tk.Button(panel_inferior, text="Botón 1", padx=0, pady=0, height=2, width=6)
        boton1.pack(side=tk.LEFT)

        boton2 = tk.Button(panel_inferior, text="Botón 2", padx=0, pady=0, height=2, width=6)
        boton2.pack(side=tk.LEFT)

        boton3 = tk.Button(panel_inferior, text="Botón 3", padx=0, pady=0, height=2, width=6)
        boton3.pack(side=tk.LEFT)

def main():
    root = tk.Tk()
    app = MiAplicacion(root)
    root.mainloop()

if __name__ == "__main__":
    main()
