from comun.try_except import try_except_int
from web_scraping.web_scraping import web_scraping

from web_scraping.crear_dataframe_web_scraping import crear_dataframe_web_scraping

from api.api_deezer import buscar_api_crear_df

from api.dataframe_api import df_limpio

from comun.fusionar_dataframes import limpiar_dataframe_final, fusionar_dataframes

from graficos.histograma import generar_histograma_duracion, generar_histograma_duracion_por_año, generar_histograma_fans

from graficos.blotpox_outliers import generar_boxplot

from calculos.calculos_estadistica import calcular_estadisticas_numericas

from graficos.barras import diagramas_barras

from graficos.dispersion import diagramas_dispersion

from graficos.mapa_calor import mapa_calor
def menu_general():

    print("0 salir")
    print("1 generar dataframe web scraping")
    print("2 generar dataframe API")
    print("3 generar dataframe conjunto")
    print("4 calculos estadisticos de datos")



def menu_web_scraping():

    print("0 salir")
    print("1 sacar datos de web scraping")
    print("2 crear_dataframe_web_scraping")


def menu_api():

    print("0 salir")
    print("1 buscar datos api")
    print("2 limpiar dataframe")



    
def menu_grafica():

    print("0 salir")
    print("1 histograma")
    print("2 barras")
    print("3 blotpox")
    print("4 dispersion")
    print("5 mapa de calor")


def web_scraping_menus():

    opcion_web_scraping = -1 

    dataframe_web_scraping = None

    while(opcion_web_scraping != 0):

            menu_web_scraping()

            opcion_web_scraping = try_except_int("escoge una opcion: ")

            while(opcion_web_scraping < 0 or opcion_web_scraping > 2):

                menu_web_scraping()
                opcion_web_scraping = try_except_int("escoge una opcion correcta: ")


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
        
        opcion_api = try_except_int("escoge una opcion: ")

        while(opcion_api < 0 or opcion_api > 2):

            menu_api()
            opcion_api = try_except_int("escoge una opcion correcta: ")

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


def ver_no_ver_dataframe(df): # funcion para decidir si el usuario quiere ver que datos hay en el dataframe 
# final 

    opcion_ver_dataframe = try_except_int("pon 1 si quieres ver el dataframe final, 0 en caso contrario: ")

    while(opcion_ver_dataframe != 0 and opcion_ver_dataframe != 1): # si no es ni 0 ni 1 vuelve a pedir un dato
                    
        opcion_ver_dataframe = try_except_int("pon un dato correcto, 1 si quieres ver el dataframe final, 0 en caso contrario: ")
                
                
    if (opcion_ver_dataframe == 1): # si es 1 mostramos el tmaño de el dataframe

        print("tamaño del dataframe fusionado:", df.shape)
        print(df.head())

        print("tamaño de los datos en total :", df.shape[0]*df.shape[1])

        print("valores vacíos que quedan:", df.isna().sum().sum())

        print(df.info()) # mostramos los datos de el dataframe





menu_general()

opcion = -1

while(opcion != 0): # bucle que solo sale si se escribe un 0

    opcion = try_except_int("escoge una opcion: ")

    while(opcion < 0 or opcion > 4):

        menu_general()

        opcion = try_except_int("escoge una opcion correcta: ")


    if (opcion == 1): # opciones de solo la web_scraping
        
        dataframe_web_scraping = web_scraping_menus()


    elif (opcion == 2):

        dataframe_api_scraping = api_menu()

    elif (opcion == 3):

        
        menu_grafica()

        opcion_grafica = try_except_int("escoge una opcion: ")

        while(opcion_grafica != 0):

            while(opcion_grafica < 0 or opcion_grafica > 5):

                opcion_grafica = try_except_int("escoge una opcion correcta: ")


            if (opcion_grafica != 0):

                df = limpiar_dataframe_final(fusionar_dataframes())

                ver_no_ver_dataframe(df)

                if (opcion_grafica == 1):

                
                    print("histograma general")
                    
                    generar_histograma_duracion(df)

                    año_elegido = try_except_int("Introduce el año que quieres visualizar entre 2005-2025, 0 para salir: ")
                    
                    if (año_elegido != 0):

                        while(año_elegido < 2005 or año_elegido > 2025):

                            año_elegido = try_except_int("Introduce el año que quieres visualizar, 0 para salir: ")

                        if (año_elegido != 0):

                            generar_histograma_duracion_por_año(df, año_elegido)

                        
                    
                    generar_histograma_fans(df)

                    opcion_grafica = 0

                elif(opcion_grafica == 2):

                    diagramas_barras()

                elif (opcion_grafica == 3):

                    tabla = input("escribe que grafica quieres ver el blotpox: ")

                    generar_boxplot(df, tabla)

                    opcion_grafica = 0

                elif (opcion_grafica == 4):

                    diagramas_dispersion()

                elif (opcion == 5):
                    mapa_calor()

    
    elif(opcion == 4):

        resultado = calcular_estadisticas_numericas(limpiar_dataframe_final(fusionar_dataframes()))

        print(resultado)
