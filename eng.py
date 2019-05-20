
class Encabezado(object):
    archivo = "File"
    nuevo = "New"
    abrir = "Open"
    guardar = "Save"
    guardarComo = "Save as..."
    cerrar = "Close"
    ayuda = "Help"
    acerca = "About..."
    idiomas= "Language"
    espanol="Spanish"
    ingles = "English"

class Vehicle:
    name = ""
    tires = 4


class Car(Vehicle):
    def __init__(self, name, tires):
        self.name = name
        self.tires = tires


mi_carro = Car(tires=4, name='mitsubishi')


def render(palabra, lenguaje):
    return languages[lenguaje][palabra]

languages = {
    'ES': {
        'archivo': "Archivo",
        'nuevo': "New",
        'abrir': "Open",
        'guardar': "Save",
        'guardarComo': "Save as...",
        'cerrar': "Close",
        'ayuda': "Help",
        'acerca': "About...",
        'idiomas': "Language",
        'espanol': "Spanish",
        'ingles': "English",
    },
    'EN': {
        'archivo': "File",
        'nuevo': "New",
        'abrir': "Open",
        'guardar': "Save",
        'guardarComo': "Save as...",
        'cerrar': "Close",
        'ayuda': "Help",
        'acerca': "About...",
        'idiomas': "Language",
        'espanol': "Spanish",
        'ingles': "English",
    }
}