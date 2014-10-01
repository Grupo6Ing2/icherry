

# Observer abstracto. No instanciar
class Observer():

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def actualizar(self, unObservable):
        raise NotImplementedError("Método abstracto")


# Observable abstracto. No instanciar
class Observable():

    def __init__(self):
        self.__observers = set()

    def registrarObserver(self, unObserver):
        self.__observers.add(unObserver)

    def eliminarObserver(self, unObserver):
        self.__observers.remove(unObserver)

    def notificarObservers(self):
        for observer in self.__observers:
            observer.actualizar(self)
