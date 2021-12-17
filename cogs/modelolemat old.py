#modelolematizador - PRE-ADRI
import discord 
import pickle
from discord.ext import commands
from datetime import datetime
import random
import pandas as pd
from nltk.tokenize import word_tokenize
import re
import numpy as np
import math
import requests
from bs4 import BeautifulSoup
from collections import Counter
from os import remove
import nltk
import random

nltk.download('punkt')
nltk.download('spanish_grammars')
nltk.download('vader_lexicon')
nltk.download('stopwords')
palabras_funcionales=nltk.corpus.stopwords.words("spanish")
palabras_funcionales.extend([".", ",", ":", ";", "!", "?","'","#","...","-","$","``","''","(",")","¿","!" ])

# Variables declaradas globales por agilizar funciones. 

# Variables para lemmatizer:

global lemma_ray
global superinfo
global sustantivos
global verbos
global adjetivos

# df de lemmas
with open(f'cogs/datos/rayo_lemmatizador' , 'rb') as f:
	lemma_ray = pickle.load(f)

#conti 14 atributos de cada palabra + el target (POS)
with open(f'cogs/datos/X_train' , 'rb') as f:
	superinfo = pickle.load(f)

sustantivos = superinfo[superinfo['POS']=='NOUN'].Palabra.value_counts().index
verbos = superinfo[superinfo['POS']=='VERB'].Palabra.value_counts().index
adjetivos = superinfo[superinfo['POS']=='ADJ'].Palabra.value_counts().index

# Variables para creacionpool:
global df_frasest
global tokens_alfonso

df_frasest=pd.io.json.read_json(f'cogs/datos/frasest.json')
tokens_alfonso=df_frasest.columns.drop(['frase','tokenizado'])

#Ingreso de datos

def lemmascrapper(token):
	"""Escrapea en the free dictionary la palabra recibida y averigua si su lema, si no lo encuentra devuelve un error"""
	url="https://es.thefreedictionary.com/"+token
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	req = requests.get(url, headers=headers)
	soup= BeautifulSoup(req.text, "lxml")
	resultado=soup.find('div', class_="content-holder")
	# print(resultado.h1.text,"RESULTADO SCRAP")
	#Control de que sea una palabra real
	if soup.find('div', id="Definition") == None:
		raise ValueError("Esta palabra no lleva a ningún lema")
	else:
		tipo=soup.find('i')
		return resultado.h1.text,tipo.text[0]


def lemmatizer(to_tokenize):

    #Creamos variable que será una lista de tokens de la frase inicial
    #la lista irradiated son las palabras de la frase lemmatizadas ya.
    #la lista topics son los lemmas de los SUSTANTIVOS y VERBOS de la frase
    #la lista sin_lemma son los tokens que no están registrados ni tienen lemma
	try:
		tokens = word_tokenize(to_tokenize.content,"spanish")
	except:
		tokens = word_tokenize(to_tokenize,"spanish")

	tokens_limpios=[]
	for token in tokens:
		token=token.lower() 
		if token not in palabras_funcionales:
			if 'jaja' not in token:
				for i in ['¿','-','#']:
					try:
						token=token.strip(i)
					except:
						pass
				tokens_limpios.append(token)

	irradiated, topics, sin_lemma, toklemma = [],[],[],[]

	for token in tokens_limpios:
		lemma = lemma_ray[lemma_ray['Form']==token].lemma.values
		try:
			irradiated.append(lemma[0])
			toklemma.append(lemma[0])
		except:
			sin_lemma.append(token)
		if (token in sustantivos) or (token in verbos) or (token in adjetivos):
			topics.append(lemma[0].lower())

	#añadiendo lectura del diccionario a los tokens no lematizados
	sin_lemma_def=[]
	# print(sin_lemma,"sinlema",len(sin_lemma))
	# print(irradiated,"irradiated",len(irradiated))
	# print(topics,"topics",len(topics))
	
	# Busca tokens que no logra lematizar:
	# Las que encuentra las guarda en a_pickelizar.txt junto a su lemma
	# Las que no encuentra las guarda en a_lemmatizar.txt
	if True==True:
		a_picklelizar=[]
		for tok in sin_lemma:
			try:
				# print(tok,"TOK")
				lema,tipo =lemmascrapper(tok)
				irradiated.append(lema)
				if tipo == "s" or tipo == "v":
					topics.append(lema)
				toklemma.append(lema.lower())
				a_picklelizar.append((tok.lower(),lema.lower()))
			except:
				sin_lemma_def.append(tok.lower())
				toklemma.append(tok)
		with open(f"cogs/datos/a_pickelizar.txt","a") as fh:
			for ele,mento in a_picklelizar:
				try:
					fh.write(str(ele)+","+str(mento)+";")
				except UnicodeEncodeError:
					print(str(ele), str(mento))
	# print(sin_lemma_def,"sin_lemma_def",len(sin_lemma_def))
	if len(sin_lemma_def)>0:
		with open(f"cogs/datos/a_lemmatizar.txt","a") as fh:
			for elemento in sin_lemma_def:
				try:
					fh.write(";"+str(elemento))
				except UnicodeEncodeError:
					pass
					
	# Agrega las palabras no encontradas a topics
	topics.extend(sin_lemma_def)

	print(toklemma)

	return irradiated, topics, toklemma


def guardadoinputs(message,tokens_limpios):
	sep=";--;"
	with open(f"cogs/datos/inputs_espia.csv","a") as fh:
		fh.write("\n"+str(datetime.now())+sep+str(message.channel)+sep+str(message.author)+sep+"'"+str(message.clean_content)+"'"+sep+str(tokens_limpios)+sep+str(message.mentions))

def creacionpool(tokens_limpios,percentil):
	#TO - DO: LEMMATIZAR TODAS LAS FRASES DE ALFOBOT
	pool = pd.DataFrame()
	for token_usuario in tokens_limpios:
		if token_usuario in tokens_alfonso:
			frindices = df_frasest[df_frasest[token_usuario]>=1].index.values
			for i in frindices:
				if i in pool.index.values:
					pool.at[i,'num'] = pool.at[i,'num']+1
				else:
					pool.at[i,'num']=1	
	# Aplicamos percentil
	pool['num']=pd.to_numeric(pool['num'])		
	corte = np.percentile(pool['num'].values, percentil)
	# df con índice de la frase y num de tokens coincidentes
	pool = pool[pool['num']>=corte]
	pool['frases']=pool.index

	# Añadimos datos de puntuaciones:
	df_puntuacion=pd.io.json.read_json(f'cogs/datos/puntuacion.json')
	pool = df_puntuacion.merge(pool,how='right',on='frases')
	print(pool)
	# Columnas de pool: frases, num_reacciones, num_risas, num, num_usada
	return pool

def seleccionrespuesta(pool):
	# Suma de las 3 variables. Ponderadas con pond?
	pond=1

	pool['num']=pd.to_numeric(pool['num'])
	pool['num_reacciones']=pd.to_numeric(pool['num_reacciones'])
	pool['num_risas']=pd.to_numeric(pool['num_risas'])
	#pool['num_usada']=pd.to_numeric(pool['num_usada'])

	pool['suma']=pool['num']+pond*pool['num_reacciones']+pond*pool['num_risas']#-pond*pool['num_usada']

	# Random con pesos. Suavizador a modificar para balancear pesos si fuese necesario
	suavizador = 0
	ind = random.choices(population = pool['frases'].values, weights = [x+suavizador for x in pool['suma'].values], k=1)[0]
	print(ind)
	print(df_frasest.at[ind,'frase'])

	# Apunta en puntuacion.json que la frase ha sido usada
	
	df_puntuacion=pd.io.json.read_json(f'cogs/datos/puntuacion.json')
	if ind in df_puntuacion['frases'].values:
		index_punt = df_puntuacion[df_puntuacion['frases']==ind].index.values[0]
		df_puntuacion.at[index_punt,'num_usada']+=1
	else:
		# df_puntuacion.at[len(df_puntuacion),'frases']=ind
		# df_puntuacion.at[len(df_puntuacion),'num_usada']=1
		u_linea=len(df_puntuacion)
		linea_ceros=[0 for x in range(len(df_puntuacion.columns))]
		linea_ceros[0]=ind
		df_puntuacion.loc[u_linea]=linea_ceros
		df_puntuacion['num_usada'].iat[u_linea]=1
	df_puntuacion.fillna(0, inplace=True)
	df_puntuacion.to_json(f"cogs/datos/puntuacion.json")


	return df_frasest.at[ind,'frase']

def actualizarpickles():
	'''
	Toma las palabras que encontró y puso en a_pickelizar.txt y las introduce en la base de datos en pickle
	'''
	pick=pd.read_pickle(f'cogs/datos/rayo_lemmatizador')
	with open(f'cogs/datos/a_pickelizar.txt') as apc:
		apk=apc.read()
	l_apk=apk.split(";")
	for tup in l_apk[:-1]:
		l_tup=tup.split(",")
		if l_tup[0] not in pick["Form"].values:
			pick=pick.append({'Form':l_tup[0],"lemma":l_tup[1]},ignore_index=True)
		else:
			print(l_tup[0],"está en la base")
	pick.to_pickle(f'cogs/datos/rayo_lemmatizador')
	remove(f'cogs/datos/a_pickelizar.txt')

def risaReaccion():
	reacciones=["Vaya CRACK soy, no?","Es o no es","De qué te ríes","Lo leí en mi twitter jaja", "Pues Adrianbot es más gracioso aún"]
	return random.choice(reacciones)