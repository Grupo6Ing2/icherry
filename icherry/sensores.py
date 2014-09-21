class Sensor():

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def sensar(self):
        raise NotImplementedError("Metodo abstracto")


class SensorTemperatura():

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def sensar(self):
        raise NotImplementedError("Metodo abstracto")


class SensorHumedad():

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def sensar(self):
        raise NotImplementedError("Metodo abstracto")


class SensorAcidez():   

    def __init__(self):
        raise NotImplementedError("Clase abstracta")

    def sensar(self):
        raise NotImplementedError("Metodo abstracto")


class SensorHumedadUSB():

    def __init__(self, puertoUSB):
        raise NotImplementedError("Not implemented yet")

    def sensar(self):
        raise NotImplementedError("Not implemented yet")


class SensorTemperaturaUSB():

    def __init__(self, puertoUSB):
        raise NotImplementedError("Not implemented yet")

    def sensar(self):
        raise NotImplementedError("Not implemented yet")


class SensorAcidezUSB():

    def __init__(self, puertoUSB):
        raise NotImplementedError("Not implemented yet")

    def sensar(self):
        raise NotImplementedError("Not implemented yet")


class SensorAcidezSimulado():

    def __init_(self, acidezEnPh):
        self.acidezEnPh = acidezEnPh
        return self

    def sensar(self):
        return self.acidezEnPh

    def setAcidez(acidezEnPh):
        self.acidezEnPh = acidezEnPh
        return self

class SensorTemperaturaSimulado():

    def __init_(self, temperaturaEnCentigrados):
        self.temperaturaEnCentigrados = temperaturaEnCentigrados

    def sensar(self):
        return self.temperaturaEnCentigrados

    def setTemperatura(temperaturaEnCentigrados):
        self.temperaturaEnCentigrados = temperaturaEnCentigrados


class SensorHumedadSimulado():

    def __init_(self, humedadRelativa):
        self.humedadRelativa = humedadRelativa

    def sensar(self):
        return self.humedadRelativa

    def setHumedad(humedadRelativa):
        self.humedadRelativa = humedadRelativa

