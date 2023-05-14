import tkinter as tk
from tkinter import ttk
from interfaz import Frame,divisor_audio,barra_menu, participantes, transcripción

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Asistente para órganos colegiados")
        self.barra_menu = barra_menu(self)
        self.config(menu=self.barra_menu)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.frame_agregar_punto = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_agregar_punto, text="Puntos de la agenda")

        self.frame_participantes = participantes(self.notebook)
        self.notebook.add(self.frame_participantes, text="Participantes")

        self.frame_eliminar_punto = transcripción(self.notebook)
        self.notebook.add(self.frame_eliminar_punto, text="Transcripción")

        self.frame_divisor_audio = divisor_audio(self.notebook)
        self.notebook.add(self.frame_divisor_audio, text="Divisor de audio")

        self.app = Frame(self.frame_agregar_punto)  # Pasamos el frame correspondiente como padre

    def change_tab(self, index):
        self.notebook.select(index)  # Cambiar a la pestaña en el índice especificado

def main():
    app = MainApplication()
    app.mainloop()

if __name__ == "__main__":
    main()
