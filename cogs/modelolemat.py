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



# Variables declaradas globales por agilizar funciones. ¿Alguna sería mejor que siguiese estando 
# dentro de su respectiva función?

# Variables para lemmatizer:

global lemma_ray
global superinfo
global sustantivos
global verbos

#Abre el lemma en vinagre; es un dataset.
with open(f'cogs/datos/rayo_lemmatizador' , 'rb') as f:
	lemma_ray = pickle.load(f)

#también sacamos de conserva el dataset de las palabras
#contiene 14 atributos de cada palabra + el target (POS)
with open(f'cogs/datos/X_train' , 'rb') as f:
	superinfo = pickle.load(f)

sustantivos = superinfo[superinfo['POS']=='NOUN'].Palabra.value_counts().index
verbos = superinfo[superinfo['POS']=='VERB'].Palabra.value_counts().index

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
	print(resultado.h1.text,"RESULTADO SCRAP")
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

	sentence = word_tokenize(to_tokenize.content)

	# "jajaja" estaba entrando. Forma temporal de quitarnoslo
	for i in sentence:
		if 'jaja' in i:
			sentence.remove(i)

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
	#Si la cantidad de tokens no lematizados es superior a la cantidad de tokens leídos busca en el diccionario.
	#Para evitar que busque innecesariamente, se lo puede modificar sin problema
	if len(sin_lemma)>len(irradiated):
		a_picklelizar=[]
		for tok in sin_lemma:
			try:
				print(tok,"TOK")
				lema,tipo =lemmascrapper(tok)
				irradiated.append(lema)
				if tipo == "s" or tipo == "v":
					topics.append(lema)
				a_picklelizar.append((tok,lema))
			except:
				sin_lemma_def.append(tok)
		with open(f"cogs/datos/a_pickelizar.txt","a") as fh:
			for ele,mento in a_picklelizar:
				fh.write(str(ele)+","+str(mento)+";")
	print(sin_lemma_def,"sin_lemma_def",len(sin_lemma_def))
	if len(sin_lemma_def)>0:
		with open(f"cogs/datos/a_lemmatizar.txt","a") as fh:
			for elemento in sin_lemma_def:
				fh.write(";"+str(elemento))
	#agregar los sin lemma definitivos a topics permite captar los nombres propios.
	topics.extend(sin_lemma_def)
	irradiated.extend(sin_lemma_def)
	return irradiated, topics


def guardadoinputs(message,tokens_limpios):
	sep=";--;"
	with open(f"cogs/datos/inputs_espia.csv","a",encoding="utf-8") as fh:
		fh.write("\n"+str(datetime.now())+
			sep+str(message.channel)+
			sep+str(message.author)+
			sep+"'"+str(message.clean_content)+"'"+
			sep+str(tokens_limpios)+
			sep+str(message.mentions)
			)

def seleccionrespuesta(pool):
	# Suma de las 3 variables. Ponderadas con pond?
	pond=1

	pool['num']=pd.to_numeric(pool['num'])
	pool['num_reacciones']=pd.to_numeric(pool['num_reacciones'])
	pool['num_risas']=pd.to_numeric(pool['num_risas'])

	pool['suma']=pool['num']+pond*pool['num_reacciones']+pond*pool['num_risas']

	# Random con pesos. Suavizador a modificar para balancear pesos si fuese necesario
	suavizador = 0
	ind = random.choices(population = pool['frases'].values, weights = [x+suavizador for x in pool['suma'].values],k=1)[0]
	print(ind)
	print(df_frasest.at[ind,'frase'])
	return df_frasest.at[ind,'frase']


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
	# Columnas de pool: frases, num_reacciones, num_risas, num
	return pool

def actualizarpickles():
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