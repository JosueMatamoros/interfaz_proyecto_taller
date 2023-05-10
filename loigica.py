import tkinter as tk # Importamos la librería tkinter para crear la interfaz gráfica
from tkinter import filedialog # Importamos el módulo filedialog para abrir el explorador de archivos
from pydub import AudioSegment
from pydub.silence import split_on_silence


global agenda
agenda = {}
def puntos_agenda(punto_general, punto):
    if punto_general not in agenda:
        agenda[punto_general] = set([punto])
    else:
        puntos_especificos = agenda[punto_general]
        if punto in puntos_especificos:
            return "El punto específico ya existe en el punto general."
        puntos_especificos.add(punto)
    return "Punto agregado correctamente."

#resultado = puntos_agenda("Punto general 1", "Punto específico 1")
#resultado = puntos_agenda("Punto general 1", "Punto específico 2")
#resultado = puntos_agenda("Punto general 1", "Punto específico 2")
#resultado = puntos_agenda("Punto general 2", "Punto específico 3")

def seleccionar_archivo(ruta_texto):
    """
    Función que permite seleccionar un archivo de audio.
    """
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de audio", "*.wav")])
    ruta_texto.delete("1.0", tk.END)
    ruta_texto.insert(tk.END, archivo)

def seleccionar_carpeta_destino(ruta_carpeta_texto):
    """
    Función que permite seleccionar una carpeta de destino para guardar los segmentos de audio.
    """
    carpeta_destino = filedialog.askdirectory()
    ruta_carpeta_texto.delete("1.0", tk.END)
    ruta_carpeta_texto.insert(tk.END, carpeta_destino)
    return carpeta_destino

def dividir_audio(ruta_texto, ruta_carpeta_texto):
    """
    Función que permite dividir un archivo de audio en segmentos de audio.
    """
    archivo = ruta_texto.get("1.0", tk.END).strip()
    carpeta_destino = ruta_carpeta_texto.get("1.0", tk.END).strip()

    if archivo == "" or carpeta_destino == "":
        tk.messagebox.showwarning("Advertencia", "Por favor, seleccione el archivo de audio y la carpeta de destino.")
        return

    duracion_pausa_ms = 3000

    audio = AudioSegment.from_file(archivo, format="wav")
    segmentos = split_on_silence(audio, min_silence_len=duracion_pausa_ms, silence_thresh=-50)

    for i, segmento in enumerate(segmentos):
        segmento.export(f"{carpeta_destino}/segmento_{i}.wav", format="wav")

    tk.messagebox.showinfo("Fin del proceso", "Se ha dividido el audio en segmentos correctamente.")