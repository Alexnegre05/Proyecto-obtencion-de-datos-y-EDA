import os

import numpy as np
import pandas as pd


# Fichero con el dataframe final
FICHERO_FUSIONADO = "data/processed/canciones_fusionado.csv"

# Fichero de salida
CARPETA_PREPARADOS = "data/processed"
FICHERO_ESTANDARIZADO = CARPETA_PREPARADOS + "/canciones_estandarizado.csv"

# Columnas numéricas que se estandarizan
# (año, posicion y pico no: son un orden o una fecha, no una medida)
COLUMNAS_A_ESTANDARIZAR = ["duracion_s", "popularidad_deezer", "semanas", "artista_fans_log"]

# A partir de cuántas desviaciones típicas consideramos que un valor es atípico
LIMITE_ATIPICO = 3


def estandarizar_datos(df=None):

    # si no nos pasan el dataframe, lo cargamos del csv
    if df is None:
        df = pd.read_csv(FICHERO_FUSIONADO)

    # copia para no modificar el dataframe original
    df = df.copy()

    # artista_fans va de cientos a más de 20 millones: con el logaritmo
    # los valores quedan en una escala parecida (2 = 100 fans, 7 = 10 millones)
    df["artista_fans_log"] = np.log10(df["artista_fans"])

    # estandarización (z-score): z = (valor - media) / desviación típica
    # después cada columna tiene media 0 y desviación típica 1, así se pueden comparar
    # columnas con unidades distintas (segundos, puntos, semanas, fans)
    for columna in COLUMNAS_A_ESTANDARIZAR:
        media = df[columna].mean()
        desviacion = df[columna].std()
        df[columna + "_z"] = (df[columna] - media) / desviacion

    # comprobación: la media tiene que salir 0 y la desviación 1
    columnas_z = [columna + "_z" for columna in COLUMNAS_A_ESTANDARIZAR]
    print("media y desviación típica de las columnas estandarizadas:")
    print(df[columnas_z].agg(["mean", "std"]).round(2))

    # valores atípicos: los que están a más de 3 desviaciones típicas de la media
    print(f"\nvalores atípicos (|z| > {LIMITE_ATIPICO}) por columna:")
    print((df[columnas_z].abs() > LIMITE_ATIPICO).sum())

    # guardamos el resultado (las columnas originales se conservan)
    os.makedirs(CARPETA_PREPARADOS, exist_ok=True)
    df.to_csv(FICHERO_ESTANDARIZADO, index=False, encoding="utf-8")
    print(f"\nDataFrame estandarizado guardado en {FICHERO_ESTANDARIZADO}")

    return df


if __name__ == "__main__":
    df = estandarizar_datos()
