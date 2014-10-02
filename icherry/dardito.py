
class SpecifiedObservable():
    def __init__(self, data_source, callback_method='update'):
        self.observers = []
        self.data_source = data_source
        self.callback_method = callback_method

    def add(self, observer):
        self.observers.add(observer)

    def remove(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            pass

    def notify():
        for observer in self.observers:
            getattr(observer, self.callback_method)(self.data_source)

class SpecifiedObserver():
    def __init__(self, observer1, observer2):
        observer1.add(self)
        observer2.add(self)

    def update_for_1_specified(self, data_source):
        pass

    def update(self, data_source):
        pass

data_source1 = SomeObject()
data_source2 = SomeOtherObject()
observable1 = SpecifiedObservable(data_source1, 'update_for_1_specified')
observable2 = SpecifiedObservable(data_source2)
observer = SpecifiedObserver(observable1, observable2)
