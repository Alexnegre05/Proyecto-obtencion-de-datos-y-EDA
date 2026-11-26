def try_except_int(string):

    comprovar = 0 # variable para ver si el usuaraio a escrito bien los datos

    while(comprovar == 0): # solo salimos de la funcion si el try no peta

        try:

            resultado = int(input((string)))
            comprovar = 1

        except:
            comprovar = 0 # si va a except el comprovar pasa a 0

            print("introduce un valor entero")

    
    return resultado


def try_except_float(string):

    comprovar = 0 # variable para ver si el usuaraio a escrito bien los datos

    while(comprovar == 0): # solo salimos de la funcion si el try no peta

        try:

            resultado = float(input((string)))
            comprovar = 1

        except:
            comprovar = 0 # si va a except el comprovar pasa a 0

            print("introduce un valor racional")

    
    return resultado



def try_except_string(string):

    comprovar = 0 # variable para ver si el usuaraio a escrito bien los datos

    while(comprovar == 0): # solo salimos de la funcion si el try no peta

        try:

            resultado = input((string))
            
            comprovar = 1

        except:
            comprovar = 0 # si va a except el comprovar pasa a 0

            print("introduce un valor de texto")

    
    return resultado