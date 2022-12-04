import spacy 
import re
import pandas as pd
nlp = spacy.load("es_core_news_sm")


def abrirArchivo(nombre):
    with open(nombre+".txt", encoding="UTF-8") as archivo_entrada:
        dataset = archivo_entrada.read()
    return dataset

def obtener_palabras_diferentes(noticia):
    lista = []
    #quitamos signos de puntuacion solo para esto
    signos = '[.,\/#!$%\^&\*;:{}=\-_`~()”“"…]'
    stop_words = nlp.Defaults.stop_words
    for palabra in noticia: 
        palabra_limpia =  re.sub(signos,"",palabra).lower()
        #sino esta agregada ya y ademas no es stoprword
        if(palabra_limpia not in lista and palabra_limpia not in stop_words):
            lista.append(palabra_limpia)

    return lista[:len(lista)-1]

def obtener_frases(noticia):
    lista = []
    signos = '[.,\/#!$%\^&\*;:{}=\-_`~()”“"…]'
    stop_words = nlp.Defaults.stop_words
    frase = ""
    #index  = list(stop_words).index('tres')
    #print("XD",list(stop_words)[index])

    for palabra in noticia:
        #si choca con signo de puntuación 
        signo = re.compile(signos)
        tiene_signo = re.findall(signo,palabra)
        #print(len(tiene_signo))
        if(palabra.lower() not in stop_words):
            frase+=palabra.lower()+" "
            if(len(tiene_signo)>0):
                frase = re.sub(signos,"",frase)
                #frase = frase.strip()
                if(frase!=""):
                    #frase = re.sub("\s{2,}"," ",frase)
                    frase = frase[:len(frase)-1]
                    lista.append(frase)
                frase = ""
            
            #print(frase)
        else:
            #print(palabra)
            if(frase!=""):
                frase = frase[:len(frase)-1]
                lista.append(frase)
            frase = ""
    if(frase!=""):
        frase = frase[:len(frase)-2]
        lista.append(frase)

    return lista 

def putuacion_frase(data,lista_frases):
    #planets[planets.method == 'Pulsar Timing']
    puntuaciones_frase = []
    for frase in lista_frases:
        palabras = frase.strip().split(' ')
        puntuacion = 0
        for palabra in palabras: 
            puntuacion_palabra = data[data["palabra"] == palabra] 
            #print("xd",puntuacion_palabra)
            puntuacion_palabra = puntuacion_palabra["puntuacion"].values[0] if not puntuacion_palabra.empty else 0
            puntuacion+=puntuacion_palabra
        puntuaciones_frase.append(puntuacion)
    dic = {
        "frase":lista_frases,
        "puntuacion":puntuaciones_frase
    }
    data = pd.DataFrame(dic)
    data = data[data["puntuacion"] > 1.0]#todas las mayores a 1

    data = data.sort_values('puntuacion',ascending=False)
    ##data = data["frase"].unique()
    #print(data)

    return data


def obtener_grado(lista_palabras,lista_frases):
    lista_frecuencias = []
    lista_grados = []
    lista_puntuacion = []

    for l in lista_palabras:
        #l.append(1) #añadimos el grado consigo mismo
        #encontramos las frases en las que aparezca la palabra 
        filtro = list(filter(lambda x: (l in x.split(' ')), lista_frases))
        #esta longitud nos da la frecuencia
        lista_frecuencias.append(len(filtro))
        #una vez obtenidas, agregamos las concurrencias, que serían el total de palabras
        longitud_grado =  sum( [len(re.split(' ',x.strip())) for x in filtro ] )
        lista_grados.append(longitud_grado)
        #añadimos la puntuacion
        lista_puntuacion.append(longitud_grado/len(filtro)) if (len(filtro)>0) else 0
        #print(l, list(filtro),longitud_grado)
        #l.append(len(filtro))
    #creamos un dataframe
    dic = {
        "palabra":lista_palabras,
        "grado":lista_grados,
        "frecuencia":lista_frecuencias,
        "puntuacion":lista_puntuacion
    }
    data = pd.DataFrame(dic)
    #ordenamos por puntaje
    data = data.sort_values('puntuacion',ascending=False)
    return data

def obtener_valores(noticia):
    
    lista_palabras = obtener_palabras_diferentes(noticia)
    #print(lista_palabras[:20])
    lista_frases = obtener_frases(noticia)
    #print(lista_palabras)
    #print(lista_frases)
    lista_grados = obtener_grado(lista_palabras,lista_frases)
    #print(lista_grados)
    puntuaciones_frases = putuacion_frase(lista_grados,lista_frases)
    print(puntuaciones_frases.head(80))

    return lista_grados,puntuaciones_frases



if __name__ == "__main__":
    corpus = abrirArchivo("corpus_sin_lematizar")
    corpus = re.split("\n",corpus)
    #separamos por espacios cada elemento,, token= " "
    noticias = [re.split(" ",c) for c in corpus]

    datas = []
    puntuaciones = []
    for noticia in noticias[len(noticias)-2:len(noticias)-1]: 
        data,puntuacion_frase = obtener_valores(noticia)
        datas.append(data)
        puntuaciones.append(puntuacion_frase)
        #print(data.head(5))
        
    
    #print(lista_palabras)
    #print(lista_palabras)
   
    

    #corpus = re.split("\n",corpus)

   
