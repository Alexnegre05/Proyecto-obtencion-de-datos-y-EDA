from comun.try_except import try_except_int
from web_scraping.web_scraping import web_scraping

from web_scraping.crear_dataframe_web_scraping import crear_dataframe_web_scraping

from api.api_deezer import buscar_api_crear_df

from api.dataframe_api import df_limpio

from comun.fusionar_dataframes import limpiar_dataframe_final, fusionar_dataframes

from graficos.histograma import generar_histograma_duracion, generar_histograma_duracion_por_año, generar_histograma_fans
def menu_general():

    print("0 salir")
    print("1 generar dataframe web scraping")
    print("2 generar dataframe API")
    print("3 generar dataframe conjunto")



def menu_web_scraping():

    print("0 salir")
    print("1 sacar datos de web scraping")
    print("2 crear_dataframe_web_scraping")


def menu_api():

    print("0 salir")
    print("1 buscar datos api")
    print("2 limpiar dataframe")



def web_scraping_menus():

    opcion_web_scraping = -1 

    dataframe_web_scraping = None

    while(opcion_web_scraping != 0):

            menu_web_scraping()

            opcion_web_scraping = try_except_int("escoge una opcion")

            while(opcion_web_scraping < 0 or opcion_web_scraping > 2):

                menu_web_scraping()
                opcion_web_scraping = try_except_int("escoge una opcion correcta")


            if (opcion_web_scraping == 1):

                try:
                    web_scraping()
                except:
                    print("ya existe el archivo")

            elif(opcion_web_scraping == 2):

                try:
                    dataframe_web_scraping = crear_dataframe_web_scraping()
                except:
                    print("ya existe el dataframe")

    
    return dataframe_web_scraping






def api_menu():

    menu_api()

    opcion_api = -1

    dataframe_api_scraping = None

    while(opcion_api != 0):
        
        opcion_api = try_except_int("escoge una opcion")

        while(opcion_api < 0 or opcion_api > 2):

            menu_api()
            opcion_api = try_except_int("escoge una opcion correcta")

        try:

            if (opcion_api == 1):

                dataframe_api_scraping = buscar_api_crear_df()

            elif(opcion_api == 2):

                dataframe_api_scraping = df_limpio()

        except:

            print("ha habido un error")

            opcion_api = -1

        menu_api()



    return dataframe_api_scraping

    





menu_general()

opcion = -1

while(opcion != 0): # bucle que solo sale si se escribe un 0

    opcion = try_except_int("escoge una opcion: ")

    while(opcion < 0 or opcion > 3):

        menu_general()

        opcion = try_except_int("escoge una opcion correcta: ")


    if (opcion == 1): # opciones de solo la web_scraping
        
        dataframe_web_scraping = web_scraping_menus()


    elif (opcion == 2):

        dataframe_api_scraping = api_menu()

    elif (opcion == 3):

        df = limpiar_dataframe_final(fusionar_dataframes())

        print("histograma general")
        generar_histograma_duracion(df)

        año_elegido = try_except_int("Introduce el año que quieres visualizar entre 2005-2025, 0 para salir: ")
        
        if (año_elegido != 0):

            while(año_elegido < 2005 or año_elegido > 2025):

                año_elegido = try_except_int("Introduce el año que quieres visualizar, 0 para salir: ")

            if (año_elegido != 0):

                generar_histograma_duracion_por_año(df, año_elegido)

            
            generar_histograma_fans(df)