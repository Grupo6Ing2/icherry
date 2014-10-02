import time
import sys
import icherry.tiempo as tiempo
import random

while (1):
    fechaYHora = tiempo.FechaYHora.ahora()
    pronostico = ''

    for i in range(1, 30):
        pronostico += str(fechaYHora) + "\n"
        fechaYHora = fechaYHora.agregarHoras(1)
        pronostico += str(fechaYHora) + "\n"
        pronostico += "{}\n{}\n{}\n{}\n".format(
            random.randint(15, 25),
            random.randint(10, 50),
            random.randint(30, 50),
            random.randint(10, 20)
        )

    with open(sys.argv[1], 'w') as archivo:
        archivo.write(pronostico)

    time.sleep(300)
