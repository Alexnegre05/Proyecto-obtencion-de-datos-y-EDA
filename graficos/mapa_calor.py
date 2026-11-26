import os

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd


# Fichero con el dataframe final
FICHERO_FUSIONADO = "data/processed/canciones_fusionado.csv"

# Carpeta donde se guardan las imágenes
CARPETA_IMAGENES = "graficos/imagenes"

# Columnas numéricas y el nombre que se ve en el gráfico
COLUMNAS = {
    "año": "año",
    "posicion": "posición",
    "pico": "pico",
    "semanas": "semanas",
    "duracion_s": "duración",
    "popularidad_deezer": "popularidad",
    "artista_fans": "fans artista",
}

# Colores: rojo = relación negativa, gris = sin relación, azul = relación positiva
COLORES = LinearSegmentedColormap.from_list(
    "rojo_gris_azul", ["#a61b1c", "#ec4647", "#efefef", "#257de0", "#0e3d7e"]
)
COLOR_TEXTO = "#191919"
COLOR_TEXTO_SUAVE = "#666666"


def mapa_calor(df=None):

    # si no nos pasan el dataframe, lo cargamos del csv
    if df is None:
        df = pd.read_csv(FICHERO_FUSIONADO)

    # quitamos las filas con datos imputados para que no cambien las correlaciones
    df = df[df["datos_imputados"] == False]

    # correlación de Spearman entre todas las columnas numéricas
    # (se calcula con la posición (rank) de cada valor, así no hace falta instalar scipy)
    correlaciones = df[list(COLUMNAS)].rank().corr()
    correlaciones = correlaciones.rename(index=COLUMNAS, columns=COLUMNAS)

    # la matriz es simétrica: solo enseñamos la mitad de abajo para no repetir datos
    mitad_arriba = np.triu(np.ones(correlaciones.shape, dtype=bool))
    valores = correlaciones.mask(mitad_arriba)

    # la primera fila y la última columna quedan vacías: las quitamos
    valores = valores.iloc[1:, :-1]

    figura, ejes = plt.subplots(figsize=(8, 6.5))

    imagen = ejes.imshow(valores, cmap=COLORES, vmin=-1, vmax=1)

    # número dentro de cada casilla
    for fila in range(len(valores.index)):
        for columna in range(len(valores.columns)):
            valor = valores.iloc[fila, columna]
            if not np.isnan(valor):
                color = "white" if abs(valor) > 0.5 else COLOR_TEXTO
                ejes.text(columna, fila, f"{valor:.2f}".replace(".", ","),
                          ha="center", va="center", color=color, fontsize=10)

    # nombres de las columnas en los ejes
    ejes.set_xticks(range(len(valores.columns)), valores.columns, rotation=45, ha="right")
    ejes.set_yticks(range(len(valores.index)), valores.index)
    ejes.tick_params(colors=COLOR_TEXTO_SUAVE, length=0)
    for borde in ejes.spines.values():
        borde.set_visible(False)

    # barra de colores con la escala
    barra = figura.colorbar(imagen, ax=ejes, shrink=0.8)
    barra.set_label("correlación de Spearman", color=COLOR_TEXTO_SUAVE)
    barra.outline.set_visible(False)
    barra.ax.tick_params(colors=COLOR_TEXTO_SUAVE, length=0)

    ejes.set_title("Correlación entre las variables numéricas", loc="left", color=COLOR_TEXTO, fontsize=13)

    plt.tight_layout()

    # guardamos la imagen y la mostramos
    os.makedirs(CARPETA_IMAGENES, exist_ok=True)
    plt.savefig(f"{CARPETA_IMAGENES}/mapa_calor_correlaciones.png", dpi=150)
    plt.show()

    return correlaciones


if __name__ == "__main__":
    print(mapa_calor().round(2))
