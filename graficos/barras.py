import os

import matplotlib.pyplot as plt
import pandas as pd


# Fichero con el dataframe final
FICHERO_FUSIONADO = "data/processed/canciones_fusionado.csv"

# Carpeta donde se guardan las imágenes
CARPETA_IMAGENES = "graficos/imagenes"

# Colores
COLOR_BARRAS = "#257de0"
COLOR_TEXTO = "#191919"
COLOR_TEXTO_SUAVE = "#666666"


def dibujar_barras(valores, nombre_imagen, titulo, texto_eje):

    # el valor más grande arriba
    valores = valores.sort_values()

    figura, ejes = plt.subplots(figsize=(9, max(3, len(valores) * 0.4)))

    barras = ejes.barh(valores.index.astype(str), valores.values, color=COLOR_BARRAS, height=0.7)

    # número al final de cada barra (con punto de miles: 745.278)
    etiquetas = [f"{valor:,.0f}".replace(",", ".") for valor in valores.values]
    ejes.bar_label(barras, labels=etiquetas, padding=3, color=COLOR_TEXTO_SUAVE, fontsize=9)

    ejes.set_title(titulo, loc="left", color=COLOR_TEXTO, fontsize=13)
    ejes.set_xlabel(texto_eje, color=COLOR_TEXTO_SUAVE)

    # quitamos los bordes que no hacen falta
    for borde in ["top", "right", "bottom"]:
        ejes.spines[borde].set_visible(False)
    ejes.tick_params(colors=COLOR_TEXTO_SUAVE, length=0)
    ejes.set_xticks([])

    plt.tight_layout()

    # guardamos la imagen y la mostramos
    os.makedirs(CARPETA_IMAGENES, exist_ok=True)
    plt.savefig(f"{CARPETA_IMAGENES}/barras_{nombre_imagen}.png", dpi=150)
    plt.show()


def diagrama_barras(df, columna, titulo, maximo=None):

    # contamos cuántas canciones hay de cada valor
    conteo = df[columna].value_counts()

    # si hay muchos valores, nos quedamos con los más frecuentes
    if maximo is not None:
        conteo = conteo.head(maximo)

    dibujar_barras(conteo, columna, titulo, "número de canciones")


def popularidad_por_genero(df, minimo_canciones=10):

    # quitamos los géneros desconocidos
    df = df[df["genero"] != "desconocido"]

    # solo los géneros con suficientes canciones (la media de 1 o 2 canciones no es fiable)
    conteo = df["genero"].value_counts()
    generos = conteo[conteo >= minimo_canciones].index
    df = df[df["genero"].isin(generos)]

    # media de popularidad de cada género
    media = df.groupby("genero")["popularidad_deezer"].mean()

    dibujar_barras(media, "popularidad_genero", "Popularidad media en Deezer por género",
                   f"popularidad media (géneros con {minimo_canciones} canciones o más)")


def diagramas_barras(df=None):

    # si no nos pasan el dataframe, lo cargamos del csv
    if df is None:
        df = pd.read_csv(FICHERO_FUSIONADO)

    # genero, explicita y tipo_lanzamiento vienen de Deezer: quitamos las filas con datos imputados
    # para que los valores inventados no cambien el resultado
    df_deezer = df[df["datos_imputados"] == False]

    diagrama_barras(df_deezer, "genero", "Canciones por género")

    explicita = df_deezer["explicita"].map({True: "Sí", False: "No"})
    diagrama_barras(explicita.to_frame(), "explicita", "¿La canción es explícita?")

    diagrama_barras(df_deezer, "tipo_lanzamiento", "Canciones por tipo de lanzamiento")

    popularidad_por_genero(df_deezer)

    # label y artista vienen de Official Charts: usamos todas las filas
    diagrama_barras(df, "label", "Las 15 discográficas con más canciones", maximo=15)

    diagrama_barras(df, "artista", "Los 15 artistas con más canciones en las listas", maximo=15)


if __name__ == "__main__":
    diagramas_barras()
