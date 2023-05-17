import tkinter as tk
from tkinter import ttk 
from loigica import puntos_agenda, eliminar_punto_diccionario, agenda,archivos, personas,eliminar_participante, seleccionar_archivo, seleccionar_carpeta_destino, dividir_audio,participantes_agenda, seleccionar_carpeta_segmentos, convertir_audio_a_texto, corregir_ruta_archivo, modificar_participante, eliminar_segmento_usado, reporte, guardar_diccionario, seleccionar_archivo_texto, cargar_datos

def barra_menu(ventana):
    barra_menu = tk.Menu(ventana)
    ventana.config(menu=barra_menu)

class Frame(tk.Frame):
    def __init__(self, ventana=None):
        super().__init__(ventana,width=700, height=500)
        self.ventana = ventana
        self.pack()

        self.puntos_agenda()
        self.deshabilitar_campos()
        self.tabla_puntos(agenda)

        self.entry_general = None
        self.entry_especifico = None

    def puntos_agenda(self):
        """
        Este método crea los elementos de la interfaz para la agenda.
        """
        #Labels para cada apartado de la agenda
        self.punto_general = tk.Label(self, text="Punto general")
        self.punto_general.config(font = ("arial",12, "bold"))
        self.punto_general.grid(row=0, column=0, padx=10, pady=10)

        self.punto_especifico = tk.Label(self, text="Punto específico")
        self.punto_especifico.config(font = ("arial",12, "bold"))
        self.punto_especifico.grid(row=1, column=0, padx=10, pady=10)

        #Entradas para cada apartado de la agenda
        self.punto_general = tk.StringVar()
        self.entry_punto_general = tk.Entry(self, textvariable = self.punto_general)
        self.entry_punto_general.config(width = 50 , font = ("arial",12, ))
        self.entry_punto_general.grid(row=0, column=1, padx=10, pady=10, columnspan=2)
        
        self.punto_especifico = tk.StringVar()
        self.entry_punto_especifico = tk.Entry(self, textvariable = self.punto_especifico)
        self.entry_punto_especifico.config(width = 50 , font = ("arial",12, ))
        self.entry_punto_especifico.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        #Botones 
        self.boton_nuevo = tk.Button(self, text="Nuevo",command=self.habilitar_campos)
        self.boton_nuevo.config(width = 20, font = ("arial",12, "bold"),
                                bg="#2196F3" ,activebackground="#BBDEFB", fg="white", cursor="hand2")
        self.boton_nuevo.grid(row=2, column=0, padx=10, pady=10)
       
        self.boton_guardar= tk.Button(self, text="Guardar", command= self.guardar_punto)
        self.boton_guardar.config(width = 20, font = ("arial",12, "bold"),
                                  bg="#CC33FF", activebackground="#CE93D8", fg="white", cursor="hand2")
        self.boton_guardar.grid(row=2, column=1, padx=10, pady=10)
      
        self.boton_cancelar= tk.Button(self, text="Cancelar",command=self.deshabilitar_campos)
        self.boton_cancelar.config(width = 20, font = ("arial",12, "bold"),
                                   bg="#EF5350", activebackground="#FFCDD2", fg="white", cursor="hand2")
        self.boton_cancelar.grid(row=2, column=2, padx=10, pady=10)
        
        #Botón para editar tabla
        self.boton_editar = tk.Button(self, text="Editar",state=tk.DISABLED, command=self.editar_punto_ventana)
        self.boton_editar.config(width = 20, font = ("arial",12, "bold"),
                                    bg="#2196F3" ,activebackground="#BBDEFB", fg="white", cursor="hand2")
        self.boton_editar.grid(row=4, column=0, padx=10, pady=10)

        #Botón para eliminar contenido de la tabla
        self.boton_eliminar = tk.Button(self, text="Eliminar", command=self.eliminar_punto_ventana, state=tk.DISABLED)
        self.boton_eliminar.config(width = 20, font = ("arial",12, "bold"),
                                    bg="#EF5350", activebackground="#FFCDD2", fg="white", cursor="hand2")
        self.boton_eliminar.grid(row=4, column=1, padx=10, pady=10)

    def habilitar_campos(self):
        self.punto_general.set(" ")
        self.punto_especifico.set(" ")

        self.entry_punto_general.config(state="normal")
        self.entry_punto_especifico.config(state="normal")

        self.boton_guardar.config(state="normal")
        self.boton_cancelar.config(state="normal")
    
    def deshabilitar_campos(self):
        self.punto_general.set(" ")
        self.punto_especifico.set(" ")

        self.entry_punto_general.config(state="disabled")
        self.entry_punto_especifico.config(state="disabled")

        self.boton_guardar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")
        
    def guardar_punto(self):
        puntos_agenda(self.punto_general.get(), self.punto_especifico.get())
        self.deshabilitar_campos()
        self.tabla_puntos(agenda)
       
    def tabla_puntos(self, diccionario):
        contenedor_tabla = tk.Frame(self)
        contenedor_tabla.grid(row=3, column=0, columnspan=4, sticky="nsew")

        self.tabla = ttk.Treeview(contenedor_tabla, columns=("Punto general", "Punto específico"))
        self.tabla.grid(row=0, column=0, columnspan=4, sticky="nsew")

        contenedor_tabla.grid_rowconfigure(0, weight=1)
        contenedor_tabla.grid_columnconfigure(0, weight=1)

        self.tabla.heading("#0", text="ID")
        self.tabla.heading("#1", text="Punto general")
        self.tabla.heading("#2", text="Punto específico")

        id_counter = 1
        for punto_general, subpuntos in diccionario.items():
            for subpunto in subpuntos:
                self.tabla.insert('', 'end', text=str(id_counter), values=(punto_general, subpunto))
                id_counter += 1

         # Asociar eventos de selección en la tabla a la actualización de los botones
        self.tabla.bind("<<TreeviewSelect>>", self.actualizar_botones)
    
    def actualizar_botones(self, event = None):
        item = self.tabla.selection()

        if item:
            self.boton_eliminar.config(state=tk.NORMAL)
            self.boton_editar.config(state=tk.NORMAL)
        else:
            self.boton_eliminar.config(state=tk.DISABLED)
            self.boton_editar.config(state=tk.DISABLED)

    def eliminar_punto_ventana(self):
        # Obtener el punto seleccionado en la tabla
        item = self.tabla.selection()[0]
        punto_general = self.tabla.item(item)['values'][0]
        punto_especifico = self.tabla.item(item)['values'][1]

        # Eliminar el punto de la tabla
        self.tabla.delete(item)
        eliminar_punto_diccionario(punto_general, punto_especifico, agenda)
        self.tabla_puntos(agenda)
        
    def editar_punto_ventana(self):
    # Obtener el punto seleccionado en la tabla
        item = self.tabla.selection()[0]
        punto_general = self.tabla.item(item)['values'][0]
        punto_especifico = self.tabla.item(item)['values'][1]

        # Crear una nueva ventana de edición
        ventana_edicion = tk.Toplevel(self)
        ventana_edicion.geometry("300x150")  # Especificar tamaño de la ventana

        # Etiquetas y campos de entrada para editar el punto
        label_general = tk.Label(ventana_edicion, text="Punto general:")
        label_general.pack()
        self.entry_general = tk.Entry(ventana_edicion)
        self.entry_general.insert(tk.END, punto_general)
        self.entry_general.pack()


        label_especifico = tk.Label(ventana_edicion, text="Punto específico:")
        label_especifico.pack()
        self.entry_especifico = tk.Entry(ventana_edicion)
        self.entry_especifico.insert(tk.END, punto_especifico)
        self.entry_especifico.pack()

        # Botón para guardar los cambios
        boton_guardar = tk.Button(ventana_edicion, text="Guardar cambios", command=lambda: [self.guardar_cambios(punto_general, punto_especifico, agenda), ventana_edicion.destroy()])
        boton_guardar.pack(pady=10, padx=10)

    def guardar_cambios(self, punto_general, punto_especifico, diccionario):
        # Obtener los nuevos valores del punto editado
        nuevo_punto_general = self.entry_general.get()
        nuevo_punto_especifico = self.entry_especifico.get()

        # Modificar el punto específico y la clave
        if punto_general in diccionario and punto_especifico in diccionario[punto_general]:
            conjunto = diccionario[punto_general]
            conjunto.remove(punto_especifico)
            conjunto.add(nuevo_punto_especifico)
            if punto_general != nuevo_punto_general:
                diccionario[nuevo_punto_general] = diccionario.pop(punto_general)

        # Actualizar la tabla con los cambios realizados
        self.tabla_puntos(diccionario)

class divisor_audio(tk.Frame):
    def __init__(self, ventana=None):
        super().__init__(ventana, width=700, height=500)
        self.ventana = ventana

        # Etiqueta y botón para seleccionar el archivo de audio
        etiqueta_archivo = tk.Label(self, text="Archivo de audio:")
        etiqueta_archivo.grid(row=0, column=0, padx=5, pady=5)
        etiqueta_archivo.config(font=("arial", 12, "bold"))

        boton_seleccionar_archivo = tk.Button(self, text="Seleccionar archivo", command=lambda: seleccionar_archivo(self.ruta_texto))
        boton_seleccionar_archivo.grid(row=1, column=0, padx=10, pady=10)
        boton_seleccionar_archivo.config(width=20, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")

        self.ruta_texto = tk.Text(self, height=1)
        self.ruta_texto.grid(row=2, column=0, padx=10, pady=10)

        # Etiqueta y campo de texto para especificar la carpeta de destino
        etiqueta_carpeta_destino = tk.Label(self, text="Carpeta de destino:")
        etiqueta_carpeta_destino.grid(row=3, column=0, padx=5, pady=5)
        etiqueta_carpeta_destino.config(font=("arial", 12, "bold"))

        boton_seleccionar_carpeta = tk.Button(self, text="Seleccionar carpeta", command=lambda: seleccionar_carpeta_destino(self.ruta_carpeta_texto))
        boton_seleccionar_carpeta.grid(row=4, column=0, padx=10, pady=10)
        boton_seleccionar_carpeta.config(width=20, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")

        self.ruta_carpeta_texto = tk.Text(self, height=1)
        self.ruta_carpeta_texto.grid(row=5, column=0, padx=10, pady=10)

        # Botón para iniciar la división del audio
        boton_dividir_audio = tk.Button(self, text="Dividir audio", command=lambda: dividir_audio(self.ruta_carpeta_texto, self.ruta_texto))
        boton_dividir_audio.grid(row=6, column=0, padx=10, pady=10)
        boton_dividir_audio.config(width=20, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")

class participantes(tk.Frame):
    def __init__(self, ventana=None):
        super().__init__(ventana, width=700, height=500)
        self.ventana = ventana
        self.puntos_participante()
        self.tabla_puntos(personas)

    def puntos_participante(self):
        #Labels para la información del participante.
        self.punto_carnet = tk.Label(self, text="Carnet")
        self.punto_carnet.config(font = ("arial",12, "bold"))
        self.punto_carnet.grid(row=0, column=0, padx=10, pady=10)

        self.punto_nombre = tk.Label(self, text="Nombre")
        self.punto_nombre.config(font = ("arial",12, "bold"))
        self.punto_nombre.grid(row=1, column=0, padx=10, pady=10)

        #Entradas para la información del participante.
        self.punto_carnet = tk.StringVar()
        self.entry_punto_carnet = tk.Entry(self, textvariable = self.punto_carnet)
        self.entry_punto_carnet.config(width = 50 , font = ("arial",12, ))
        self.entry_punto_carnet.grid(row=0, column=1, padx=10, pady=10, columnspan=2)
        
        self.punto_nombre = tk.StringVar()
        self.entry_punto_nombre = tk.Entry(self, textvariable = self.punto_nombre)
        self.entry_punto_nombre.config(width = 50 , font = ("arial",12, ))
        self.entry_punto_nombre.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        #Validación de entrada de datos.
        self.punto_carnet.trace("w", self.check_entry_content)
        self.punto_nombre.trace("w", self.check_entry_content)

        #Botón para guardar información del participante.
        self.boton_guardar= tk.Button(self, text="Guardar", command= self.guardar_participante)
        self.boton_guardar.config(width = 20, font = ("arial",12, "bold"),
                                  fg="white", cursor="hand2",bg="#CC33FF", activebackground="#CE93D8", state=tk.DISABLED)
        self.boton_guardar.grid(row=2, column=0, padx=10, pady=10)

        #Botón para eliminar contenido de la tabla.
        self.boton_eliminar = tk.Button(self, text="Eliminar", command=self.eliminar_personas_ventana)
        self.boton_eliminar.config(width = 20, font = ("arial",12, "bold"),state=tk.DISABLED,
                                   bg="#EF5350", activebackground="#FFCDD2", fg="white", cursor="hand2")
        self.boton_eliminar.grid(row=4, column=1, padx=10, pady=10)

        #Botón para editar tabla
        self.boton_editar = tk.Button(self, text="Editar",command=self.editar_personas_ventana)
        self.boton_editar.config(width = 20, font = ("arial",12, "bold"),
                                    bg="#2196F3" ,activebackground="#BBDEFB", fg="white", cursor="hand2", state=tk.DISABLED)
        self.boton_editar.grid(row=4, column=0, padx=10, pady=10)
     
    def tabla_puntos(self, diccionario:dict):
        contenedor_tabla = tk.Frame(self)
        contenedor_tabla.grid(row=3, column=0, columnspan=4, sticky="nsew")

        self.tabla_participantes = ttk.Treeview(contenedor_tabla, columns=("Carnet","Nombre"))
        self.tabla_participantes.grid(row=0, column=0, columnspan=4, sticky="nsew")

        contenedor_tabla.grid_rowconfigure(0, weight=1)
        contenedor_tabla.grid_columnconfigure(0, weight=1)

        self.tabla_participantes.heading("#0", text="Carnet")
        self.tabla_participantes.heading("#1", text="Nombre")
        self.tabla_participantes.heading("#2", text="Apellido")

        for carnet, datos in diccionario.items():
            nombre = datos["nombre"]
            self.tabla_participantes.insert('', 'end', text=str(carnet), values=(nombre))


        # Asociar el controlador de eventos a la tabla
        self.tabla_participantes.bind('<<TreeviewSelect>>', self.on_item_selected)
                
    def guardar_participante(self):
        participantes_agenda(self.punto_carnet.get(), self.punto_nombre.get())
        self.tabla_puntos(personas)
        self.limpiar_entry()
        self.boton_guardar.config(state=tk.DISABLED)
        
    def limpiar_entry(self):
        self.punto_carnet.set(" ")
        self.punto_nombre.set(" ")

    def eliminar_personas_ventana(self):
        # Obtener una persona y eliminarla de la tabla.
        item = self.tabla_participantes.selection()[0]
        carnet = self.tabla_participantes.item(item)['text']
        eliminar_participante(carnet)
        self.tabla_puntos(personas)
        self.desactivar_botones()
        
    def editar_personas_ventana(self):
        # Obtener una persona y editarla de la tabla.
        item = self.tabla_participantes.selection()[0]
        carnet = self.tabla_participantes.item(item)['text']
        nombre = self.tabla_participantes.item(item)['values'][0]

        # Crear una nueva ventana de edición
        ventana_edicion = tk.Toplevel(self)
        ventana_edicion.geometry("300x150")
        
        # Etiquetas y campos de entrada para editar el punto
        label_carnet = tk.Label(ventana_edicion, text="Punto general:")
        label_carnet.pack()
        self.entry_carnet = tk.Entry(ventana_edicion)
        self.entry_carnet.insert(tk.END, carnet)
        self.entry_carnet.pack()


        label_nombre = tk.Label(ventana_edicion, text="Punto específico:")
        label_nombre.pack()
        self.entry_nombre = tk.Entry(ventana_edicion)
        self.entry_nombre.insert(tk.END, nombre)
        self.entry_nombre.pack()

        # Botón para guardar los cambios
        boton_guardar = tk.Button(ventana_edicion, text="Guardar cambios", command=lambda: [self.guardar_cambios(carnet, nombre), ventana_edicion.destroy()])
        boton_guardar.pack(pady=10, padx=10)
        
    def guardar_cambios(self, carnet, nombre):
        nuevo_carnet = self.entry_carnet.get()
        nuevo_nombre = self.entry_nombre.get()

        if carnet == nuevo_carnet:
            personas[nuevo_carnet]["nombre"] = nuevo_nombre

        else:
            if nuevo_carnet not in personas:
                personas.pop(carnet)
                personas[nuevo_carnet] = {
                    "nombre": nombre,
                    "t_palabras": 0
                }   
            else:
                tk.messagebox.showwarning("Advertencia", "El participante ya existe.")

        self.tabla_puntos(personas)
        self.desactivar_botones()
    
    def on_item_selected(self, event = None):
        item = self.tabla_participantes.selection()

        if item:
            self.boton_eliminar.config(state=tk.NORMAL)  # Activar el botón Eliminar
            self.boton_editar.config(state=tk.NORMAL)  # Activar el botón Editar
        else:
            self.boton_eliminar.config(state=tk.DISABLED)  # Desactivar el botón Eliminar
            self.boton_editar.config(state=tk.DISABLED)  # Desactivar el botón Editar

    def desactivar_botones(self):
        self.boton_eliminar.config(state=tk.DISABLED)
        self.boton_editar.config(state=tk.DISABLED)
 
    def check_entry_content(self,*args):
        if self.punto_carnet.get() and self.punto_nombre.get():
            self.boton_guardar.config(state=tk.NORMAL)
        else:
            self.boton_guardar.config(state=tk.DISABLED)

class transcripción(tk.Frame):
    def __init__(self, ventana=None):
        super().__init__(ventana, width=700, height=500)
        self.ventana = ventana

        # Etiqueta y botón para seleccionar el archivo de audio
        self.boton_seleccionar_archivo = tk.Button(self, text="Seleccionar archivo",
                                                   command=self.mostar_tabla_segmentos)
        self.boton_seleccionar_archivo.grid(row=0, column=0, padx=5, pady=10,columnspan=2)
        self.boton_seleccionar_archivo.config(width=30, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")

        self.ruta_texto = tk.Text(self, height=1, width=30)
        self.ruta_texto.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.ruta_texto.config(width = 50 , font = ("arial",12, ))

        # Crear el label con texto rojo, centrado y dos líneas
        texto = "El audio debe de estar segmentado \n si lo necesita utilice la función dividir audio"
        self.advertencia = tk.Label(self, text=texto, foreground="red", justify="center", wraplength=200, height=2,font=("arial", 8, "bold"))
        self.advertencia.grid(row=2, column=0, padx=10, pady=10,ipadx=10, ipady=10,columnspan=2)

        #Etiqueta y botón para seleccionar la carpeta de destino de proyecto ya existente.
        self.boton_old_proyecto = tk.Button(self, text="Continuar existente",
                                                   command=self.proyecto_existente)
        self.boton_old_proyecto.grid(row=3, column=0, padx=5, pady=10,columnspan=2)
        self.boton_old_proyecto.config(width=30, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")

        self.ruta_op = tk.Text(self, height=1, width=30)
        self.ruta_op.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.ruta_op.config(width = 50 , font = ("arial",12, ))

        self.tabla = None  # Agregamos el atributo de la tabla
    
    def proyecto_existente(self):
        ruta = seleccionar_archivo_texto(self.ruta_op)
        agenda, personas, reporte, archivos = cargar_datos(ruta)
        self.new_pro_forget_boto()
        self.tabla_segmentos(archivos)

    def new_pro_forget_boto(self):
        self.boton_old_proyecto.grid_forget()
        self.ruta_op.grid_forget()
        self.boton_seleccionar_archivo.grid_forget()
        self.ruta_texto.grid_forget()
        self.advertencia.grid_forget()

    def continuar_mas_tarde(self):
        ruta = seleccionar_carpeta_destino(self.ruta_cd)
        guardar_diccionario(agenda,personas,reporte,self.archivos,ruta)
        self.destroy()

    def almacenar_información(self, parrafo: str):
        # Ocultar elementos de la interfaz
        self.tabla.grid_forget()
        self.boton_transcribir.grid_forget()
        self.boton_ver_reportes.grid_forget()
        self.boton_continuar_después.grid_forget()
        self.ruta_cd.grid_forget()

        # Label de selección de tema y subtema
        self.label_persona = tk.Label(self, text="Seleccione el carnet de la persona correspondiente")
        self.label_persona.config(font = ("arial",10, "bold"))
        self.label_persona.grid(row=0, column=0,sticky="w")

        self.label_general = tk.Label(self, text="Seleccione el tema correspondiente")
        self.label_general.config(font = ("arial",10, "bold"))
        self.label_general.grid(row=1, column=0,sticky="w")

        self.label_especifico = tk.Label(self, text="Seleccione el subtema correspondiente")
        self.label_especifico.config(font = ("arial",10, "bold"))
        self.label_especifico.grid(row=2, column=0,sticky="w")

        # Botones de selección de tema y subtema
        self.opcion_seleccionada_persona = tk.StringVar(value=list(personas.keys())[0])  # Valor inicial predeterminado
        self.opcion_persona = tk.OptionMenu(self, self.opcion_seleccionada_persona, *personas.keys())
        self.opcion_persona.grid(row=0, column=1,padx=10, pady=10, sticky="ew")

        self.opcion_seleccionada = tk.StringVar(value=list(agenda.keys())[0])  # Valor inicial predeterminado
        self.opcion_general = tk.OptionMenu(self, self.opcion_seleccionada, *agenda.keys(), command=lambda _: self.actualizar_opcion_especifica())
        self.opcion_general.grid(row=1, column=1,padx=10, pady=10, sticky="ew")

        self.opcion_seleccionada_especifica = tk.StringVar(value=list(agenda[self.opcion_seleccionada.get()])[0])
        self.opcion_especifica = tk.OptionMenu(self, self.opcion_seleccionada_especifica, *agenda[self.opcion_seleccionada.get()])
        self.opcion_especifica.grid(row=2, column=1,padx=10, pady=10, sticky="ew")

        # Entry para mostrar el texto transcrito
        self.parrafo = parrafo
        self.texto_variable = tk.StringVar(value=self.parrafo)

        self.texto_entry = tk.Text(self, height=5, width=30)
        self.texto_entry.insert(tk.END, self.parrafo)
        self.texto_entry.grid(row=0, column=2, rowspan=3, padx=10, pady=10, sticky="nsew")

        # Botón para guardar los cambios
        self.boton_agregar = tk.Button(self, text="Agregar", command=self.guardar_cambios)
        self.boton_agregar.grid(row=5, column=0, padx=5, pady=5)
        self.boton_agregar.config(width=20, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")

    def actualizar_opcion_especifica(self):
        self.opcion_especifica.grid_forget()
        self.opcion_seleccionada_especifica = tk.StringVar(value=list(agenda[self.opcion_seleccionada.get()])[0])
        self.opcion_especifica = tk.OptionMenu(self, self.opcion_seleccionada_especifica, *agenda[self.opcion_seleccionada.get()])
        self.opcion_especifica.grid(row=2, column=1, padx=2, pady=5)

    def guardar_cambios(self):
        punto_general = self.opcion_seleccionada.get()
        punto_especifico = self.opcion_seleccionada_especifica.get()
        carnet = self.opcion_seleccionada_persona.get()
        texto = self.texto_entry.get("1.0", tk.END)
        modificar_participante(punto_general, punto_especifico, carnet, texto)
        self.actualizar_tabla_segmentos()

        # Terminar proceso de transcripción automaticamnete
        if len(self.archivos) == 0:
            self.mostrar_reportes()   

    def actualizar_tabla_segmentos(self):
        # Olvidar elementos de la interfaz
        for widget in self.winfo_children():
            widget.grid_forget()

        # Mostrar elementos de la interfaz
        self.tabla_segmentos(self.archivos)

    def mostar_tabla_segmentos(self):
        archivos = seleccionar_carpeta_segmentos(self.ruta_texto)
        self.archivos = archivos # Guardar los archivos para usarlos en otros métodos.
        self.tabla_segmentos(self.archivos)


        # Olvidar botones y entry de la interfaz
        self.boton_seleccionar_archivo.grid_forget()
        self.ruta_texto.grid_forget()
        self.advertencia.grid_forget()
        self.boton_old_proyecto.grid_forget()
        self.ruta_op.grid_forget()

    def tabla_segmentos(self, archivos):
        #NOTA : Agregar label para la tabla

        contenedor_tabla = tk.Frame(self)
        contenedor_tabla.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        self.tabla = ttk.Treeview(contenedor_tabla, height=10)
        self.tabla["columns"] = ("Archivo")

        self.tabla.column("#0", width=0, stretch=tk.NO)
        self.tabla.column("Archivo", anchor=tk.W, width=400)

        self.tabla.heading("#0", text="")
        self.tabla.heading("Archivo", text="Segmentos de audio")

        for archivo in archivos:
            self.tabla.insert("", tk.END, text="", values=(archivo))

        self.tabla.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.tabla.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        # Botón para iniciar la transcripción
        self.boton_transcribir = tk.Button(self, text="Transcribir", state=tk.DISABLED,
                                           command=self.transcribir_audio_seleccionado)
        self.boton_transcribir.grid(row=4, column=0, padx=10, pady=10)
        self.boton_transcribir.config(width=20, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")

        # Botón para iniciar la transcripción
        self.boton_ver_reportes = tk.Button(self, text="Finalizar",
                                           command=self.mostrar_reportes)
        self.boton_ver_reportes.grid(row=4, column=3, padx=10, pady=10)
        self.boton_ver_reportes.config(width=20, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")
        
        #Etiqueta y botón para continuar el proyecto después.
        self.boton_continuar_después = tk.Button(self, text="Continuar después",
                                                   command=self.continuar_mas_tarde)
        self.boton_continuar_después.grid(row=5, column=0, padx=5, pady=5,columnspan=2)
        self.boton_continuar_después.config(width=30, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")

        self.ruta_cd = tk.Text(self, height=0, width=30)
        self.ruta_cd.grid(row=6, column=0, columnspan=2, padx=5, pady=10)
        self.ruta_cd.config(width = 50 , font = ("arial",12, ))

    def on_item_selected(self, event = None):
        item = self.tabla.selection()

        if item:
            self.boton_transcribir.config(state=tk.NORMAL)
        else:
            self.boton_transcribir.config(state=tk.DISABLED)

    def transcribir_audio_seleccionado(self):
        selected_item = self.tabla.focus()
        if selected_item:
            archivo_seleccionado = self.tabla.item(selected_item)["values"][0]
            ruta_corregida = corregir_ruta_archivo(archivo_seleccionado)
            texto_transcrito = convertir_audio_a_texto(ruta_corregida)
            self.almacenar_información(texto_transcrito)
            eliminar_segmento_usado(archivo_seleccionado,self.archivos)

    def mostrar_reportes(self):
        ventana_reportes = VentanaReportes(self)  # Crear la ventana de reportes
        ventana_reportes.mainloop()  # Iniciar el bucle de la interfaz


# Reportes no necesarios. 
class VentanaReportes(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reportes")
        self.geometry("700x500")

        # Crear la barra de menú
        barra_menu = tk.Menu(self)
        
        # Crear los comandos de menú y asociarlos a los frames correspondientes
        barra_menu.add_command(label="Frame 1", command=self.mostrar_frame1)
        barra_menu.add_command(label="Frame 2", command=self.mostrar_frame2)
        barra_menu.add_command(label="Frame 3", command=self.mostrar_frame3)
        
        # Asignar la barra de menú a la ventana
        self.config(menu=barra_menu)
        
        # Frame actualmente visible
        self.frame_actual = None
        
        # Mostrar un frame inicial
        self.mostrar_frame1()
        
    def mostrar_frame1(self):
        if self.frame_actual is not None:
            self.frame_actual.destroy()
        
        self.frame_actual = Frame1(self)
        self.frame_actual.pack(fill=tk.BOTH, expand=True)

    def mostrar_frame2(self):
        if self.frame_actual is not None:
            self.frame_actual.destroy()
        
        self.frame_actual = Frame2(self)
        self.frame_actual.pack(fill=tk.BOTH, expand=True)

    def mostrar_frame3(self):
        if self.frame_actual is not None:
            self.frame_actual.destroy()
        
        self.frame_actual = Frame3(self)
        self.frame_actual.pack(fill=tk.BOTH, expand=True)

class Frame1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear el widget Listbox
        listbox = tk.Listbox(self, width=40)
        listbox.grid(row=0, column=0, sticky="nsew")

        # Crear el widget Scrollbar
        scrollbar = tk.Scrollbar(self, command=listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Asociar el Listbox con el Scrollbar
        listbox.config(yscrollcommand=scrollbar.set)

        # Agregar elementos a la lista
        for item in reporte:
            listbox.insert(tk.END, item)

        # Crear el botón "Finalizar"
        boton_finalizar = tk.Button(self, text="Salir")
        boton_finalizar.grid(row=1, column=0, padx=10, pady=10, sticky="sw")

        # Crear el botón "Regresar"
        boton_regresar = tk.Button(self, text="Regresar")
        boton_regresar.grid(row=1, column=1, padx=10, pady=10, sticky="se")

        # Configurar el tamaño de las filas y columnas
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

class Frame2(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear el widget Listbox
        listbox = tk.Listbox(self, width=40)
        listbox.grid(row=0, column=0, sticky="nsew")

        # Crear el widget Scrollbar
        scrollbar = tk.Scrollbar(self, command=listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Asociar el Listbox con el Scrollbar
        listbox.config(yscrollcommand=scrollbar.set)

        # Agregar elementos a la lista
        for carnet in personas:
            total_palabras = personas[carnet]["t_palabras"]
            total_palabras = str(total_palabras)
            nombre = personas[carnet]["nombre"]
            listbox.insert(tk.END, nombre + " -> Total de palabras: " + total_palabras + "\n")

        # Crear el botón "Finalizar"
        boton_finalizar = tk.Button(self, text="Salir")
        boton_finalizar.grid(row=1, column=0, padx=10, pady=10, sticky="sw")

        # Crear el botón "Regresar"
        boton_regresar = tk.Button(self, text="Regresar")
        boton_regresar.grid(row=1, column=1, padx=10, pady=10, sticky="se")

        # Configurar el tamaño de las filas y columnas
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)


class Frame3(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Crear el widget Listbox
        listbox = tk.Listbox(self, width=40)
        listbox.grid(row=0, column=0, sticky="nsew")

        # Crear el widget Scrollbar
        scrollbar = tk.Scrollbar(self, command=listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Asociar el Listbox con el Scrollbar
        listbox.config(yscrollcommand=scrollbar.set)

        # Agregar elementos a la lista
        for carnet in personas:
           nombre = personas[carnet]["nombre"]
           for punto_general in personas[carnet]:
                if punto_general == "nombre" or punto_general == "t_palabras":
                    continue
                else:
                    for punto_especifico in personas[carnet][punto_general]:
                        contador = personas[carnet][punto_general][punto_especifico]
                        contador = str(contador)
                        listbox.insert(tk.END, nombre + " -> " + punto_general + " -> " + punto_especifico + " Total de participaciones " +contador  )
               
        # Crear el botón "Finalizar"
        boton_finalizar = tk.Button(self, text="Salir")
        boton_finalizar.grid(row=1, column=0, padx=10, pady=10, sticky="sw")

        # Crear el botón "Regresar"
        boton_regresar = tk.Button(self, text="Regresar")
        boton_regresar.grid(row=1, column=1, padx=10, pady=10, sticky="se")

        # Configurar el tamaño de las filas y columnas
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)