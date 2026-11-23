import os
import re
import unicodedata

import pandas as pd


# Fichero original que generó api_deezer.py (no se modifica)
FICHERO_ORIGINAL = "data/raw/deezer_canciones.csv"

# Fichero con los datos preparados
CARPETA_PREPARADOS = "data/processed"
FICHERO_PREPARADO = CARPETA_PREPARADOS + "/deezer_canciones_preparado.csv"

# Palabras que indican que Deezer ha devuelto una versión karaoke, cover o tributo y no la original
PALABRAS_FALSAS = ["karaoke", "originally performed", "made famous", "tribute", "in the style of",
                   "instrumental", "piano vocal", "emulation", "ringtone"]

# Artistas que Deezer escribe de otra forma (nombre en Official Charts -> nombre en Deezer)
NOMBRES_DEEZER = {"PINK": "P!nk", "ASAP ROCKY": "A$AP Rocky"}

# Columnas que vienen de Deezer (se vacían si la coincidencia es incorrecta)
COLUMNAS_DEEZER = ["deezer_titulo", "deezer_artista", "duracion_s", "explicita", "popularidad_deezer",
                   "sello_deezer", "fecha_lanzamiento", "tipo_lanzamiento", "genero", "artista_fans"]


def limpiar_texto(texto):
  # "P!nk" -> "pnk", "Señorita" -> "senorita": minúsculas, sin acentos ni signos
  texto = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
  return re.sub(r"[^a-z0-9]", "", texto.lower())


def artista_principal(artista):
  # "TONY CHRISTIE FT PETER KAY" -> "TONY CHRISTIE"
  for separador in [" FT ", " X ", " VS ", " & ", "/", ","]:
    artista = artista.split(separador)[0]
  return artista.strip()


def es_correcta(fila):
  # decide si la canción que devolvió Deezer es la misma que la de Official Charts

  if fila["encontrada"] == False:
    return False

  titulo_deezer = str(fila["deezer_titulo"]).lower()

  # 1. Si es una versión karaoke, cover o tributo, es incorrecta
  for palabra in PALABRAS_FALSAS:
    if palabra in titulo_deezer:
      return False

  # 2. Si el artista coincide, es correcta
  artista_oc = artista_principal(fila["artista"])
  artista_oc = limpiar_texto(NOMBRES_DEEZER.get(artista_oc, artista_oc))
  artista_dz = limpiar_texto(fila["deezer_artista"])

  if artista_oc in artista_dz or artista_dz in artista_oc:
    return True

  # 3. Si el artista no coincide pero el título es exactamente el mismo, la damos por buena
  #    (son casos como PINK -> P!nk o ASAP ROCKY -> A$AP Rocky, que se escriben distinto)
  if limpiar_texto(fila["titulo"]) == limpiar_texto(fila["deezer_titulo"]):
    return True

  return False



def df_limpio():
      
    # ---------------------------------------------------------------------------
    # 1. Cargar los datos originales en un DataFrame
    # ---------------------------------------------------------------------------

    df = pd.read_csv(FICHERO_ORIGINAL)


    # ---------------------------------------------------------------------------
    # 2. Revisar las coincidencias y vaciar las incorrectas
    # ---------------------------------------------------------------------------

    df["coincidencia_correcta"] = df.apply(es_correcta, axis=1)

    # en las incorrectas, los datos de Deezer no son de nuestra canción: los dejamos vacíos
    df.loc[df["coincidencia_correcta"] == False, COLUMNAS_DEEZER] = None


    # ---------------------------------------------------------------------------
    # 3. Poner a cada columna su tipo correcto
    # ---------------------------------------------------------------------------

    # fechas
    df["fecha_lanzamiento"] = pd.to_datetime(df["fecha_lanzamiento"], errors="coerce")
    df["fecha_obtencion"] = pd.to_datetime(df["fecha_obtencion"], errors="coerce")

    # fechas erróneas: Deezer pone 0000-00-00 o fechas futuras cuando no la sabe
    df.loc[df["fecha_lanzamiento"] > df["fecha_obtencion"], "fecha_lanzamiento"] = None
    df["anio_lanzamiento"] = df["fecha_lanzamiento"].dt.year.astype("Int64")

    # números enteros (Int64 admite valores vacíos)
    for columna in ["duracion_s", "popularidad_deezer", "artista_fans"]:
      df[columna] = df[columna].astype("Int64")

    # verdadero / falso
    df["explicita"] = df["explicita"].astype("boolean")

    # categorías (pocos valores que se repiten)
    for columna in ["tipo_lanzamiento", "genero", "sello_deezer"]:
      df[columna] = df[columna].astype("category")

    # la columna "encontrada" ya no hace falta: "coincidencia_correcta" la sustituye
    df = df.drop(columns=["encontrada"])


    # ---------------------------------------------------------------------------
    # 4. Guardar el DataFrame preparado
    # ---------------------------------------------------------------------------

    os.makedirs(CARPETA_PREPARADOS, exist_ok=True)
    df.to_csv(FICHERO_PREPARADO, index=False, encoding="utf-8")
    print(f"DataFrame creado y guardado en {FICHERO_PREPARADO}")

    return df