import tkinter as tk # Importamos la librería tkinter para crear la interfaz gráfica
from tkinter import filedialog # Importamos el módulo filedialog para abrir el explorador de archivos
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import os

global personas # Diccionario que almacena los participantes.
global agenda # Diccionario que almacena los puntos de la agenda.
global reporte # Lista que almacena los puntos de la agenda.
personas = {}
agenda = {}
reporte = []

def puntos_agenda(punto_general:str, punto:str):
    """
    Función que permite agregar un punto de la agenda a la lista de puntos de la agenda.

    Args:
        punto_general (str): Punto general de la agenda.
        punto (str): Punto específico de la agenda.

    Returns:
        dict: Retorno la agenda con los nuevos cambios.
    """
    # Eliminamos los espacios en blanco al inicio y al final de la cadena y convertimos la primera letra en mayúscula.
    punto_general = punto_general.strip().capitalize()
    punto = punto.strip().capitalize()

    #Lógica para agregar los puntos de la agenda.
    if punto_general not in agenda:
        agenda[punto_general] = set([punto])
    else:
        puntos_especificos = agenda[punto_general]
        if punto in puntos_especificos:
            tk.messagebox.showwarning("Advertencia", "El punto especifico ya existe.")
        puntos_especificos.add(punto)
    return agenda

def eliminar_punto_diccionario(punto_general, punto_especifico,diccionario):
        """
        Función que permite eliminar un punto de la agenda de la lista de puntos de la agenda.

    Args:
        punto_general (str): Punto general de la agenda.
        punto_especifico (str): Punto específico de la agenda.
        diccionario (dict): Diccionario que contiene los puntos de la agenda.

    Returns:
        dict: Retorno la agenda con el punto eliminado.
        """
        # Logica para eliminar los puntos de la agenda.
        if punto_general in diccionario and punto_especifico in diccionario[punto_general]:
            diccionario[punto_general].remove(punto_especifico)
            if len(diccionario[punto_general]) == 0:
                del diccionario[punto_general]
        return diccionario

def participantes_agenda(carnet:str,nombre:str):
    """
    Función que permite agregar un participante a la lista de participantes.

    Args:
        carnet (str): Carnet del participante que se desea agregar.
        nombre (str): Nombre del participante que se desea agregar.
    """
    # Eliminamos los espacios en blanco al inicio y al final de la cadena.
    carnet = carnet.strip()
    nombre = nombre.strip()

    # Lógica para agregar los participantes.
    if carnet not in personas:
        personas[carnet] = {
            "nombre": nombre,
            "t_palabras": 0 
        }   # Espacio para total de palabras por persona en la reunión.
    else:
        tk.messagebox.showwarning("Advertencia", "El participante ya existe.")
    
def eliminar_participante(carne:str):
    """
    Función que permite eliminar un participante de la lista de participantes.

    Args:
        carne (str): Carnet de la personas que se desea eliminar.
    """
    # Lógica para eliminar participantes.
    if carne in personas:
        del personas[carne]

def modificar_participante(punto_general,punto_especifico,carne:str,texto:str):
    """
    Función que permite agregar los datos a la base de datos.

    Args:
        punto_general (str: Punto general de la agenda.
        punto_especifico (str): Punto específico de la agenda.
        carne (str): Carnet de la persona que participó.
        texto (str): Texto reconocido por el speech recognition.
    """
    #Total de palabras por persona en la reunión.
    total_palabras = len(texto.split())
    personas[carne]["t_palabras"] += total_palabras
    #Participaciones por subtema.
    nombre =  personas[carne]["nombre"]
    reporte.append([f"{punto_general} - {punto_especifico} - {nombre} - {texto}"])

    #Participaciones por subtema.
    if punto_general in personas[carne]:
        if punto_especifico in personas[carne][punto_general]:
            personas[carne][punto_general][punto_especifico] += 1
        else:
            personas[carne][punto_general][punto_especifico] = 1
    else:
        personas[carne][punto_general] = {punto_especifico: 1}

def seleccionar_carpeta_segmentos(ruta_carpeta_texto):
    """
    Función que permite seleccionar la carpeta que contiene los archivos de audio.

    Args:
        ruta_carpeta_texto (str): Ruta de la carpeta que contiene los archivos de audio.

    Returns:
        str: Dirección de la carpeta que contiene los archivos de audio.
    """
    carpeta_segmentos = filedialog.askdirectory()
    ruta_carpeta_texto.delete("1.0", tk.END)
    ruta_carpeta_texto.insert(tk.END, carpeta_segmentos)
    return obtener_archivos_audio(carpeta_segmentos)

def obtener_archivos_audio(carpeta):
    """
    Función que permite obtener los archivos de audio de una carpeta.

    Args:
        carpeta (str): Dirección de la carpeta que contiene los archivos de audio.

    Returns:
        list: Lista con las rutas de los archivos de audio.
    """
    archivos = [] # Lista que contiene las rutas de los archivos de audio.
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".mp3") or archivo.endswith(".wav"):
            ruta_archivo = carpeta+"/"+archivo # Obtiene la ruta completa del archivo
            #ruta_archivo.replace("\\", "/")   Reemplazar barras invertidas con barras inclinadas hacia adelante
            archivos.append(ruta_archivo)
    return archivos

def corregir_ruta_archivo(ruta_archivo):
    """
    Función que permite corregir la ruta de un archivo al formato correcto para el speech recognition.

    Args:
        ruta_archivo (str): Str qur contiene la ruta del archivo.

    Returns:
        str: Ruta del archivo corregida.
    """
    # Corregir la ruta del archivo al formato correcto para el speech recognition.
    ruta_absoluta = os.path.abspath(ruta_archivo)
    ruta_carpeta = os.path.dirname(ruta_absoluta)
    nombre_archivo = os.path.basename(ruta_absoluta)
    ruta_corregida = os.path.join(ruta_carpeta, nombre_archivo)
    return ruta_corregida

def convertir_audio_a_texto(archivo_audio):
    """
    Función que permite convertir un archivo de audio a texto.

    Args:
        archivo_audio (str): Ruta del archivo de audio.

    Returns:
        str: Transcripción del archivo de audio.
    """

    r = sr.Recognizer()
    with sr.AudioFile(archivo_audio) as fuente:
        audio = r.record(fuente)

    try:
        texto = r.recognize_google(audio, language="es-ES")
        return texto
    except sr.UnknownValueError:
        tk.messagebox.showwarning("No se pudo reconocer el audio.")
    except sr.RequestError as e:
        tk.messagebox.showwarning(f"Error al realizar la solicitud al servicio de reconocimiento de voz de Google: {e}")


def seleccionar_archivo(ruta_texto):
    """
    Función que permite seleccionar un archivo de audio.

    Args:
        ruta_texto (str): Ruta del archivo de audio.
    """
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de audio", "*.wav")])
    ruta_texto.delete("1.0", tk.END)
    ruta_texto.insert(tk.END, archivo)

def seleccionar_carpeta_destino(ruta_carpeta_texto):
    """
    Función que permite seleccionar la carpeta de destino de los archivos de audio.

    Args:
        ruta_carpeta_texto (str): Ruta de la carpeta de destino de los archivos de audio.

    Returns:
        str: Dirección de la carpeta de destino de los archivos de audio.
    """
    carpeta_destino = filedialog.askdirectory()
    ruta_carpeta_texto.delete("1.0", tk.END)
    ruta_carpeta_texto.insert(tk.END, carpeta_destino)
    return carpeta_destino

def dividir_audio(ruta_carpeta_texto, ruta_texto):
    """
    Función que permite dividir un archivo de audio en segmentos.

    Args:
        ruta_carpeta_texto (_type_): _description_
        ruta_texto (_type_): _description_
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

def eliminar_segmento_usado(elemento,archivo):
    """
    Función que permite eliminar un elemento de una lista.

    Args:
        elemento (str): Elemento a eliminar.
        archivo (str): Lista con elementos.

    Returns:
        list: Lista sin el elemento eliminado.
    """
    if elemento in archivo:
        archivo.remove(elemento)
    return archivo