import spacy

#python -m spacy download es

nlp = spacy.load("es_core_news_sm")

#archivo_entrada = open('ejercicio-1/archivo_entrada.txt', 'r')

#for line in archivo_entrada:
#	print (line, end='')

#archivo_entrada.close()

#Aquí no es necesario el llamado a close ya que lo hace automáticamente
with open('ejercicio-1/archivo_ejercicio_entrada.txt', encoding="UTF-8") as archivo_entrada:
	dataset = archivo_entrada.read()

#print (dataset)

doc = nlp(dataset)

normalizado = ""
ban = True
for token in doc:
    #print(token.text, token.pos_, token.dep_, token.lemma_) #texto/verbo,adverbio,etc.//forma base
    

    if(token.text=="\n"):
        ban = False
    elif(token.text=="\n\n"):
        ban = False
        normalizado+="\n"
    else: 
         normalizado = normalizado + token.lemma_ 
         ban = True

    if(ban):
      normalizado +=  " "
    
    
print (normalizado)

archivo_salida = open('ejercicio-1/archivo_salida.txt', 'w', encoding="UTF-8")
archivo_salida.write(normalizado)
archivo_salida.close()