import json

from bs4 import BeautifulSoup
from curl_cffi import requests  



def resolver(valor, nuxt_data): # lo que hace esto es sacar el valor de lalista a partir de la clave que es un numero
# hay que comprovar que es un entero el numero que buscamos el [valor]

  if (isinstance(valor, int) == True and 0 <= valor < len(nuxt_data)):

    return nuxt_data[valor] # devolvemos la clave
  
  else:

    return valor # si no funciona devolvemos el valor original

def escribir_fichero(fichero, canciones_lista, i):

  # Acumulamos todo el texto del año en una sola variable
  bloque = f"{i} canciones:\n"

  for k in range(len(canciones_lista)):

    canciones = canciones_lista[k]

    bloque = bloque +  (
        f"{k} | posicion: {canciones['posicion']} | titulo: {canciones['titulo']} | artista:"
        f" {canciones['artista']} | pico: {canciones['pico']} | semanas: {canciones['semanas']} |"
        f" label: {canciones['label']} | catalogo: {canciones['catalogo']} | primera_fecha:"
        f" {canciones['primera_fecha']}\n"
    )

  # Un solo .write() para todo el bloque
  fichero.write(bloque)

  fichero.flush()  # Fuerza a guardar en el disco duro inmediatamente

  return fichero



def web_scraping():

  fichero_canciones = open("officialcharts_2005_2025.csv", "a", encoding="utf-8") # fichero, tiene que ser append para que no sobreescriba
    
  for i in range(2005, 2026):

    print(i)

    # url de donde sacamos los datos
    url = f"https://www.officialcharts.com/charts/end-of-year-singles-chart/{i}0101/37501/"

    # Petición principal con requests, hacemos timeout=15 para no saturar la pagina

    # impersonate es para decir que somo chrome y poder conectarnos y que los blocks no se cierran

    respuesta = requests.get(url, impersonate="chrome", timeout=15) 

    respuesta.raise_for_status() # buscamos si hay algun error 40x,... solo si es codigo 20x no petara

    html_limpio = BeautifulSoup(respuesta.text, "html.parser") # este codigo, lo que hace beautiful soup es separar el html por etiquetas 

    script_nuxt = html_limpio.find("script", id="__NUXT_DATA__") # esto busca solo la etiqueta script que tenga id nuxt data

    nuxt_data = json.loads(script_nuxt.string) # pasa a json todo lo que hay dentro de el script




    canciones_lista = [] # aqui guardamos una lisat con todas las canciones que hay

    for item in nuxt_data:

      if isinstance(item, dict) == True and resolver(item.get("element"), nuxt_data) == "track-info": # la informacion que buscamos esta en un diccionario, todo lo que no sea 
        # diccionario no lo queremos (listas, tuplas...) y queremos sacar solo lo que el diccionario coincida que es un track-info, descartamos todo lo demas
        # element es si la clave existe la devuelve, en este caso un numero, ese numero representa una cancion en concreto


        # item.get devuelve la clave de el diccionario 
        posicion = resolver(item.get("position"), nuxt_data) # sacamos los datos a partir de su posicion 

        titulo = resolver(item.get("title"), nuxt_data)

        artista = resolver(item.get("artist"), nuxt_data)

        semanas = resolver(item.get("weeks"), nuxt_data)

        pico = resolver(item.get("peak"), nuxt_data)

        info_url = resolver(item.get("infoUrl"), nuxt_data) # hay mas informacion que viene dentro de cada cancion pero esta en otra url, representa el boton info

        label = None

        catalogo = None

        primera_fecha = None # esta es la informacion que podemos sacar a partir de esos datos
        
        comprovar = 0 # variable que es 0 si el try except no falla, 1 en caso contraio

        if info_url != None: # si no es vacio

          try: # try except por si peta el sacar los datos

            #  Aquí también usamos impersonate="chrome" 
            res_info = requests.get(info_url, impersonate="chrome", timeout=20) # esta url es de donde sacar los datos personalizados

            if (res_info.status_code == 200): # si el codigo es correcto

              datos_extra = res_info.json() # sacamos los datos con json

              label = datos_extra.get("label") # sacamos las etiquetas que queremos

              catalogo = datos_extra.get("catNo") or datos_extra.get(
                  "catalogueNumber"
              ) # catNo es abreviacion de catalogo number

              primera_fecha = (
                      datos_extra.get("firstChartDate")
                      or datos_extra.get("firstCharted")
                      or datos_extra.get("first_chart_date")
                      or datos_extra.get("chartDate")
                      or datos_extra.get("entryDate")
                  )

          except Exception as e:

            comprovar = 1

            print(f"Error en canción {posicion}: {e}")

          
        if (comprovar == 0): # si no ha petado añadimos los datos en la lista

          canciones_lista.append({"posicion": posicion,"titulo": titulo,"artista": artista,"pico": pico,"semanas": semanas,"label": label,"catalogo": catalogo,"primera_fecha": primera_fecha,})

        # añadimos la cancion en la lista de las canciones con su información
    

    fichero_canciones = escribir_fichero(fichero_canciones,canciones_lista, i)
      

  fichero_canciones.close() # cerramos el fichero

    