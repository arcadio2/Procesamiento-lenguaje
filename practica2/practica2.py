#Aguilera Gómez DOnaji
#Ayala Gónzales Ricardo Angel
#Cruz Hernández Yexalen
#López Guerrero Arcadio

import spacy 
import re
nlp = spacy.load("es_core_news_sm")

def crearArchivoSalida(nombre,normalizado):
    archivo_salida = open(nombre+".txt", 'w', encoding="UTF-8")
    archivo_salida.write(normalizado)
    archivo_salida.close()


def abrirArchivo(nombre):
    with open(nombre+".txt", encoding="UTF-8") as archivo_entrada:
        dataset = archivo_entrada.read()
    return dataset

def extraer(dataset):
    #elimina los caracteres que están al final de las noticias que son de diferentes tipos
    #Estos caracteres son tipo: aaaa&&&&& o dasksda&&&
    patron = re.sub("[a-z]{0,5}[\s]{0,6}[&]{2,}([0-9,]{1,}[,0-9]{1,}){2,}","",dataset)
    #eliiminamos el titulo, ya que está encerrado entre 2 cadenas del tipo &&&& algo.. &&&
    patron = re.sub("[0-9]{2,}[&]{2,}.{1,}[&]{2,}","",patron)
    #este quita los caracteres como __user__ __url__ _url_
    patron  = re.sub("[()]{0,1}[ ]{0,1}[_]{1,}[a-zA-Z]{1,}[_]{1,}[ ]{0,1}[)]{0,1}","",patron)
    patron = re.sub("\s{2,}"," ",patron)
    #patron = re.sub("[&]{3,}","",patron)
    #res = patron.findall(dataset)
    res = re.split("\n",patron) #las separamos por salto de linea, cada noticia está una linea
    return res


"""
Esta función es para normalizar nuestro texto, aquí mandaremos cada noticia de nuestro corpus
"""
def normalizar(data): 
    #usamos spacy para llevar el texto a su forma base
    doc = nlp(data) #lematización
    normalizado = "" #cadena para agregar el texto normalozado
    ban = True
    
    for token in doc:
        #print(token.text, token.pos_, token.dep_, token.lemma_) #texto/verbo,adverbio,etc.//forma base
        #las hacemos minusculas todas
        normalizado = normalizado + token.lemma_.lower() + " "

    #quitamos posibkes espacios repetidos
    normalizado = " ".join(re.split(r"\s+", normalizado))
    return normalizado

def listaNormalizada(lista):
    nueva = []
    for l in lista: 
        normalizada = normalizar(l)
        nueva.append(normalizada)
    return nueva

def generarArchivo(lista,nombre):
    texto = ""
    for l in lista:
        texto+=l+"\n"
    texto = texto[:len(texto)-1]
    archivo_salida = open(nombre+'.txt', 'w', encoding="UTF-8")
    archivo_salida.write(texto)
    archivo_salida.close()

"""Función que remueve stopwords"""
def removeStopWords(text):
    #Nos da las stop_words en el, idioma que hayamos definido
    stop_words = nlp.Defaults.stop_words
    #separamos el texto en palabras, para que pueda identificarlas, cada palabra se separa por espacio
    palabras = re.split(" ",text)
    #print(stop_words)
    #nuestro texto sin stop words
    without = [word for word in palabras if not word in stop_words]
    #convertimos la lista resultante en texto 
    final = " ".join(without)
    return final
    #stopword_es = nltk.corpus.stopwords.words('spanish')

if __name__=="__main__":
    dataset = abrirArchivo("corpus_noticias")
    data = extraer(dataset)
    data = data[:len(data)-1] #eliminamos el ultimo elemento que sale vacío
    generarArchivo(data,"corpus_sin_lematizar")
    #print(data[:10]) #imprime del primero al decimo
    #print(len(data)) #longitud de las noticias que son 635
    
    print("______________________Normalizado_________________________")
    normalizada = listaNormalizada(data)
    print(normalizada[0])
    #solo para probar guardamos el archivo con stop words
    generarArchivo(normalizada,"corpus_con_stopwords")
    #removemos los stop words de cada noticia, recorriendo la lista y pasandola por la función
    normalizada_sw = [removeStopWords(noticia) for noticia in normalizada]
    print(normalizada_sw[0])
    #doc = nlp(dataset)
    #generamos el archivo mandando la lista final
    generarArchivo(normalizada_sw,"corpus_generado")

