from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors

sentences = [['i', 'like', 'apple', 'pie', 'for', 'dessert'],
           ['i', 'dont', 'drive', 'fast', 'cars'],
           ['data', 'science', 'is', 'fun'],
           ['chocolate', 'is', 'my', 'favorite'],
           ['my', 'favorite', 'movie', 'is', 'predator']]
           
# Emtrenamiento de un modelo word2vec
model = Word2Vec(sentences, min_count=1, vector_size = 5)
print(model)
model.save("word2vec.model")
model = Word2Vec.load("word2vec.model")
vector = model.wv['chocolate']
print(vector)
result = model.wv.most_similar('chocolate')
print(result)


#Carga de un modelo pre-entrenado en formato txt
model = KeyedVectors.load_word2vec_format('SBW-vectors-300-min5_recortado.txt')

#Imprime el más similar
result = model.most_similar('año')
most_similar_key, similarity = result[0]
print(f"{most_similar_key}: {similarity:.4f}")
#Imprime el término que no tiene relación
print(model.doesnt_match(['carro', 'moto', 'bicicleta', 'cereal']))

#Analogía
result = model.most_similar(positive=['mujer', 'rey'], negative=['hombre'], topn=3)
print (result)#Imprime los términos similares









