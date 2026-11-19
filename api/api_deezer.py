import json
import time

import pandas as pd
import requests


# Fichero que genera el web scraping (está en la carpeta principal del repositorio)
FICHERO_SCRAPING = "officialcharts_2005_2025.csv"

# Ficheros que genera este script
FICHERO_JSON = "deezer_respuestas_originales.json"  # respuestas de la API tal cual llegan
FICHERO_CSV = "deezer_canciones.csv"                # tabla con los datos que nos interesan

URL_API = "https://api.deezer.com"  # API pública de Deezer: gratis y sin clave


def leer_scraping(nombre_fichero):
  # lee el fichero del scraping y devuelve una lista de canciones (diccionarios)
  # formato de cada línea:  0 | posicion: 1 | titulo: AXEL F | artista: CRAZY FROG | ...
  # y antes de cada año hay una línea:  2005 canciones:

  canciones = []
  anio = None

  fichero = open(nombre_fichero, "r", encoding="utf-8")

  for linea in fichero:

    linea = linea.strip()

    if linea.endswith("canciones:"):  # línea del año
      anio = int(linea.split(" ")[0])

    elif "|" in linea:  # línea de una canción
      partes = linea.split(" | ")
      cancion = {"anio": anio}

      for parte in partes[1:]:  # la primera parte es el número de fila, no la queremos
        clave, valor = parte.split(": ", 1)
        cancion[clave] = valor

      canciones.append(cancion)

  fichero.close()

  return canciones


def llamar_api(ruta, parametros=None):
  # hace una petición a la API y devuelve el JSON, o None si hay error

  time.sleep(0.2)  # esperamos para no superar el límite de 50 peticiones cada 5 segundos

  try:
    respuesta = requests.get(URL_API + ruta, params=parametros, timeout=15)
    datos = respuesta.json()

  except Exception as e:
    print(f"Error en {ruta}: {e}")
    return None

  if "error" in datos:  # Deezer avisa de los errores dentro del JSON
    print(f"Error de la API en {ruta}: {datos['error']}")
    return None

  return datos


def artista_principal(artista):
  # "TONY CHRISTIE FT PETER KAY" -> "TONY CHRISTIE"  (buscamos solo por el primer artista)
  for separador in [" FT ", " X ", " & ", "/", ","]:
    artista = artista.split(separador)[0]
  return artista.strip()


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

canciones = leer_scraping(FICHERO_SCRAPING)
print(f"Canciones leídas del scraping: {len(canciones)}")

# una canción puede salir en varios años: la buscamos una sola vez
canciones_unicas = []
for cancion in canciones:
  pareja = (cancion["titulo"], cancion["artista"])
  if pareja not in canciones_unicas:
    canciones_unicas.append(pareja)

print(f"Canciones distintas a buscar en Deezer: {len(canciones_unicas)}")

respuestas_originales = []  # aquí guardamos todo lo que devuelve la API
filas = []                  # aquí guardamos los datos que nos interesan

for n, (titulo, artista) in enumerate(canciones_unicas):

  print(n + 1, "/", len(canciones_unicas), "-", titulo, "-", artista)

  fila = {"titulo": titulo, "artista": artista, "encontrada": False}

  # 1. Buscamos la canción escribiendo el artista principal y el título, como en el buscador de Deezer
  busqueda = llamar_api("/search", {"q": f"{artista_principal(artista)} {titulo}", "limit": 5})
  respuestas_originales.append({"titulo": titulo, "artista": artista, "busqueda": busqueda})

  # 2. De los 5 primeros resultados, nos quedamos con el primero cuyo título coincide con el nuestro
  #    (así evitamos quedarnos con una canción que no tiene nada que ver)
  resultado = None

  if busqueda != None:
    for opcion in busqueda["data"]:
      titulo_deezer = opcion["title"].lower().replace("’", "'")
      if titulo.lower() in titulo_deezer or titulo_deezer in titulo.lower():
        resultado = opcion
        break

  if resultado != None:

    # 3. Pedimos los datos del álbum (sello, género, fecha) y del artista (seguidores)
    album = llamar_api(f"/album/{resultado['album']['id']}")
    datos_artista = llamar_api(f"/artist/{resultado['artist']['id']}")
    respuestas_originales[-1]["album"] = album
    respuestas_originales[-1]["artista_deezer"] = datos_artista

    fila["encontrada"] = True
    fila["deezer_titulo"] = resultado["title"]
    fila["deezer_artista"] = resultado["artist"]["name"]
    fila["duracion_s"] = resultado["duration"]
    fila["explicita"] = resultado["explicit_lyrics"]
    fila["popularidad_deezer"] = resultado["rank"]

    if album != None:
      generos = album.get("genres", {}).get("data", [])
      fila["sello_deezer"] = album.get("label")
      fila["fecha_lanzamiento"] = album.get("release_date")
      fila["tipo_lanzamiento"] = album.get("record_type")  # single, album, ep...
      fila["genero"] = generos[0]["name"] if len(generos) > 0 else None

    if datos_artista != None:
      fila["artista_fans"] = datos_artista.get("nb_fan")

  filas.append(fila)


# 4. Guardamos las respuestas originales y la tabla
with open(FICHERO_JSON, "w", encoding="utf-8") as f:
  json.dump(respuestas_originales, f, ensure_ascii=False, indent=1)

df = pd.DataFrame(filas)
df["fecha_obtencion"] = time.strftime("%Y-%m-%d")
df.to_csv(FICHERO_CSV, index=False, encoding="utf-8")

print(f"Encontradas en Deezer: {df['encontrada'].sum()} de {len(df)}")
print(f"Guardado {FICHERO_JSON} y {FICHERO_CSV}")

