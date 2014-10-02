import npyscreen
import prettytable
import icherry.magnitudes as magnitudes
import icherry.plan_maestro as plan_maestro

class EstadoPantallaVisibilidad():

    def dibujar(self, unaPantalla):
        pass


class EstadoPantallaVisible(EstadoPantallaVisibilidad):

    def dibujar(self, unaPantalla):
        unaPantalla.display()


class EstadoPantallaOculta(EstadoPantallaVisibilidad):

    def dibujar(self, unaPantalla):
        pass


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
            menu, 'MENU_EDITAR_ESTADO_FENOLOGICO', 'EDICION_ESTADO_FENOLOGICO')
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

        self._estadoVisibilidad = EstadoPantallaOculta()
        self._estadoDePlanta.registrarObserver(self)

        super(PantallaDeEstadoDePlantaMVC, self).__init__(
            name=proveedorDeTexto.obtener("SCREEN_ESTADO_PLANTA"), **kargs)

    def beforeEditing(self):

        self._estadoVisibilidad = EstadoPantallaVisible()

    def afterEditing(self):

        self._estadoVisibilidad = EstadoPantallaOculta()
        self.parentApp.setNextForm('MAIN')

    def create(self):

        self._wPager = self.add(npyscreen.Pager)

    def actualizar(self, unSensor):

        self._wPager.values = self.render()
        self._estadoVisibilidad.dibujar(self)

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

        self._estadoVisibilidad = EstadoPantallaOculta()

        self._sensorDeTemperatura.registrarObserver(self)
        self._sensorDeHumedad.registrarObserver(self)
        self._sensorDeAcidez.registrarObserver(self)

        super(PantallaDeSensoresMVC, self).__init__(
            name=proveedorDeTexto.obtener("SCREEN_SENSORES"), **kargs)

    def beforeEditing(self):

        self._estadoVisibilidad = EstadoPantallaVisible()

    def afterEditing(self):

        self._estadoVisibilidad = EstadoPantallaOculta()
        self.parentApp.setNextForm('MAIN')

    def create(self):

        self._wPager = self.add(npyscreen.Pager)

    def actualizar(self, unSensor):

        self._wPager.values = self.render()
        self._estadoVisibilidad.dibujar(self)

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

        self._estadoVisibilidad = EstadoPantallaOculta()
        self._central.registrarObserver(self)

        super(PantallaDeCentralMVC, self).__init__(
            name=proveedorDeTexto.obtener('SCREEN_CENTRAL_METEOROLOGICA'), **kargs)

    def beforeEditing(self):

        self._estadoVisibilidad = EstadoPantallaVisible()

    def afterEditing(self):

        self._estadoVisibilidad = EstadoPantallaOculta()
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
        self._estadoVisibilidad.dibujar(self)

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


class PantallaDeEdicionDeEstadoFenologico(npyscreen.ActionForm):

    def __init__(self, proveedorDeTexto, estadoFenologico, **kargs):

        self._proveedorDeTexto = proveedorDeTexto
        self._estadoFenologico = estadoFenologico

        super(PantallaDeEdicionDeEstadoFenologico, self).__init__(
            name=proveedorDeTexto.obtener('SCREEN_EDICION_ESTADO'), **kargs)

    def beforeEditing(self):

        self._wEstadio.value = plan_maestro.CicloDeVida.estadios().index(self._estadoFenologico.estadioDeCultivo())
        self._wAltura.value = str(self._estadoFenologico.altura().valor())
        self._wBrotes.value = str(self._estadoFenologico.cantidadBrotes())
        self._wFlores.value = str(self._estadoFenologico.cantidadFlores())
        self._wFrutos.value = str(self._estadoFenologico.cantidadFrutos())
        self._wMaduras.value = str(self._estadoFenologico.porcentajeFrutasMaduras().valor())

    def on_cancel(self):

        self.parentApp.setNextForm('MAIN')

    def on_ok(self):

        try:
            self._estadoFenologico.estadioDeCultivo(plan_maestro.CicloDeVida.estadios()[self._wEstadio.value])
            self._estadoFenologico.altura(magnitudes.LongitudEnCentimetros(int(self._wAltura.value)))
            self._estadoFenologico.cantidadBrotes(int(self._wBrotes.value))
            self._estadoFenologico.cantidadFlores(int(self._wFlores.value))
            self._estadoFenologico.cantidadFrutos(int(self._wFrutos.value))
            self._estadoFenologico.porcentajeFrutasMaduras(magnitudes.Porcentaje(int(self._wMaduras.value)))

        except Exception as err:
            npyscreen.notify_confirm("Error: {0}".format(err))

        else:
            self.parentApp.setNextForm('MAIN')

    def create(self):

        proveedorDeTexto = self._proveedorDeTexto

        self._wEstadio = self.add(
            npyscreen.TitleMultiLine,
            max_height=8,
            name=proveedorDeTexto.obtener("INPUT_ESTADIO"),
            values=[e.nombre() for e in plan_maestro.CicloDeVida.estadios()])

        self._wAltura = self.add(npyscreen.TitleText, name=proveedorDeTexto.obtener("INPUT_ALTURA"))
        self._wBrotes = self.add(npyscreen.TitleText, name=proveedorDeTexto.obtener("INPUT_CANT_BROTES"))
        self._wFlores = self.add(npyscreen.TitleText, name=proveedorDeTexto.obtener("INPUT_CANT_FLORES"))
        self._wFrutos = self.add(npyscreen.TitleText, name=proveedorDeTexto.obtener("INPUT_CANT_FRUTOS"))
        self._wMaduras = self.add(npyscreen.TitleText, name=proveedorDeTexto.obtener("INPUT_FRUTAS_MADURAS"))
