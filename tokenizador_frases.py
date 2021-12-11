import random
import pandas as pd
import nltk
import numpy as np
import requests
from bs4 import BeautifulSoup
import pickle
from nltk.tokenize import word_tokenize
import time

# nltk.download('punkt')
# nltk.download('spanish_grammars')
# nltk.download('vader_lexicon')
# nltk.download('stopwords')

def lemmascrapper(token):
  """Escrapea en the free dictionary la palabra recibida y averigua si su lema, si no lo encuentra devuelve un error"""
  url="https://es.thefreedictionary.com/"+token
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
  req = requests.get(url, headers=headers)
  soup= BeautifulSoup(req.text, "lxml")
  resultado=soup.find('div', class_="content-holder")
  print(resultado.h1.text,"RESULTADO SCRAP")
  #Control de que sea una palabra real
  if soup.find('div', id="Definition") == None:
    raise ValueError("Esta palabra no lleva a ningún lema")
  else:
    tipo=soup.find('i')
    return resultado.h1.text,tipo.text[0]


def lemmatizer(to_tokenize):
  #Abre el lemma en vinagre; es un dataset.
  with open(f'cogs/datos/rayo_lemmatizador' , 'rb') as f:
    lemma_ray = pickle.load(f)

  #también sacamos de conserva el dataset de las palabras
  #contiene 14 atributos de cada palabra + el target (POS)
  with open(f'cogs/datos/X_train' , 'rb') as f:
    superinfo = pickle.load(f)

  sustantivos = superinfo[superinfo['POS']=='NOUN'].Palabra.value_counts().index
  verbos = superinfo[superinfo['POS']=='VERB'].Palabra.value_counts().index



    #Creamos variable que será una lista de tokens de la frase inicial
    #la lista irradiated son las palabras de la frase lemmatizadas ya.
    #la lista topics son los lemmas de los SUSTANTIVOS y VERBOS de la frase
    #la lista sin_lemma son los tokens que no están registrados ni tienen lemma

  sentence = word_tokenize(to_tokenize)
  irradiated, topics, sin_lemma = [],[],[]

  for token in sentence:
    lemma = lemma_ray[lemma_ray['Form']==token].lemma.values
    try:
      irradiated.append(lemma[0])
    except:
      sin_lemma.append(token)
    if token in sustantivos:
      topics.append(lemma[0])
    elif token in verbos:
      topics.append(lemma[0])
  #añadiendo lectura del diccionario a los tokens no lematizados
  sin_lemma_def=[]
  print(sin_lemma,"sinlema",len(sin_lemma))
  print(irradiated,"irradiated",len(irradiated))
  print(topics,"topics",len(topics))
  for tok in sin_lemma:
    time.sleep(random.randint(0,7))
    try:
      print(tok,"TOK")
      lema,tipo =lemmascrapper(tok)
      irradiated.append(lema)
      if tipo == "s" or tipo == "v":
        topics.append(lema)
    except:
      sin_lemma_def.append(tok)
  print(sin_lemma_def,"sin_lemma_def",len(sin_lemma_def))
  if len(sin_lemma_def)>0:
    try:
      with open(f"cogs/datos/a_lemmatizar.txt","a") as fh:
        for elemento in sin_lemma_def:
          fh.write(";"+elemento)
    except:
      pass
  topics.extend(sin_lemma_def)
  print(topics)
  return topics

def tokenizar():
  df=pd.io.json.read_json(f'cogs/datos/frases.json')
  df.columns=['frase']
  #frecuentes=[]
  df2=df["frase"].apply(lambda x: lemmatizer(x))

  df["tokenizado"]=df2
  print(df["tokenizado"])

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
def tokenizador_frase_unica(frase):
  """ Incluye frases en la base de datos de frases y las tockeniza,
  Además comprueba que no estén antes, ni la frase ni los lemmas-tokkens """
  df=pd.io.json.read_json(f'cogs/datos/frasest.json')
  if frase in df['frase'].values:
    return "Mi genialidad ya incluía esta frase"
  u_linea=len(df)
  row=[0 for x in range(len(df.columns))]
  row[0]=frase
  row[1]=lemmatizer(frase)
  if row[1] in list(df['tokenizado'].values):
    return "Mi genialidad ya incluía esta frase"
  df.loc[u_linea]=row
  df.to_json(f'cogs/datos/frasest.json')
  return "Obvio que pensaba decir eso más adelante"



