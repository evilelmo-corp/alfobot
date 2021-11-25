import random
import pandas as pd
import nltk
import numpy as np

nltk.download('punkt')
nltk.download('spanish_grammars')
nltk.download('vader_lexicon')
nltk.download('stopwords')

def tokenizar():
  df=pd.io.json.read_json('frases.json')
  df.columns=['frase']

  palabras_funcionales=nltk.corpus.stopwords.words("spanish")
  inf_funcionales=nltk.corpus.stopwords.words("english")
  palabras_funcionales.extend([".", ",", ":", ";", "!", "?","'","-"])
  palabras_funcionales.extend(inf_funcionales)

  #frecuentes=[]
  df2=df["frase"].apply(lambda x: nltk.word_tokenize(x,"spanish"))

  df["tokenizado"]=df2
  print(df["tokenizado"])
  for ind in range(len(df['frase'])):
      tokens_limpios=list()
      #print(ind)
      #print(df["frase"].iloc[ind])
      for tok in df["tokenizado"].iloc[ind]:
          if tok.lower() not in palabras_funcionales:
              tokens_limpios.append(tok.lower())
      print(ind,tokens_limpios)
      df.at[ind,"tokenizado"]=tokens_limpios

  conjunto=set()
  for n in range(len(df["tokenizado"])):
      for f in df["tokenizado"].iloc[n]:
          if f in conjunto:
              if df[f].iloc[n] > 0:
                  df[f].iat[n]+=1
              else:
                  df[f].iat[n]=1
          else:
              conjunto.add(f)
              df[f]=0
              df[f].iat[n]=1

  df.to_json("frasest.json")