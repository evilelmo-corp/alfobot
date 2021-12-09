#modelolematizador - PRE-ADRI
import discord 
from discord.ext import commands
from datetime import datetime
import random
import pandas as pd
import nltk
import re
import math
#Ingreso de datos

nltk.download('punkt')
nltk.download('spanish_grammars')
nltk.download('vader_lexicon')
nltk.download('stopwords')
palabras_funcionales=nltk.corpus.stopwords.words("spanish")
palabras_funcionales.extend([".", ",", ":", ";", "!", "?","'","jaja","jaj","jajaj","ja","jajaja","jajajajaj","jajaja" ])
# df=pd.io.json.read_json(f'cogs/datos/frasest.json')
# tokens_frases=df.columns.drop(['frase','tokenizado'])
#df_usuarios=pd.read_csv(f'cogs/datos/pedidos.csv',delimiter=";")

def tokenizar(message):
	tokens=nltk.word_tokenize(message.content,"spanish")
	tokens_limpios=[] 
	tokens = [token.lower() for token in tokens]
	for token in tokens: 
		if token not in palabras_funcionales:
			tokens_limpios.append(token)
	print(tokens_limpios)
	return tokens_limpios
def guardadoinputs(message,tokens_limpios):
	df_usuarios=pd.read_csv(f'cogs/datos/pedidos.csv',delimiter=";")
	sep=";.;..;.;;"
	df_usuarios.loc[len(df_usuarios)]=[message.author,tokens_limpios,datetime.now()]
	df_usuarios.to_csv(f"cogs/datos/pedidos.csv",sep=";",index=False,encoding='utf-8-sig')
	with open(f"cogs/datos/inputs.csv","a") as fh:
		fh.write("\n"+str(datetime.now())+sep+str(message.author)+sep+"'"+str(message.content)+"'"+sep+str(tokens_limpios))
def seleccionrespuesta(frase_pool_pool):
	r1=random.randint(0,len(frase_pool_pool)-1)
	frase_pool=frase_pool_pool[r1]
	r2=random.randint(0,len(frase_pool)-1)
	return str(frase_pool.iloc[r2][0])

def creacionpool(tokens_limpios):
	df=pd.io.json.read_json(f'cogs/datos/frasest.json')
	tokens_frases=df.columns.drop(['frase','tokenizado'])
	frase_pool_pool=[]
	for tok_mes in tokens_limpios:
		le=math.ceil(len(tok_mes)*(2/3))
		for tok_fra in tokens_frases:
			if tok_fra.startswith(tok_mes[:le]):
				frase_pool_pool.append(df[df[tok_fra]>0])
	return frase_pool_pool