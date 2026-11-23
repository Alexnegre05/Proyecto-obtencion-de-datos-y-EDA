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


def poner_formatos(df):

    # fechas
    df["primera_fecha"] = pd.to_datetime(df["primera_fecha"], format="%d/%m/%Y")
    df["fecha_lanzamiento"] = pd.to_datetime(df["fecha_lanzamiento"])
    df["fecha_obtencion"] = pd.to_datetime(df["fecha_obtencion"])

    # números enteros (Int64 admite valores vacíos)
    for columna in ["año", "posicion", "pico", "semanas", "duracion_s", "popularidad_deezer", "artista_fans"]:
        df[columna] = df[columna].astype("Int64")

    # verdadero / falso
    df["explicita"] = df["explicita"].astype("boolean")

    # texto
    df["catalogo"] = df["catalogo"].astype("string")

    # categorías (pocos valores que se repiten)
    for columna in ["label", "tipo_lanzamiento", "genero"]:
        df[columna] = df[columna].astype("category")

    return df


def imputar_datos(df):

    # guardamos qué filas no tenían datos de Deezer antes de imputar
    df["datos_imputados"] = df["duracion_s"].isna()

    # 1. datos del artista: si el mismo artista sale en otra fila, cogemos sus datos
    df["artista_fans"] = df["artista_fans"].fillna(df.groupby("artista")["artista_fans"].transform("max"))

    genero_artista = df.dropna(subset=["genero"]).groupby("artista")["genero"].agg(lambda col: col.mode()[0])
    df["genero"] = df["genero"].astype("string").fillna(df["artista"].map(genero_artista))

    # 2. fecha de lanzamiento: usamos la fecha en que la canción entró en la lista
    df["fecha_lanzamiento"] = df["fecha_lanzamiento"].fillna(df["primera_fecha"])

    # 3. números: la mediana (no le afectan los valores extremos)
    for columna in ["duracion_s", "popularidad_deezer", "artista_fans"]:
        df[columna] = df[columna].fillna(round(df[columna].median()))

    # 4. verdadero / falso: el valor más frecuente
    df["explicita"] = df["explicita"].fillna(df["explicita"].mode()[0])

    # 5. categorías que no se pueden deducir: "desconocido"
    for columna in ["tipo_lanzamiento", "genero"]:
        df[columna] = df[columna].astype("string").fillna("desconocido").astype("category")

    return df


def limpiar_dataframe_final(df):

    # borramos las columnas con información repetida y nos quedamos con la más completa
    df = df.drop(columns=COLUMNAS_REPETIDAS)

    # cada columna con su tipo y rellenamos los vacíos
    df = poner_formatos(df)
    df = imputar_datos(df)

    print("tamaño del dataframe final:", df.shape)
    print("valores vacíos que quedan:", df.isna().sum().sum())
    print(df.info())

    # guardamos el resultado
    df.to_csv(FICHERO_FUSIONADO, index=False, encoding="utf-8")
    print(f"DataFrame final guardado en {FICHERO_FUSIONADO}")

    return df


if __name__ == "__main__":
    df = limpiar_dataframe_final(fusionar_dataframes())