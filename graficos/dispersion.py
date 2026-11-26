import os

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd


# Fichero con el dataframe final
FICHERO_FUSIONADO = "data/processed/canciones_fusionado.csv"

# Carpeta donde se guardan las imágenes
CARPETA_IMAGENES = "graficos/imagenes"

# Colores
COLOR_PUNTOS = "#257de0"
COLOR_LINEA = "#191919"
COLOR_TEXTO = "#191919"
COLOR_TEXTO_SUAVE = "#666666"
COLOR_REJILLA = "#e5e5e5"


def diagrama_dispersion(df, x, y, titulo, texto_x, texto_y, escala_log=False, mediana_por_x=False):

    figura, ejes = plt.subplots(figsize=(9, 5.5))

    # si x tiene pocos valores (como los años), movemos un poco los puntos a los lados
    # para que no queden todos uno encima de otro
    valores_x = df[x]
    if mediana_por_x:
        valores_x = valores_x + np.random.uniform(-0.3, 0.3, len(df))

    ejes.scatter(valores_x, df[y], s=12, alpha=0.35, color=COLOR_PUNTOS, linewidths=0, label="canciones")

    # línea con la mediana de cada valor de x (ayuda a ver la tendencia)
    if mediana_por_x:
        mediana = df.groupby(x)[y].median()
        ejes.plot(mediana.index, mediana.values, color=COLOR_LINEA, linewidth=2, label=f"mediana por {x}")
        # leyenda arriba a la derecha, fuera del gráfico para no tapar puntos
        ejes.legend(loc="lower right", bbox_to_anchor=(1, 1), ncol=2, frameon=False,
                    labelcolor=COLOR_TEXTO_SUAVE, fontsize=9)

    if escala_log:
        ejes.set_xscale("log")

    # correlación de Spearman: de -1 a 1 (0 = no hay relación)
    # se calcula con la posición (rank) de cada valor, así no hace falta instalar scipy
    correlacion = df[x].rank().corr(df[y].rank())

    ejes.set_title(titulo, loc="left", color=COLOR_TEXTO, fontsize=13, pad=22)
    ejes.text(0, 1.02, f"correlación de Spearman: {correlacion:.2f}".replace(".", ","),
              transform=ejes.transAxes, color=COLOR_TEXTO_SUAVE, fontsize=9)
    ejes.set_xlabel(texto_x, color=COLOR_TEXTO_SUAVE)
    ejes.set_ylabel(texto_y, color=COLOR_TEXTO_SUAVE)

    # números del eje y con punto de miles (800.000 en vez de 0.8 1e6)
    ejes.yaxis.set_major_formatter(FuncFormatter(lambda valor, posicion: f"{valor:,.0f}".replace(",", ".")))

    # rejilla suave y sin bordes que no hacen falta
    ejes.grid(color=COLOR_REJILLA, linewidth=0.8)
    ejes.set_axisbelow(True)
    for borde in ["top", "right"]:
        ejes.spines[borde].set_visible(False)
    ejes.tick_params(colors=COLOR_TEXTO_SUAVE, length=0)

    plt.tight_layout()

    # guardamos la imagen y la mostramos
    os.makedirs(CARPETA_IMAGENES, exist_ok=True)
    plt.savefig(f"{CARPETA_IMAGENES}/dispersion_{x}_{y}.png", dpi=150)
    plt.show()


def diagramas_dispersion(df=None):

    # si no nos pasan el dataframe, lo cargamos del csv
    if df is None:
        df = pd.read_csv(FICHERO_FUSIONADO)

    # todas las gráficas usan datos de Deezer: quitamos las filas con datos imputados
    df = df[df["datos_imputados"] == False]

    diagrama_dispersion(df, "artista_fans", "popularidad_deezer",
                        "¿Los artistas con más fans tienen canciones más populares?",
                        "fans del artista en Deezer (escala logarítmica)", "popularidad actual en Deezer",
                        escala_log=True)

    diagrama_dispersion(df, "año", "duracion_s",
                        "¿Las canciones de éxito son cada vez más cortas?",
                        "año de la lista", "duración (segundos)",
                        mediana_por_x=True)

    diagrama_dispersion(df, "año", "popularidad_deezer",
                        "¿Se escuchan más hoy los éxitos recientes?",
                        "año de la lista", "popularidad actual en Deezer",
                        mediana_por_x=True)


if __name__ == "__main__":
    diagramas_dispersion()
