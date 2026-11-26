import numpy as np
import pandas as pd


def calcular_estadisticas_numericas(df):
    # 1. Seleccionar solo columnas numéricas (excluyendo booleanas)
    df_num = df.select_dtypes(include="number")

    resultados = []

    for col in df_num.columns:

        serie = df_num[col].dropna().astype(float) # lo pasa a float incluido los datos que son decimales

        mitjana = serie.mean()

        mediana = serie.median()

        # Puede haber varias modas; cogemos la primera o las unimos si hay empate
        modas = serie.mode()

        moda = ", ".join(modas.astype(str)) if len(modas) <= 3 else f"{modas.iloc[0]} (y más)"

        varianza = serie.var(ddof=0)            # Varianza muestral (n)
        desv_estandar = serie.std(ddof=1)       # Desviación estándar (raíz de varianza)

        # Desviación media respecto a la media en valor absoluto
        desv_abs = np.mean(np.abs(serie - mitjana))

        # Desviación cuadrática media
        desv_cuadratica = np.sqrt(np.mean((serie - mitjana) ** 2))

        resultados.append({
            "Variable": col,
            "Mitjana": round(mitjana, 2),
            "Mediana": round(mediana, 2),
            "Moda": moda,
            "Varianza": round(varianza, 2),
            "Desv. Estándar": round(desv_estandar, 2),
            "Desv. valor absoluto": round(desv_abs, 2),
        })

    tabla_estadisticas = pd.DataFrame(resultados)
    return tabla_estadisticas
