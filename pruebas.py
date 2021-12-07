import pandas as pd

df=pd.load_json('frases.json')

print(df)

import nltk
tokens=nltk.word_tokenize(message.content,"spanish")
nltk.download('stopwords')
palabras_funcionales=nltk.corpus.stopwords.words("spanish")
palabras_funcionales.extend([".", ",", ":", ";", "!", "?","'" ])
tokens_limpios=[] 
tokens = [token.lower() for token in tokens]
for token in tokens: 
    if token not in palabras_funcionales: 
        tokens_limpios.append(token)



        #,"cod vpca":"from sklearn.decomposition import PCA \n pca = PCA() \n X_train_pca = pca.fit_transform(X) \n pca.explained_variance\_ratio\_ \n plt.figure(figsize=(8,6)) \n plt.bar(range(1, len(numerodecolumnas)), pca.explained\_variance\_ratio\_) \n plt.ylabel('Varianza explicada')   # puedo definir un corte en la cantidad de Z que quiero de acuerdo a la cantidad acumulada de varianza explicada. \n  plt.xlabel('PCA Index')  # lo ideal es quedarse con una varianza acumulada del 60% (en este caso las tres primeras barras explcian el 60% de la varianza explicada) \n plt.show() \n #pca.explained_variance_ratio_.cumsum()"
