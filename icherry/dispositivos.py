class DispositivoDeLectura():

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def leer(self):
        raise NotImplementedError("Método abstracto")


class DispositivosDeLecturaArchivo(DispositivoDeLectura):

    def __init__(self, unNombreArchivo):
        self.archivo = open(unNombreArchivo, 'r')

    def leer(self):
        self.archivo.seek(0)
        return self.archivo.read()


class DispositivoDeEscritura():

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def escribir(self):
        raise NotImplementedError("Método abstracto")


class DispositivoDeEscrituraArchivo(DispositivoDeEscritura):

    def __init__(self, unNombreArchivo):
        self.archivo = open(unNombreArchivo, 'w')

    def escribir(self, unaCadena):
        return self.archivo.write(unaCadena)
