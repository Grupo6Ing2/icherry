from icherry.magnitudes import Rango
from icherry.programa_suministro import AccionProgramada, ProgramaDeSuministro
from icherry.tiempo import FechaYHora
from datetime import date,time,timedelta

import unittest

# Este test debería funcionar independientemente de qué día es el
# '_dia0'. La hora no interesa, sólamente nos desplazamos en la
# dimensión de las fechas, no de las horas. Usamos timedelta para eso.
# La primera versión directamente usaba números en lugar de
# 'FechaYHora' como "horario" para las acciones programadas.

_dia0 = date(666,11,10)         # \m/ Jason está cerca.
_hora = time(0,0,0)

# con esta función nos desligamos de las FechaYHora y simplemente
# pensamos en términos de un índice (0 es el '_día0').
def diaN(n):
    # contando desde 0
    return FechaYHora(_dia0 + timedelta(days=n), _hora)

# una lista de pares para interpretar como lista de acciones. Lo único
# que realmente interesa son los horarios (que en este caso son
# instancias de fechaYHora, pero incluso podrían ser números (como fue
# la primera versión de este test)), las 'acciones' las suplantamos
# con cualquier banana (magia del mundo dinámico) porque no hacen nada
# por ahora.
_lista = [(diaN(0), 'primera'),
          (diaN(1), 'segunda'),
          (diaN(2), 'tercera'),
          (diaN(3), 'cuarta'),
          (diaN(4), 'quinta'),
          (diaN(5), 'sexta')]

# el lapso en el que trabajamos (alcanza con que abarque a los
# horarios de la lista, puede tener exceso).
_lapso = Rango(diaN(-2),diaN(8))

class TestProgramaDeSuministros(unittest.TestCase):
    # def sortAccionesProgramadas(self, lista):
    #     return sorted(lista)

    def accionesProgramadas2tuplas(self, lista):
        return [(aP.fechaYHora(),aP.accion()) for aP in lista]

    def chk_accionesProgramadas(self, programa, lista1):
        """verifica que la lista de acciones programadas, ordenadas por
        horario, es igual que la lista pasada como argumento.

        """
        lista2 = [(aP.fechaYHora(),aP.accion()) for aP in
             programa.accionesProgramadas()]
        self.assertEqual(lista1, lista2)

    def test_inicializacion(self):
        """este test prueba varias formas alternativas de construir un mismo
        programa de suministro.

        """
        # primera ('programar()')
        p = ProgramaDeSuministro(_lapso)
        l = _lista
        for x in l:
            p.programar(AccionProgramada(*x))
        self.chk_accionesProgramadas(p,l)

        # segunda ('programarAccion')
        p = ProgramaDeSuministro(_lapso)
        for x in l:
            p.programarAccion(*x)
        self.chk_accionesProgramadas(p,l)

        # tercera (por constructor)
        p = ProgramaDeSuministro(_lapso,
                                 [AccionProgramada(*x) for x in l])
        self.chk_accionesProgramadas(p,l)

    def test_acciones_en_horario(self):
        def lapso(desde, hasta):
            return Rango(diaN(desde),diaN(hasta))

        def acciones(desde, hasta):
            # el 'hasta' está incluído
            n = len(_lista)
            if hasta < 0 or desde >= n : return set()
            if desde < 0  : desde = 0
            if hasta >= n : hasta = n - 1
            return set([aP[1] for aP in _lista[desde:hasta+1]])

        def chk_acciones(p,desde,hasta):
            s = set(p.accionesEnHorario(lapso(desde,hasta)))
            self.assertEqual(s, acciones(desde,hasta))

        # ahora sí, iniciamos una pequeña batería de tests
        p = ProgramaDeSuministro(_lapso,
                                 [AccionProgramada(*x) for x in _lista])

        s = set(p.accionesEnHorario(p.lapso()))
        self.assertEqual(s, acciones(0, len(_lista)-1))

        chk_acciones(p,0,2)
        chk_acciones(p,4,20)
        chk_acciones(p,-1,2)
        chk_acciones(p,-2,-1)

    def test_acciones_removidas(self):
        # en este test verificamos que las acciones sean correctamente
        # removidas del programa de suministro. Vamos a usar cualquier
        # fruta como los datos del programa de suministro porque no
        # interesa ya demasiado el tema de las fechas y hora (eso ya
        # lo probamos antes).
        p = ProgramaDeSuministro(Rango(1,10))
        for i in range(1,7):
            p.programarAccion(i,str(i))

        # pequeño sanity check antes de empezar
        self.assertEqual(set(p.accionesEnHorario(p.lapso())),
                         {'1', '2', '3', '4', '5', '6'})

        def chk_remove(rango,accionesRemovidas,accionesFinales):
            """verifica que dado un rango, el programa de suministro encuentre las
            acciones removidas, las remueva y finalmente se quede sólo
            con las acciones finales (ambos argumentos son
            conjuntos)

            """
            self.assertEqual(set(p.accionesEnHorario(rango, remover=True)),
                             accionesRemovidas)
            self.assertEqual(set(p.accionesEnHorario(p.lapso())),
                             accionesFinales)

        # removemos '3' y '4'
        chk_remove(Rango(3,4), {'3','4'}, {'1', '2', '5', '6'})

        # removemos '6,'
        chk_remove(Rango(5.5,100), {'6'}, {'1', '2', '5'})

        # removemos '1' y '2,'
        chk_remove(Rango(-10,2.8), {'1','2'}, {'5'})

        # removemos '5', queda vacío
        chk_remove(Rango(-10,10), {'5'}, set())
