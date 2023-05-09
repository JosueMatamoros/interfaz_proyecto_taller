import tkinter as tk
from tkinter import ttk 
from loigica import puntos_agenda, agenda

def barra_menu(ventana):
    barra_menu = tk.Menu(ventana)
    ventana.config(menu=barra_menu)

    menu_agenda = tk.Menu(barra_menu, tearoff=0) #Objeto para agenda.
    barra_menu.add_cascade(label="Agenda", menu=menu_agenda)

    menu_agenda.add_command(label="Agregar punto a la agenda")
    menu_agenda.add_command(label="Eliminar punto a la agenda")
    menu_agenda.add_command(label="Salir", command=ventana.destroy)

    barra_menu.add_cascade(label="Participantes", menu=menu_agenda)
    #se debe agaragar objeto y comando para participantes
    barra_menu.add_cascade(label="Divisor de audio", menu=menu_agenda)
    #Lo mismo para el divisor de audio

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
                                bg="green", fg="white", cursor="hand2")
        self.boton_nuevo.grid(row=2, column=0, padx=10, pady=10)
       
        self.boton_guardar= tk.Button(self, text="Guardar", command= self.guardar_punto)
        self.boton_guardar.config(width = 20, font = ("arial",12, "bold"),
                                  bg="blue", fg="white", cursor="hand2")
        self.boton_guardar.grid(row=2, column=1, padx=10, pady=10)
      
        self.boton_cancelar= tk.Button(self, text="Cancelar",command=self.deshabilitar_campos)
        self.boton_cancelar.config(width = 20, font = ("arial",12, "bold"),
                                   bg="red", fg="white", cursor="hand2")
        self.boton_cancelar.grid(row=2, column=2, padx=10, pady=10)
        
        #Boton para editar tabla
        self.boton_editar = tk.Button(self, text="Editar",state=tk.DISABLED, command=self.editar_punto_ventana)
        self.boton_editar.config(width = 20, font = ("arial",12, "bold"),
                                    bg="green", fg="white", cursor="hand2")
        self.boton_editar.grid(row=4, column=0, padx=10, pady=10)

        #Boton para eliminar contenido de la tabla
        self.boton_eliminar = tk.Button(self, text="Eliminar", command=self.eliminar_punto_ventana, state=tk.DISABLED)
        self.boton_eliminar.config(width = 20, font = ("arial",12, "bold"),
                                    bg="red", fg="white", cursor="hand2")
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
        self.eliminar_punto_diccionario(punto_general, punto_especifico, agenda)
        self.tabla_puntos(agenda)

    def eliminar_punto_diccionario(self, punto_general, punto_especifico,diccionario):
        if punto_general in diccionario and punto_especifico in diccionario[punto_general]:
            diccionario[punto_general].remove(punto_especifico)
            if len(diccionario[punto_general]) == 0:
                del diccionario[punto_general]
        
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

        
    

      