from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import numpy as np
from scipy.sparse import csr_matrix
import pandas as pd
import csv
import math

def abrirArchivo(nombre):
    with open(nombre+".txt", encoding="UTF-8") as archivo_entrada:
        dataset = archivo_entrada.read()
    return dataset

def binarizada(corpus,regex,binaria=True,vectorizer=False):
    if(not vectorizer):
        vectorizador = CountVectorizer(binary=binaria, token_pattern= regex)
    else: 
        vectorizador = TfidfVectorizer(token_pattern= regex)
    X = vectorizador.fit_transform(corpus)
    """print (vectorizador.get_feature_names_out())
    print (X)#sparse matrix
    print (type(X))#sparse matrix
    # ~ print (type(X.toarray()))#dense ndarray
    print ('Representación vectorial binarizada')
    print (X.toarray())#dense ndarray """
    print (X)
    columnas = vectorizador.get_feature_names_out()

    return X,columnas

def csv(X,columnas,nombre):
    X = csr_matrix(X)
    df = pd.DataFrame.sparse.from_spmatrix(X, columns=columnas)
    print(df) 
    df.to_csv(nombre)



if __name__=="__main__":
    corpus = abrirArchivo("corpus_generado")
    corpus = re.split("\n",corpus)
    regex = r'(?u)\w\w+|\w\w+\n|[\.\,\?\!\¿\¡\:\;]'
    print(len(corpus))
    X,columnas = binarizada(corpus,regex)

    X2 = binarizada(corpus,regex,False)
    X3 = binarizada(corpus,regex, vectorizer=True)

    csv(X,columnas,"representacion_binaria.csv")
    csv(X2,columnas,"representacion_frecuencia.csv")
    csv(X3,columnas,"representacion_tf-idf.csv")

    



