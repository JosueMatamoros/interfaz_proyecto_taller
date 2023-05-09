
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