import npyscreen
import prettytable


class ICherryCurses(npyscreen.NPSAppManaged):
    pass


class PantallaEnConstruccion(npyscreen.Form):

    def __init__(self, proveedorDeTexto, **kargs):

        self.proveedorDeTexto = proveedorDeTexto
        super(PantallaEnConstruccion, self).__init__(
            name=proveedorDeTexto.obtener("EN_CONSTRUCCION"), **kargs)

    def afterEditing(self):

        self.parentApp.setNextForm('MAIN')

    def create(self):

        self.add(npyscreen.Pager, values=[self.proveedorDeTexto.obtener(
            "EN_CONSTRUCCION")])


class PantallaDeInicio(npyscreen.FormWithMenus):

    def __init__(self, proveedorDeTexto, archivoFondoAscii='', **kargs):

        if (archivoFondoAscii):
            with open(archivoFondoAscii, 'r') as archivo:
                self.fondoAscii = archivo.read()
        else:
            self.fondoAscii = proveedorDeTexto.obtener("BIENVENIDO")

        self.proveedorDeTexto = proveedorDeTexto
        super(PantallaDeInicio, self).__init__(
            name=proveedorDeTexto.obtener("NOMBRE_APLICACION"), **kargs)

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
            menu, 'MENU_ESTADO_PLANTA', 'ESTADO')
        self._agregarEntradaDeMenu(
            menu, 'MENU_EDITAR_ESTADO_FENOLOGICO', 'EN_CONSTRUCCION')
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


class PantallaDeEstadoDePlantaMVC(npyscreen.Form):

    def __init__(self, proveedorDeTexto, estadoDePlanta, **kargs):

        self._estadoDePlanta = estadoDePlanta
        self._proveedorDeTexto = proveedorDeTexto

        super(PantallaDeEstadoDePlantaMVC, self).__init__(
            name=proveedorDeTexto.obtener("SCREEN_ESTADO_PLANTA"), **kargs)

    def beforeEditing(self):

        self._estadoDePlanta.registrarObserver(self)

    def afterEditing(self):

        self._estadoDePlanta.eliminarObserver(self)
        self.parentApp.setNextForm('MAIN')

    def create(self):

        self._wPager = self.add(npyscreen.Pager)

    def actualizar(self, unSensor):

        self._wPager.values = self.render()
        self.display()

    def render(self):
        return [
            self._proveedorDeTexto.obtener('ESTADO_SALUD') + ':',
            '',
            self._estadoDePlanta.estadoDeSalud().nombre(),
            '',
            self._proveedorDeTexto.obtener('CONDICION_SALUD') + ':',
            '',
            self._proveedorDeTexto.obtener(
                "SPAN_TEMPERATURA", self._estadoDePlanta.temperatura().valor()),
            self._proveedorDeTexto.obtener(
                "SPAN_HUMEDAD", self._estadoDePlanta.humedad().valor().valor()),
            self._proveedorDeTexto.obtener(
                "SPAN_ACIDEZ", self._estadoDePlanta.acidez().valor()),
            '',
            self._proveedorDeTexto.obtener("HEADER_ESTADO_FENOLOGICO"),
            '',
            self._proveedorDeTexto.obtener("SPAN_ESTADIO",
                self._estadoDePlanta.estadoFenologico().estadioDeCultivo().nombre()),
            self._proveedorDeTexto.obtener("SPAN_ALTURA",
                self._estadoDePlanta.estadoFenologico().altura()),
            self._proveedorDeTexto.obtener("SPAN_CANT_BROTES",
                self._estadoDePlanta.estadoFenologico().cantidadBrotes()),
            self._proveedorDeTexto.obtener("SPAN_CANT_FLORES",
                self._estadoDePlanta.estadoFenologico().cantidadFlores()),
            self._proveedorDeTexto.obtener("SPAN_CANT_FRUTOS",
                self._estadoDePlanta.estadoFenologico().cantidadFrutos()),
            self._proveedorDeTexto.obtener("SPAN_PORCENTAJE_FRUTAS_MADURAS",
                self._estadoDePlanta.estadoFenologico().porcentajeFrutasMaduras().valor()),
        ]


class PantallaDeSensoresMVC(npyscreen.Form):

    def __init__(self,
                 proveedorDeTexto,
                 sensorDeTemperatura,
                 sensorDeHumedad,
                 sensorDeAcidez, **kargs):

        self._sensorDeTemperatura = sensorDeTemperatura
        self._sensorDeHumedad = sensorDeHumedad
        self._sensorDeAcidez = sensorDeAcidez
        self._proveedorDeTexto = proveedorDeTexto

        self.enPantalla = True

        super(PantallaDeSensoresMVC, self).__init__(
            name=proveedorDeTexto.obtener("SCREEN_SENSORES"), **kargs)

    def beforeEditing(self):

        self._sensorDeTemperatura.registrarObserver(self)
        self._sensorDeHumedad.registrarObserver(self)
        self._sensorDeAcidez.registrarObserver(self)

    def afterEditing(self):

        self._sensorDeTemperatura.eliminarObserver(self)
        self._sensorDeHumedad.eliminarObserver(self)
        self._sensorDeAcidez.eliminarObserver(self)

        self.parentApp.setNextForm('MAIN')

    def create(self):

        self._wPager = self.add(npyscreen.Pager)

    def actualizar(self, unSensor):

        self._wPager.values = self.render()
        self.display()

    def render(self):
        return [
            self._proveedorDeTexto.obtener(
                "SPAN_TEMPERATURA", self._sensorDeTemperatura.ultimoValorSensado().valor()),
            self._proveedorDeTexto.obtener(
                "SPAN_HUMEDAD", self._sensorDeHumedad.ultimoValorSensado().valor().valor()),
            self._proveedorDeTexto.obtener(
                "SPAN_ACIDEZ", self._sensorDeAcidez.ultimoValorSensado().valor()),
        ]


class PantallaDeCentralMVC(npyscreen.Form):

    def __init__(self, proveedorDeTexto, central, **kargs):

        self._proveedorDeTexto = proveedorDeTexto
        self._central = central
        super(PantallaDeCentralMVC, self).__init__(
            name=proveedorDeTexto.obtener('SCREEN_CENTRAL_METEOROLOGICA'), **kargs)

    def beforeEditing(self):

        self._central.registrarObserver(self)
        self._ultimoPronostico = None

    def afterEditing(self):

        self._central.eliminarObserver(self)
        self.parentApp.setNextForm('MAIN')

    def _obtenerTextoFechaYHora(self, fechaYHora):

        return self._proveedorDeTexto.obtener(
            'FORMAT_FECHAYHORA', fechaYHora.fecha(), fechaYHora.hora())

    def _crearTablaPronostico(self):

        cantHoras = 24
        proveedorDeTexto = self._proveedorDeTexto

        fechaYHora = self._central.ultimaFechaYHora()
        pronostico = self._central.ultimoPronostico()

        tabla = prettytable.PrettyTable([
            proveedorDeTexto.obtener("HEADER_FECHA"),
            proveedorDeTexto.obtener("HEADER_TEMPERATURA"),
            proveedorDeTexto.obtener("HEADER_HUMEDAD"),
            proveedorDeTexto.obtener("HEADER_LLUVIA"),
            proveedorDeTexto.obtener("HEADER_LUZ"),
        ])

        for _ in range(cantHoras):
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

    def actualizar(self, unaCentalMeteorologica):

        self._wPager.values = self.render()
        self.display()

    def create(self):

        self._wPager = self.add(npyscreen.Pager)

    def render(self):

        proveedorDeTexto = self._proveedorDeTexto
        textos = []

        fechaYHora = self._central.ultimaFechaYHora()
        textos.append(proveedorDeTexto.obtener(
            'SPAN_FECHAYHORA_ACTUAL',
            self._obtenerTextoFechaYHora(fechaYHora)))

        textos.append('')
        textos.append(proveedorDeTexto.obtener('SPAN_PRONOSTICO_24_HORAS'))
        textos = textos + self._crearTablaPronostico().get_string().split("\n")
        return textos
