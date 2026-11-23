import os

import pandas as pd


# Ficheros de entrada
FICHERO_WEB_SCRAPING = "data/raw/officialcharts_2005_2025.csv"
FICHERO_API = "data/processed/deezer_canciones_preparado.csv"

# Fichero de salida
CARPETA_PREPARADOS = "data/processed"
FICHERO_FUSIONADO = CARPETA_PREPARADOS + "/canciones_fusionado.csv"

# Columnas que tienen en común los dos dataframes
COLUMNAS_UNION = ["titulo", "artista"]

# Columnas que sobran en el dataframe final
COLUMNAS_REPETIDAS = [
    "deezer_titulo",          # repite titulo (y titulo no tiene vacíos)
    "deezer_artista",         # repite artista (y artista no tiene vacíos)
    "sello_deezer",           # repite label (y label no tiene vacíos)
    "anio_lanzamiento",       # sale de fecha_lanzamiento
    "coincidencia_correcta",  # solo servía para comprobar la API
]


def fusionar_dataframes(df_web_scraping=None, df_api=None):

    # si no nos pasan los dataframes, los cargamos de los csv
    if df_web_scraping is None:
        df_web_scraping = pd.read_csv(FICHERO_WEB_SCRAPING).drop(columns=["indice"])

    if df_api is None:
        df_api = pd.read_csv(FICHERO_API)

    # juntamos por titulo y artista
    # how="left" -> mantenemos todas las filas de Official Charts
    # validate="many_to_one" -> una canción puede salir varios años, pero en Deezer solo una vez
    df = df_web_scraping.merge(df_api, on=COLUMNAS_UNION, how="left", validate="many_to_one")

    print("tamaño del dataframe fusionado:", df.shape)
    print(df.head())

    # guardamos el resultado
    os.makedirs(CARPETA_PREPARADOS, exist_ok=True)
    df.to_csv(FICHERO_FUSIONADO, index=False, encoding="utf-8")
    print(f"DataFrame fusionado guardado en {FICHERO_FUSIONADO}")

    return df


def limpiar_dataframe_final(df):

    # borramos las columnas con información repetida y nos quedamos con la más completa
    df = df.drop(columns=COLUMNAS_REPETIDAS)

    print("tamaño del dataframe final:", df.shape)
    print(df.head())

    # guardamos el resultado
    df.to_csv(FICHERO_FUSIONADO, index=False, encoding="utf-8")
    print(f"DataFrame final guardado en {FICHERO_FUSIONADO}")

    return df

df = limpiar_dataframe_final(fusionar_dataframes())