from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import numpy as np
from scipy.sparse import csr_matrix
import pandas as pd
import csv
import math
import matplotlib.pyplot as plt
import seaborn as sns 

def representacion_palabras(corpus,regex,binaria=True,vectorizer=False):
    columnas = []
    if(not vectorizer):
        vectorizador = CountVectorizer(binary=binaria, token_pattern= regex)
            
    else: 
        vectorizador = TfidfVectorizer(token_pattern= regex)

    X = vectorizador.fit_transform(corpus)
    columnas = vectorizador.get_feature_names_out()
    """print (vectorizador.get_feature_names_out())
    print (X)#sparse matrix
    print (type(X))#sparse matrix
    # ~ print (type(X.toarray()))#dense ndarray
    print ('Representación vectorial binarizada')
    print (X.toarray())#dense ndarray """
    print (X.toarray())
   

    return X,columnas

def abrirArchivo(nombre):
    with open(nombre+".txt", encoding="UTF-8") as archivo_entrada:
        dataset = archivo_entrada.read()
    return dataset

def cosine(x, y):
    
    val = sum(x[index] * y[index] for index in range(len(x)))
    sr_x = math.sqrt(sum(x_val**2 for x_val in x))
    sr_y = math.sqrt(sum(y_val**2 for y_val in y))
    res = val/(sr_x*sr_y)
    return (res)

def similitud(dataset):
    print("FUNCION")
    data = list(dataset.toarray())
    print("DATA",len(data[0]))
    #data = data[:10]

    #print(len(list(dataset)))
    #aplicamos la primera con la primera a la ultima
    #luego la segunda desde esa a la ultima
    index = 0 
    similitudes = []
    for i in data: 
        #print(data[index+1:])
        #desde la 0 a la ultima en la primera iteracion
        x = [] #aqui se guardan la distancias para cada documento
        for j in range(len(data)):  
            coseno = cosine(i,data[j])
            x.append(coseno)
        similitudes.append(x) #guarda la matriz de similaridades
        index+=1
    return similitudes 

def encontrar_llave(elemento):
    return elemento['valor']


        

def similares(similitud):
    #obtenemos los 100 mayores de cada lista
    similitudes = np.array(similitud)
    similitudes = np.delete(similitudes,0,axis=1)
    mayores = []
    
    #print(xd)
    i = 0
    for s in similitudes: #recorremos filas
        valores = s
        maximos = []
        for j in range(10):#los 10 mas grandes de cada noticia 
            xd = np.where(valores == np.amax(valores))
            #print(valores)
            #print("Valor",valores[xd[0][0]])
            if(xd[0][0]!=i):
                dic = {
                    "punto":(i,xd[0][0]),
                    "valor":valores[xd[0][0]]
                }
                maximos.append(dic)#guardamos los indices
            valores[xd[0][0]] = 0 
                
        mayores.append(maximos)
        #print(maximos)

        i+=1
    print(np.array(mayores).shape) 
        #print(s)
    """Obtenemos los maximos que no sean de la misma posicion, es decir
    que sean diferentes entre sí"""
    maximos = []
    for mayor in mayores: #recorremos filas
        for m in mayor:
            if(len(maximos)==0):
                maximos.append(m)
            else:
                #print(m,maximos)
                bandera = False
                for maximo in maximos:
                    if(maximo.get('punto')[0]==m.get('punto')[1]  #sino es el mismo punto
                        and maximo.get('punto')[1]==m.get('punto')[0]):
                        bandera = True
                        #
                        break
                if(not bandera):
                    maximos.append(m)
    
    #print(maximos)
    print(len(maximos))
    ##Encontramos los n maximos
    maximos_finales = sorted(maximos, key = lambda i: i['valor'], reverse=True)
    #obtenemos los n mas grandes
    maximos_finales = maximos_finales[:100]
    #maximos_finales = [m.get('punto') for m in maximos_finales]
    #print(maximos_finales)
    #for i in range(10):
    return maximos_finales

#esta función es solo para imprimir las noticias con los valores
def imprimir_100_maximos(similitud,tipo="binaria"):
    print("______________________________________________________________________")
    print("Similitud "+tipo)
    i = 0 
    for s in similitud:
        print(f"{i+1}.-noticia_{s.get('punto')[0]}-noticia_{s.get('punto')[1]} {s.get('valor')}")
        i+=1
    print("______________________________________________________________________")

def obtener_10_maximos(maximos,similitudes,tipo="binaria"): 
    similitudes = np.array(similitudes) 
    #eliminamos la columna de indices que crea pandas
    similitudes = np.delete(similitudes,0,axis=1)
    maximos_10 = []
    n = 0
    for m in maximos: 
        noticia_1,noticia_2 = m.get('punto')#obtenemos los pares de noticias
        if(noticia_1 not in maximos_10):#si no esta la primera ya en la lista
            maximos_10.append(noticia_1)
            n+=1
        if(noticia_2 not in maximos_10): #lsi la segunda no está en la lista, para que sean diferentes noticias
            maximos_10.append(noticia_2)
            n+=1
        if(n==10): #si ya tenemos 10, rompemos el ciclo
            break
    """Ahora los obtenemos en formato para el mapa de calor, con los valores"""
    print(maximos_10)
    data = []
    for maximo in maximos_10: 
        datos = [] #agregamos el primero con todos, el segundo con todos y así
        for m in maximos_10:
            similitud = similitudes[maximo][m]
            datos.append(similitud)
        data.append(datos)

        #guardamos una arreglo con las intersecciones de las noticias
    #print(data)
    """Creamos el data frame"""
    columnas = [f'noticia_{noticia}' for noticia in maximos_10]
    data = pd.DataFrame(data=data,columns=columnas,index=columnas)
    data.to_csv(f'10_mejors{tipo}.csv')
    print("__________________________________________________________")
    print(tipo)
    print(data)
    print("__________________________________________________________")
    return data

def generar_mapa_calor(data,tipo):
    sns.heatmap(data=data, cmap="Greens", annot=True)
    plt.title(f'Mapa de calor de {tipo}')
    plt.show()

def guardar_csv(X,columnas,nombre):
    X = csr_matrix(X)
    df = pd.DataFrame.sparse.from_spmatrix(X, columns=columnas)
    #print(df) 
    df.to_csv(nombre)
#~ print ('Word Similarity')
#~ cosine(data_words['computadora'], data_words['internet'])    
if __name__=="__main__":    
    corpus = abrirArchivo("corpus_generado")
    corpus = re.split("\n",corpus)
    regex = r'(?u)\w\w+|\w\w+\n|[\.\,\?\!\¿\¡\:\;]'
    #representacion binaria
    binaria,columnas = representacion_palabras(corpus,regex)
    
    frecuencia,columnas = representacion_palabras(corpus,regex,False)
    vectorizada,columnas = representacion_palabras(corpus,regex, vectorizer=True)
    print(columnas)

    #print(binaria)
    #print(frecuencia)
    #guardar csv binaria
    similitudes = similitud(binaria)
    columnas_noticias = [f'noticia_{i}' for i in range(len(similitudes))]
    guardar_csv(similitudes,columnas_noticias,"similitudes_binaria.csv")

    """"""
    #guardar csv frecuencia
    similitudes = similitud(frecuencia)
    columnas_noticias = [f'noticia_{i}' for i in range(similitudes)]
    guardar_csv(similitudes,columnas_noticias,"similitudes_frecuencia.csv")

    """"""
    #guardar csv tf-idf
    similitudes = similitud(vectorizada)
    columnas_noticias = [f'noticia_{i}' for i in range(similitudes)]
    guardar_csv(similitudes,columnas_noticias,"similitudes_vectorizer.csv")



    similitudes_binaria = pd.read_csv("similitudes_binaria.csv")
    maximos_binaria = similares(similitudes_binaria)

    similitudes_frecuencia = pd.read_csv("similitudes_frecuencia.csv")
    maximos_frecuencia = similares(similitudes_frecuencia)

    similitudes_vectorizada = pd.read_csv("similitudes_vectorizada.csv")
    maximos_vector = similares(similitudes_vectorizada)

    imprimir_100_maximos(maximos_binaria)
    imprimir_100_maximos(maximos_frecuencia,"frecuencia")
    imprimir_100_maximos(maximos_vector,"TF_IDF")
    data_binaria = obtener_10_maximos(maximos_binaria,similitudes_binaria)
    data_frecuencia = obtener_10_maximos(maximos_frecuencia,similitudes_frecuencia,"frecuencia")
    data_vector = obtener_10_maximos(maximos_vector,similitudes_vectorizada,"vectorizada")

    generar_mapa_calor(data_binaria,"Binaria")
    generar_mapa_calor(data_frecuencia,"Frecuencia")
    generar_mapa_calor(data_vector,"TF_IDF")
    

    

