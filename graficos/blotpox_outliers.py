import os
import pandas as pd
import matplotlib.pyplot as plt

# Ruta dinámica a la carpeta 'imagenes' dentro de 'graficos'
CARPETA_IMAGENES = os.path.join(os.path.dirname(__file__), "imagenes")
os.makedirs(CARPETA_IMAGENES, exist_ok=True)


def generar_boxplot(df, columna):
    # 1. Crear una copia para no modificar el DataFrame original
    df_copia = df.copy()

    # Obtener la lista de columnas numéricas válidas para ayudar al usuario si falla
    columnas_numericas = df_copia.select_dtypes(include="number").columns.tolist()

    # 2. Comprobar que la columna existe
    if columna not in df_copia.columns:
        print(f"Aviso: La columna '{columna}' no existe en el dataset.")
        print(f"Columnas numéricas disponibles: {columnas_numericas}")
        return

    # 3. Comprobar que la columna es numérica (y no booleana) para que no pete
    if not pd.api.types.is_numeric_dtype(df_copia[columna]) or pd.api.types.is_bool_dtype(df_copia[columna]):
        print(f"Aviso: La columna '{columna}' es de tipo '{df_copia[columna].dtype}' (no numérica), no se puede hacer un boxplot.")
        print(f"Prueba con una de estas columnas numéricas: {columnas_numericas}")
        return

    # 4. Si es 'artista_fans', eliminar artistas duplicados
    if columna == "artista_fans":
        df_copia = df_copia.drop_duplicates(subset=["artista"])

    # 5. Limpiar valores nulos
    datos = df_copia[columna].dropna()

    if datos.empty:
        print(f"Aviso: La columna '{columna}' no tiene datos válidos para graficar.")
        return

    # 6. Generar el boxplot individual con pandas
    ax = datos.plot(
        kind="box",
        vert=False,
        color={"boxes": "#4C72B0", "whiskers": "#4C72B0", "medians": "#DD8452", "caps": "#4C72B0"},
        patch_artist=True,
        figsize=(9, 4)
    )

    # 7. Títulos y etiquetas dinámicas
    ax.set_title(f"Boxplot de '{columna}'", fontsize=13)
    ax.set_xlabel(columna)
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    # 8. Guardar imagen
    plt.tight_layout()
    ruta_salida = os.path.join(CARPETA_IMAGENES, f"boxplot_{columna}.png")
    plt.savefig(ruta_salida, dpi=300)
    plt.close()
    print(f"Boxplot guardado correctamente en: {ruta_salida}")
