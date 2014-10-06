
import unittest

from icherry.observer import Observer, Observable


class ObservableMock(Observable):
    def __init__(self):
        super().__init__()

    def realizarAccionObservada(self, valor):
        self.valor = valor
        self.notificarObservers()


class ObserverMock(Observer):
    def __init__(self):
        self.valor = None

    def actualizar(self, unObservable):
        self.valor = unObservable.valor


class TestObserver(unittest.TestCase):

    def test_observable_notifica_los_observers(self):
        observable = ObservableMock()
        observer1 = ObserverMock()
        observer2 = ObserverMock()

        observable.registrarObserver(observer1)
        observable.registrarObserver(observer2)

        observable.realizarAccionObservada(42)

        self.assertEqual(42, observer1.valor)
        self.assertEqual(42, observer2.valor)

    def test_observer_es_eliminado(self):
        observable = ObservableMock()
        observer1 = ObserverMock()
        observer2 = ObserverMock()

        observable.registrarObserver(observer1)
        observable.registrarObserver(observer2)

        observable.realizarAccionObservada(42)
        observable.eliminarObserver(observer2)
        observable.realizarAccionObservada(13)

        self.assertEqual(13, observer1.valor)
        self.assertEqual(42, observer2.valor)
