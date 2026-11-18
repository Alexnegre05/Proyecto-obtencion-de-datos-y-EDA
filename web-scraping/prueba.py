import requests

url = "https://www.officialcharts.com/charts/end-of-year-singles-chart/20250101/37501/" # escribimos la url

respuesta = requests.get(url, timeout=15)

respuesta.raise_for_status()

html = respuesta.text # sacamos todo el html 

print(html)