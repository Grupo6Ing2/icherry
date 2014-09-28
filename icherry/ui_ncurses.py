import npyscreen


class ICherryCurses(npyscreen.NPSAppManaged):
    pass


class PantallaEnConstruccion(npyscreen.Form):

    def __init__(self):
        super(PantallaEnConstruccion, self).__init__(name='En construcción')

    def afterEditing(self):
        self.parentApp.setNextForm('MAIN')

    def create(self):
        self.add(npyscreen.TitleText, name='En construcción', editable=False)


class PantallaDeInicio(npyscreen.FormWithMenus):

    def __init__(self):
        super(PantallaDeInicio, self).__init__(name='iCherry')

    def asciiArt(self):
        # FIXME: poner *bien* esto, en un constructor, etc.
        with open("icherry/main_background_pic.txt") as f:
            r = f.read()
        return r

    def create(self):

        self.add(
            npyscreen.Pager, values=self.asciiArt().split("\n"),
            editable=False)

        menu = self.new_menu(name='Opciones')

        menu.addItem(text='Sensores', onSelect=lambda:
                     self.parentApp.switchForm('SENSORES'))

        menu.addItem(text='Estado de salud', onSelect=lambda:
                     self.parentApp.switchForm('EN_CONSTRUCCION'))

        menu.addItem(text='Configurar Plan Maestro', onSelect=lambda:
                     self.parentApp.switchForm('EN_CONSTRUCCION'))

        menu.addItem(text='Programa de suministros', onSelect=lambda:
                     self.parentApp.switchForm('EN_CONSTRUCCION'))

        menu.addItem(text='Centrar Meteorologica', onSelect=lambda:
                     self.parentApp.switchForm('CENTRAL'))

        menu.addItem(text='Historial de sensores', onSelect=lambda:
                     self.parentApp.switchForm('EN_CONSTRUCCION'))

        menu.addItem(text='Historial de suministros', onSelect=lambda:
                     self.parentApp.switchForm('EN_CONSTRUCCION'))

        menu.addItem(text='')

        menu.addItem(
            text='Salir', onSelect=lambda: self.parentApp.switchForm(None))


class PantallaDeSensores(npyscreen.Form):

    def __init__(self, sensorDeTemperatura, sensorDeHumedad, sensorDeAcidez):
        self.sensorDeTemperatura = sensorDeTemperatura
        self.sensorDeHumedad = sensorDeHumedad
        self.sensorDeAcidez = sensorDeAcidez
        super(PantallaDeSensores, self).__init__(name='Sensores')

    def afterEditing(self):
        self.parentApp.setNextForm('MAIN')

    def create(self):
        self.add(
            npyscreen.TitleText, name="Temperatura:", editable=False,
            value=str(self.sensorDeTemperatura.sensar()))
        self.add(
            npyscreen.TitleText, name="Humedad:", editable=False,
            value=str(self.sensorDeHumedad.sensar()))
        self.add(
            npyscreen.TitleText, name="Acidez:", editable=False,
            value=str(self.sensorDeAcidez.sensar()))


class PantallaDeCentral(npyscreen.Form):

    def __init__(self, central):
        self.central = central
        super(PantallaDeCentral, self).__init__(name='Central')

    def afterEditing(self):
        self.parentApp.setNextForm('MAIN')

    def create(self):
        #TODO deberian ser 24hs, pero los detalles de las 24 no entran en la pantalla (tirra error).
        #cambiar si alguien sabe como hacer scrollbars.
        horas = 18
        fechaYHora = self.central.obtenerFechaYHora()
        pronostico = self.central.obtenerPronostico(fechaYHora, horas)

        self.add(
            npyscreen.TitleText, name="Tiempo:", editable=False,
            value=str(fechaYHora))
        self.add(npyscreen.TitleText, name="Pronostico para las siguientes 24hs:", editable=False)

        t = fechaYHora
        for _ in range(0, horas):
            p = pronostico.prediccionPara(t)
            self.agregarDetallesPrediccion(p)
            t = t.agregarHoras(1)


    def agregarDetallesPrediccion(self, prediccion):
        detalles = "Temperatura: {0}, Humedad: {1}, Prob. Lluvia: {2}, Luz Ambiente: {3}".format(
                prediccion.temperatura(),
                prediccion.humedad(),
                prediccion.probabilidadDeLluvia(),
                prediccion.luzAmbiente())

        self.add(npyscreen.TitleText, name="El pronóstico para {0} es:".format(prediccion.lapso()),
                 editable=False, value=detalles)


