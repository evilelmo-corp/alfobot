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