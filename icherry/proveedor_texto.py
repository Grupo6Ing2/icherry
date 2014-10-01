import json


class ProveedorDeTexto():
    """
    Permite obtener textos según una clave especificada.
    Los textos son cargados de un archivo json.
    """

    def __init__(self, nombreArchivo):
        with open(nombreArchivo, 'r') as archivo:
            self.textos = json.loads(archivo.read())

    def obtener(self, clave, *args):
        return self.textos.get(clave, clave).format(*args)
