import pandas as pd

ruta = r"D:\Alex Negre IA+BD\Proyecto-obtencion-de-datos-y-EDA\data\raw"

df = pd.read_csv(f"{ruta}\\officialcharts_2005_2025.csv") # ya tenemos el dataframe


df_copy = df.copy() # hacemos una copia de el dataframe de seguretat

# mostramos el tamaño de la matriz asi como cuantos datos 
print("tamaño total de la matriz m*n es", df.shape) 


print("En total tenemos", df.shape[0]*df.shape[1], "datos") 

print(df.head())