import time
import sys
import icherry.tiempo as tiempo

while (1):
    with open(sys.argv[1], 'w') as archivo:
        archivo.write(str(tiempo.FechaYHora.ahora()))
    time.sleep(1)
