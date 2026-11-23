import pandas as pd

ruta = r"D:\Alex Negre IA+BD\Proyecto-obtencion-de-datos-y-EDA\data\raw"

df = pd.read_csv(f"{ruta}\\officialcharts_2005_2025.csv") # ya tenemos el dataframe


df_copy = df.copy() # hacemos una copia de el dataframe de seguretat

# mostramos el tamaño de la matriz asi como cuantos datos 
print("tamaño total de la matriz m*n es", df.shape) 


print("En total tenemos", df.shape[0]*df.shape[1], "datos") 

print(df.head())

print(df.info())




# Contar cadenas vacías ("") o que solo tienen espacios ("   ") por columna
vacios_por_columna = df.select_dtypes(include=['object', 'string']).apply(
    lambda col: (col.str.strip() == '').sum()
)

# esto lo que hace es mirar columna por columna y solo los que son de tipo string o object, se le aplica un lambda 
# este lambda mira si el string es "" y hace una suma de todos los que aparecen

print("Datos vacíos (no nulos) por columna:")
print(vacios_por_columna)
print("\nTotal de celdas vacías en todo el DataFrame:", vacios_por_columna.sum())