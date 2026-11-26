import os
import matplotlib.pyplot as plt

# Ruta dinámica a la carpeta 'imagenes' que está junto a este archivo (graficos/imagenes)
CARPETA_IMAGENES = os.path.join(os.path.dirname(__file__), "imagenes")
os.makedirs(CARPETA_IMAGENES, exist_ok=True)


def generar_histograma_duracion(df):
    datos = df["duracion_s"].dropna()

    ax = datos.plot(
        kind="hist",
        bins=20,
        color="#4C72B0",
        edgecolor="black",
        figsize=(9, 5)
    )

    ax.set_title("Distribución de la duración de las canciones", fontsize=13)
    ax.set_xlabel("Duración (segundos)")
    ax.set_ylabel("Frecuencia (número de canciones)")
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()

    # Guardar imagen
    ruta_salida = os.path.join(CARPETA_IMAGENES, "histograma_general.png")
    plt.savefig(ruta_salida, dpi=300)
    plt.close()  # Cierra la figura para que no se solape si generas varios seguidos
    print(f"Gráfico guardado en: {ruta_salida}")





def generar_histograma_duracion_por_año(df, año, columna="duracion_s", bins=20):
    # 1. Filtrar por el año seleccionado
    df_año = df[df["año"] == año]

    # 2. Comprobar que existan datos para ese año
    if df_año.empty:
        print(f"No hay datos disponibles para el año {año}.")
        return

    # 3. Limpiar nulos de la columna elegida
    datos = df_año[columna].dropna()

    # 4. Generar el histograma con pandas
    ax = datos.plot(
        kind="hist",
        bins=bins,
        color="#4C72B0",
        edgecolor="black",
        figsize=(9, 5),
    )

    # 5. Títulos y etiquetas dinámicas según el año y columna
    ax.set_title(f"Distribución de la duracion de segundos de canciones en el año {año}", fontsize=13)
    ax.set_xlabel(columna)
    ax.set_ylabel("Frecuencia (número de canciones)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()

    # Guardar imagen con nombre único según columna y año
    nombre_archivo = f"histograma_{columna}_{año}.png"
    ruta_salida = os.path.join(CARPETA_IMAGENES, nombre_archivo)
    plt.savefig(ruta_salida, dpi=300)
    plt.close()  # Libera memoria y evita que los gráficos anteriores se mezclen
    print(f"Gráfico guardado en: {ruta_salida}")



def generar_histograma_fans(df, bins=20):
    # 1. Crear una copia explícita para garantizar que el DataFrame original no se modifica
    df_copia = df.copy()

    # 2. Eliminar artistas duplicados sobre la copia
    artistas_unicos = df_copia.drop_duplicates(subset=["artista"])
    datos = artistas_unicos["artista_fans"].dropna()

    # 3. Generar el histograma
    ax = datos.plot(
        kind="hist",
        bins=bins,
        logy=True,
        color="#4C72B0",
        edgecolor="black",
        figsize=(9, 5)
    )

    # 4. Títulos y etiquetas
    ax.set_title("Distribución de fans por artista único", fontsize=13)
    ax.set_xlabel("Número de fans")
    ax.set_ylabel("Cantidad de artistas (escala log)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    # 5. Guardar imagen en graficos/imagenes/histograma_artista_fans.png
    plt.tight_layout()
    ruta_salida = os.path.join(CARPETA_IMAGENES, "histograma_artista_fans.png")
    plt.savefig(ruta_salida, dpi=300)
    plt.close()
    print(f"Gráfico guardado en: {ruta_salida}")