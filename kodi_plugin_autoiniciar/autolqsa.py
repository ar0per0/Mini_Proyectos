import xbmc, random

#try: # el tray except está deshabilitado, no funciona en todas las versiones
xbmc.log('Execucion Servicio Episodio LQSA Random',1)
xbmc.executebuiltin('Notification([COLOR green]Iniciar[/COLOR], Episodio LQSA)')

#ejecutar video random del path indicado
xbmc.executebuiltin('RunScript(script.playrandomvideos, "D:\la que se avecina\Temporadas\")')

#random avanzar episodio o no 2=si
random.seed()
avanzar = random.randint(0, 2)
if avanzar==2:

#esperar a que el video se reproduzca
  i = 0
  titulo = ""
  while i < 5 and titulo == "":
    xbmc.sleep(3000) #milisegundos
    titulo=xbmc.getInfoLabel("Player.Title")
    i += 1

#random +10m avanzar episodio
  r = random.randint(2, 5)
  while 0 < r:
    xbmc.executebuiltin('Action(BigStepForward)') #avanza +10m
    r -= 1
    xbmc.sleep(1000)

#except Exception as ex:
#xbmc.log('ERROR Servicio Episodio LQSA Random:' +ex,4)
