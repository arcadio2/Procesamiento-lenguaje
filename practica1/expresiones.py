import re


def openTxtAsString(ruta):
    with open(ruta,encoding="utf8") as archivo: 
        data = archivo.read()
    #linea = archivo.readline()
    return data

def findUsersAsList(data):
    #w significa cualquier caracter menos saltos, espacios
    patron = re.compile('@{1}\w+')
    res = patron.findall(data)
    return res

def findHashtagsAsList(data):
    #w significa cualquier caracter menos saltos, espacios
    patron = re.compile('#{1}\w+')
    res = patron.findall(data)
    return res

def horasAsList(data):
    patron = re.compile(
        #espacio 0 o una vez
        '[0-9]{1,2}[h ]{0,1}[hrs]{0,1}:{1}[ ]{0,}[0-9]{2}[m ]{0,1}[h ]{0,1}'
        )
    res = patron.findall(data)
    return res

def fechasAsList(data):
    patron = re.compile(
        #espacio 0 o una vez
        "([0-9]{1,2}[/-]{1}[0-9]{1,2}[/-]{1}[0-9]{2,4})"
        )
    patron2 = re.compile(
        #espacio 0 o una vez
        "([0-9]{2,4}[/-]{1}[0-9]{1,2}[/-]{1}[0-9]{1,2})"
        )
    res = patron.findall(data)
    res2 = patron2.findall(data)
    return res + res2

def emojisAsList(data):
    patron = re.compile('(:{1}\w{1})')
   
    res = patron.findall(data)
    #res2 = re.search(['):'],data)
    return res 

def imprimir(lista):
    lista_1 = lista[:5]
    for l in lista_1: 
        print(l)


if __name__ == "__main__":
    data = openTxtAsString("practica1/tweets.txt")

    users = findUsersAsList(data)
    hashtagss = findHashtagsAsList(data)
    horas = horasAsList(data)
    fechas = fechasAsList(data)
    emojis = emojisAsList(data)

    print("users",len(users))
    print("hashtags",len(hashtagss))
    print("Horas",len(horas))
    print("Fechas",len(fechas))
    print("Emojis",len(emojis))

    """Primeros en lista"""
    imprimir(users)
    print("...")
    imprimir(hashtagss)
    print("...")
    imprimir(horas)
    print("...")
    imprimir(fechas)
    print("...")
    imprimir(emojis)
    print("...")
    #print(fechas)




    

