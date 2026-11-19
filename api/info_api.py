import pandas as pd


# Cargamos los datos preparados de la API
df = pd.read_csv("data/processed/deezer_canciones_preparado.csv", parse_dates=["fecha_lanzamiento", "fecha_obtencion"])


# 1. Tamaño
print("Filas y columnas:", df.shape)


# 2. Tipos de datos y valores no nulos
print()
df.info()


# 3. Tipo de cada variable
tipos = {
  "titulo": "texto",
  "artista": "texto",
  "deezer_titulo": "texto",
  "deezer_artista": "categórica",
  "duracion_s": "numérica continua",
  "explicita": "booleana",
  "popularidad_deezer": "numérica discreta",
  "sello_deezer": "categórica",
  "fecha_lanzamiento": "fecha",
  "tipo_lanzamiento": "categórica",
  "genero": "categórica",
  "artista_fans": "numérica discreta",
  "fecha_obtencion": "fecha",
  "coincidencia_correcta": "booleana",
  "anio_lanzamiento": "numérica discreta",
}

tabla = pd.DataFrame(tipos.items(), columns=["variable", "tipo"])
print()
print(tabla.to_string(index=False))