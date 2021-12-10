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
#Ingreso de datos



def lemmatizer(to_tokenize):
	#Abre el lemma en vinagre; es un dataset.
	with open('rayo_lemmatizador' , 'rb') as f:
		lemma_ray = pickle.load(f)

	#también sacamos de conserva el dataset de las palabras
	#contiene 14 atributos de cada palabra + el target (POS)
	with open('X_train' , 'rb') as f:
		superinfo = pickle.load(f)

	sustantivos = superinfo[superinfo['POS']=='NOUN'].Palabra.value_counts().index
	verbos = superinfo[superinfo['POS']=='VERB'].Palabra.value_counts().index



    #Creamos variable que será una lista de tokens de la frase inicial
    #la lista irradiated son las palabras de la frase lemmatizadas ya.
    #la lista topics son los lemmas de los SUSTANTIVOS y VERBOS de la frase
    #la lista sin_lemma son los tokens que no están registrados ni tienen lemma

	sentence = word_tokenize(to_tokenize.content)
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
	if len(sin_lemma)>0:
		with open(f"cogs/datos/a_lemmatizar.txt","a") as fh:
			for elemento in sin_lemma:
				fh.write(";"+elemento)

	return irradiated, topics


def guardadoinputs(message,tokens_limpios):
	df_usuarios=pd.read_csv(f'cogs/datos/pedidos.csv',delimiter=";")
	sep=";.;..;.;;"
	df_usuarios.loc[len(df_usuarios)]=[message.author,tokens_limpios,datetime.now()]
	df_usuarios.to_csv(f"cogs/datos/pedidos.csv",
		sep=";",
		index=False,
		encoding='utf-8-sig')
	with open(f"cogs/datos/inputs.csv","a") as fh:
		fh.write("\n"+str(datetime.now())+sep+str(message.author)+sep+"'"+str(message.content)+"'"+sep+str(tokens_limpios))
def seleccionrespuesta(pool):

	# r1=random.randint(0,len(pool)-1)
	# print(2,r1)
	# frase_pool=pool[r1]
	# print(3,frase_pool)
	# r2=random.randint(0,len(frase_pool)-1)
	# print(4,r2)
	# print(5,str(frase_pool.iloc[r2][0]))
	# return str(frase_pool.iloc[r2][0])
	return random.sample(pool,1)[0]

def creacionpool(tokens_limpios,percentil):
	df=pd.io.json.read_json(f'cogs/datos/frasest.json')
	#TO - DO: LEMMATIZAR TODAS LAS FRASES DE ALFOBOT
	tokens_alfonso=df.columns.drop(['frase','tokenizado'])
	d1 = dict()
	for token_usuario in tokens_limpios:
		if token_usuario in tokens_alfonso:
			frindices = df[df[token_usuario]==1].index.values
			for i in frindices:
				if i in d1.keys():
					d1.update({i:d1[i]+1})
				else:
					d1.update({i:1})			
	d1 = np.array(list(d1.items()))
	corte = np.percentile(d1[:,1], percentil)
	pool=[]
	for c in d1:
		if c[1] >=corte:
			pool.append(df.loc[c[0],'frase'])
	return pool
