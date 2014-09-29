import npyscreen
import prettytable


class ICherryCurses(npyscreen.NPSAppManaged):
    pass


class PantallaEnConstruccion(npyscreen.Form):

    def __init__(self, proveedorDeTexto):
        self.proveedorDeTexto = proveedorDeTexto
        super(PantallaEnConstruccion, self).__init__(
            name=proveedorDeTexto.obtener("EN_CONSTRUCCION"))

    def afterEditing(self):
        self.parentApp.setNextForm('MAIN')

    def create(self):
        self.add(npyscreen.TitleText, name=self.proveedorDeTexto.obtener(
            "EN_CONSTRUCCION"), editable=False)


class PantallaDeInicio(npyscreen.FormWithMenus):

    def __init__(self, proveedorDeTexto, archivoFondoAscii=''):

        if (archivoFondoAscii):
            with open(archivoFondoAscii, 'r') as archivo:
                self.fondoAscii = archivo.read()
        else:
            self.fondoAscii = proveedorDeTexto.obtener("BIENVENIDO")

        self.proveedorDeTexto = proveedorDeTexto
        super(PantallaDeInicio, self).__init__(
            name=proveedorDeTexto.obtener("NOMBRE_APLICACION"))

    def _agregarEntradaDeMenu(self, menu, texto, pantallaObjetivo):
        menu.addItem(
            text=self.proveedorDeTexto.obtener(texto),
            onSelect=lambda: self.parentApp.switchForm(pantallaObjetivo))

    def _agregarSeparacionDeMenu(self, menu):
        menu.addItem(text='')

    def _crearMenu(self):
        menu = self.new_menu(
            name=self.proveedorDeTexto.obtener('MENU_OPCIONES'))

        self._agregarEntradaDeMenu(
            menu, 'MENU_SENSORES', 'SENSORES')
        self._agregarEntradaDeMenu(
            menu, 'MENU_ESTADO_SALUD', 'EN_CONSTRUCCION')
        self._agregarEntradaDeMenu(
            menu, 'MENU_CONFIGURAR_PLAN_MAESTRO', 'EN_CONSTRUCCION')
        self._agregarEntradaDeMenu(
            menu, 'MENU_PROGRAMA_SUMINISTROS', 'EN_CONSTRUCCION')
        self._agregarEntradaDeMenu(
            menu, 'MENU_CENTRAL_METEOROLOGICA', 'CENTRAL')
        self._agregarEntradaDeMenu(
            menu, 'MENU_HISTORIAL_SENSORES', 'EN_CONSTRUCCION')
        self._agregarEntradaDeMenu(
            menu, 'MENU_HISTORIAL_SUMINISTROS', 'EN_CONSTRUCCION')
        self._agregarSeparacionDeMenu(menu)
        self._agregarEntradaDeMenu(
            menu, 'MENU_SALIR', None)

    def create(self):

        self.add(npyscreen.Pager, values=self.fondoAscii.split("\n"))
        self._crearMenu()


class PantallaDeSensores(npyscreen.Form):

    def __init__(self,
                 proveedorDeTexto,
                 sensorDeTemperatura,
                 sensorDeHumedad,
                 sensorDeAcidez):

        self.sensorDeTemperatura = sensorDeTemperatura
        self.sensorDeHumedad = sensorDeHumedad
        self.sensorDeAcidez = sensorDeAcidez
        self.proveedorDeTexto = proveedorDeTexto
        super(PantallaDeSensores, self).__init__(
            name=proveedorDeTexto.obtener("SCREEN_SENSORES"))

    def afterEditing(self):
        self.parentApp.setNextForm('MAIN')

    def create(self):
        textos = [
            self.proveedorDeTexto.obtener(
                "SPAN_TEMPERATURA", self.sensorDeTemperatura.sensar().valor()),
            self.proveedorDeTexto.obtener(
                "SPAN_HUMEDAD", self.sensorDeHumedad.sensar().valor().valor()),
            self.proveedorDeTexto.obtener(
                "SPAN_ACIDEZ", self.sensorDeAcidez.sensar().valor()),
        ]
        self.add(npyscreen.Pager, values=textos)


class PantallaDeCentral(npyscreen.Form):

    def __init__(self, proveedorDeTexto, central):
        self.proveedorDeTexto = proveedorDeTexto
        self.central = central
        super(PantallaDeCentral, self).__init__(name='Central')

    def afterEditing(self):
        self.parentApp.setNextForm('MAIN')

    def _obtenerTextoFechaYHora(self, fechaYHora):
        return self.proveedorDeTexto.obtener(
            'FORMAT_FECHAYHORA', fechaYHora.fecha(), fechaYHora.hora())

    def _crearTablaPronostico(self):

        proveedorDeTexto = self.proveedorDeTexto

        fechaYHora = self.central.obtenerFechaYHora()
        pronostico = self.central.obtenerPronostico(fechaYHora, 24)

        tabla = prettytable.PrettyTable([
            proveedorDeTexto.obtener("HEADER_FECHA"),
            proveedorDeTexto.obtener("HEADER_TEMPERATURA"),
            proveedorDeTexto.obtener("HEADER_HUMEDAD"),
            proveedorDeTexto.obtener("HEADER_LUZ"),
            proveedorDeTexto.obtener("HEADER_LLUVIA"),
        ])

        for _ in range(0, 23):
            prediccion = pronostico.prediccionPara(fechaYHora)
            tabla.add_row([
                self._obtenerTextoFechaYHora(prediccion.lapso().desde()),
                prediccion.temperatura().valor(),
                prediccion.humedad().valor().valor(),
                prediccion.probabilidadDeLluvia().valor(),
                prediccion.luzAmbiente().valor()
            ])
            fechaYHora = fechaYHora.agregarHoras(1)

        return tabla

    def create(self):

        proveedorDeTexto = self.proveedorDeTexto
        textos = []

        fechaYHora = self.central.obtenerFechaYHora()
        textos.append(proveedorDeTexto.obtener(
            'SPAN_FECHAYHORA_ACTUAL',
            self._obtenerTextoFechaYHora(fechaYHora)))

        textos.append(proveedorDeTexto.obtener('SPAN_PRONOSTICO_24_HORAS'))
        textos = textos + self._crearTablaPronostico().get_string().split("\n")

        self.add(npyscreen.Pager, values=textos)
