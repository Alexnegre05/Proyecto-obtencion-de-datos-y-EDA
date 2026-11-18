import json

from bs4 import BeautifulSoup
from curl_cffi import requests  # <-- Asegúrate de que NO quede 'import requests' suelto
import pandas as pd

url = "https://www.officialcharts.com/charts/end-of-year-singles-chart/20250101/37501/"

# 1. Petición principal con requests, hacemos timeout=15 para no saturar la pagina

respuesta = requests.get(url, impersonate="chrome", timeout=15) 

respuesta.raise_for_status() # buscamos si hay algun error 40x,... solo si es codigo 20x no petara

html_limpio = BeautifulSoup(respuesta.text, "html.parser") # este codigo, lo que hace beautiful soup es separar el html por etiquetas 

script_nuxt = html_limpio.find("script", id="__NUXT_DATA__") # esto busca solo la etiqueta script que tenga id nuxt data

nuxt_data = json.loads(script_nuxt.string) # pasa a json todo lo que hay dentro de el script


def resolver(valor): # lo que hace esto es sacar el valor de el diccionario a partir de la clave
# hay que comprovar que es un entero el numero que buscamos y que el id esta entre 0 y el total de ese script

  if (isinstance(valor, int) == True and 0 <= valor < len(nuxt_data)):

    return nuxt_data[valor]
  
  else:

    return valor # si no funciona devolvemos el valor original


canciones_lista = [] # aqui guardamos una lisat con todas las canciones que hay

for item in nuxt_data:

  if isinstance(item, dict) == True and resolver(item.get("element")) == "track-info": # la informacion que buscamos esta en un diccionario, todo lo que no sea 
    # diccionario no lo queremos (listas, tuplas...) y queremos sacar solo lo que el diccionario coincida que es un track-info, descartamos todo lo demas
    # element es si la clave existe la devuelve, en este caso un numero, ese numero representa una cancion en concreto

    posicion = resolver(item.get("position"))

    titulo = resolver(item.get("title"))

    artista = resolver(item.get("artist"))

    semanas = resolver(item.get("weeks"))

    pico = resolver(item.get("peak"))

    info_url = resolver(item.get("infoUrl")) # sacamos los datos a partir de su posicion 

    label = None

    catalogo = None

    primera_fecha = None

    if info_url != None: # si no es vacio

      try:
        #  Aquí también usamos impersonate="chrome" 
        res_info = requests.get(info_url, impersonate="chrome", timeout=10) # esta url es de donde sacar los datos personalizados

        if (res_info.status_code == 200): # si el codigo es correcto

          datos_extra = res_info.json()

          label = datos_extra.get("label")

          catalogo = datos_extra.get("catNo") or datos_extra.get(
              "catalogueNumber"
          ) # catNo es abreviacion de catalogo number

          primera_fecha = datos_extra.get("firstChartDate")

      except Exception as e:

        print(f"Error en canción {posicion}: {e}")

      

    canciones_lista.append({"posicion": posicion,"titulo": titulo,"artista": artista,"pico": pico,"semanas": semanas,"label": label,"catalogo": catalogo,"primera_fecha": primera_fecha,})

    # añadimos la cancion en la lista de las canciones con su información


df = pd.DataFrame(canciones_lista).sort_values("posicion").reset_index(drop=True) # sort_value ordena de menor a mayor por su posicion
# numera la posicion de el dataframe para que empieze en 0

print(df.head(10))

