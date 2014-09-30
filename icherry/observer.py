

# Observer abstracto. No instanciar
class Observer():
    def __init__(self):
        raise NotImplementedError("Clase abstracto")


    def update(self, unObservable):
        raise NotImplementedError("Método abstracto")



# Observable abstracto. No instanciar
class Observable():
    def __init__(self):
        self.__observers = set()


    def registrarObserver(self, unObserver):
        self.__observers.add(unObserver)


    def eliminarObserver(self, unObserver):
        self.__observers.remove(unObserver)


    def notificarCambios(self):
        for observer in self.__observers:
            observer.update(self)
