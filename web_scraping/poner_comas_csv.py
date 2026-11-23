
ruta_archivo = r"D:\Alex Negre IA+BD\Proyecto-obtencion-de-datos-y-EDA\data\raw\officialcharts_2005_2025.csv"

filas = []
""
año_actual = None

fichero = open(ruta_archivo, "r", encoding="utf-8")


for linea in fichero: # vamos linea a linea en el fichero

    linea = linea.strip() # quitanos los espacios en blanco

    if linea.endswith("canciones:"): # mira si acaba con un texto de canciones:
        año_actual = int(linea.split()[0]) # guardamos el año actual

        continue

    partes = linea.split("|") # separamos las |

    cancion = {"año": año_actual, "indice": int(partes[0].strip())} # creamos diccionario con las variables de la cancion para reescribir el diccionario

    # añadimos el indice

        # Recorremos el resto de campos (posicion, titulo, artista, etc.)
    for bloque in partes[1:]:
        clave, valor = bloque.split(":", 1)  # separa solo por el primer ':'
        clave = clave.strip()
        valor = valor.strip()

        # Limpiamos las etiquetas HTML <time...> si es la columna primera_fecha
        if clave == "primera_fecha" and ">" in valor:
            valor = valor.split(">")[1].split("<")[0]

        cancion[clave] = valor

    filas.append(cancion)  # guardamos el diccionario en la lista

fichero.close()


# reescribimos el archivo
columnas = ["año", "indice", "posicion", "titulo", "artista", "pico", "semanas", "label", "catalogo", "primera_fecha"]

fichero_salida = open(ruta_archivo, "w", encoding="utf-8")

# Escribimos la cabecera
fichero_salida.write(",".join(columnas) + "\n")

# Escribimos cada canción
for cancion in filas:
    valores = []
    for col in columnas:
        dato = str(cancion[col])
        # Si el dato tiene una coma dentro, lo rodeamos de comillas para que no se parta la columna
        if "," in dato:
            dato = f'"{dato}"'
        valores.append(dato)
    
    fichero_salida.write(",".join(valores) + "\n")

fichero_salida.close()