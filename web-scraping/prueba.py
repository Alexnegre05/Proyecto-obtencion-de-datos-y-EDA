import requests
from bs4 import BeautifulSoup

url = "https://www.officialcharts.com/charts/end-of-year-singles-chart/20250101/37501/" # escribimos la url

respuesta = requests.get(url, timeout=15)

respuesta.raise_for_status() # este conando detecta cuando el codigo http de vuelta de la pagian web POST con el html entregado no es 200 

html = respuesta.text # sacamos todo el html con .text

parser = BeautifulSoup(respuesta.text, "html.parser") # transforma el html en una especie de arbol

# .prettify añade espacios y lineas de texto

texto_html = parser.prettify()

print(texto_html) # esto nos muestra el html mas limpio

