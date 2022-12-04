from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import re
import pandas as pd
from scipy import spatial
import matplotlib.pyplot as plt
import seaborn as sns 

def abrirArchivo(nombre):
    with open(nombre+".txt", encoding="UTF-8") as archivo_entrada:
        dataset = archivo_entrada.read()
    return dataset

def encontrar_mejores(modelo):
    #print(len(modelo.dv))
    mejores = []
    #los pasamos a una estructura diferente 
    for i in range(len(modelo.dv)): 
        mejor = modelo.dv.most_similar(modelo.dv[i])
        for m in mejor: 
            #si el punto es diferente solamenre 
            if(i!=m[0]):
                dic = {
                    "punto":(i,m[0]),
                    "valor":m[1]
                }
                mejores.append(dic)
    #ordenamos por valor de mayor a menor
    mayores_finales = sorted(mejores, key = lambda i: i['valor'], reverse=True)
    #obtenemos solo los 10 
    mayores_finales = mayores_finales[:10]

    #for mejor in mejores:

    print(mayores_finales)
    return mayores_finales

def generar_mapa_calor(data,tipo):
    sns.heatmap(data=data, cmap="Greens", annot=True)
    plt.title(f'Mapa de calor de {tipo}')
    plt.show()

def generar_dataset_mejores(maximos,modelo,text="10_mejores"):
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
    data = []
    for maximo in maximos_10: 
        datos = [] #agregamos el primero con todos, el segundo con todos y así
        for m in maximos_10:
            #similitudes = modelo.dv.most_similar(model.dv[maximo])
            #similitud = modelo.dv.n_similarity(modelo.dv[maximo],modelo.dv[m])
            #vec1 = modelo.infer_vector(tagged_data[maximo][0])
            #vec2 = modelo.infer_vector(tagged_data[m][0])
            similitud = abs(spatial.distance.cosine(modelo.dv[maximo],modelo.dv[m])-1)
            datos.append(similitud)
        data.append(datos)

        #guardamos una arreglo con las intersecciones de las noticias
    #print(data)
    """Creamos el data frame"""
    columnas = [f'noticia_{noticia}' for noticia in maximos_10]
    data = pd.DataFrame(data=data,columns=columnas,index=columnas)
    data.to_csv(text+".csv")
    print("__________________________________________________________")
    #print(tipo)
    #print(data)
    print("__________________________________________________________")
    return data

def imprimir_10_maximos(similitud,tipo):
    print("______________________________________________________________________")
    print("Similitud "+tipo)
    i = 0 
    for s in similitud:
        print(f"{i+1}.-noticia_{s.get('punto')[0]}-noticia_{s.get('punto')[1]} {s.get('valor')}")
        i+=1
    print("______________________________________________________________________")

def generar_datos(tagged_data):
    dm_s = [0,1]
    vector_sizes = [100,300]
    windows = [5,10]
    text = ""
    for i in range(2):
        for j in range(2):
            for k in range(2):
                model = Doc2Vec(tagged_data, 
                    vector_size=vector_sizes[i],dm=dm_s[j],window=windows[k])
                text = f'Vec_{str(vector_sizes[i])}-dm_{str(dm_s[j])}-win_{str(windows[k])}'
                model.save(text+'.model')
                model= Doc2Vec.load(text+'.model')
                mejores = encontrar_mejores(model)
                imprimir_10_maximos(mejores,text)
                data = generar_dataset_mejores(mejores,model,text)
                generar_mapa_calor(data,text)



if __name__ == "__main__":
    corpus = abrirArchivo("corpus_sin_lematizar")
    corpus = re.split("\n",corpus)
    #separamos por espacios cada elemento,, token= " "
    sentences = [re.split(" ",c) for c in corpus]

    #asigna un identificador a cada documento
    tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(sentences)]

    print(tagged_data[1])

   
    #reduce la dimensionalidad de los datos en un vector de 30 el parametro especificado
    model = Doc2Vec(tagged_data, vector_size=30)

    print(model.dv[0])
    # Save trained doc2vec model
    model.save("doc2vec.model")
    ## Load saved doc2vec model
    model= Doc2Vec.load("doc2vec.model")
    #obtiene los pares mas similares de cada documento 
    print(model.dv.most_similar(model.dv[359]))#regresa las11 mejores, con el indice y el valor
    mejores = encontrar_mejores(model)
    data = generar_dataset_mejores(mejores,model)
    generar_mapa_calor(data,"doc2vec")
    #print(sentences[0])
    #print(len(corpus))
    generar_datos(tagged_data)