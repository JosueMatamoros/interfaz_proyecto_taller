import tkinter as tk
from interfaz import Frame, barra_menu
def main():
    ventana = tk.Tk()
    ventana.title("Asistente para órganos colegiados")
    barra_menu(ventana)
    
    app = Frame(ventana = ventana)

    app.mainloop()
 
 
if __name__ == "__main__":
    main()