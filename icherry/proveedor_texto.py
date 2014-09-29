import json


class ProveedorDeTexto():

    def __init__(self, nombreArchivo):
        with open(nombreArchivo, 'r') as archivo:
            self.textos = json.loads(archivo.read())

    def obtener(self, clave, *args):
        return self.textos.get(clave, clave).format(*args)
