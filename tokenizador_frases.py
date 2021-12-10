import random
import pandas as pd
import nltk
import numpy as np
from cogs import modelolemat

nltk.download('punkt')
nltk.download('spanish_grammars')
nltk.download('vader_lexicon')
nltk.download('stopwords')

def tokenizar():
  df=pd.io.json.read_json(f'cogs/datos/frases.json')
  df.columns=['frase']
  #frecuentes=[]
  df2=df["frase"].apply(lambda x: modelolemat.lematizer(x))

  df["tokenizado"]=df2
  print(df["tokenizado"])
  for ind in range(len(df['frase'])):
      tokens_limpios=list()
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

  df.to_json(f'cogs/datos/frasest.json')