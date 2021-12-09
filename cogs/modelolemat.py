#modelolematizador - PRE-ADRI
import discord 
from discord.ext import commands
from tokenizador_frases import tokenizar
import keep_alive
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
df=pd.io.json.read_json(f'cogs/datos/frasest.json')
tokens_frases=df.columns.drop(['frase','tokenizado'])
df_usuarios=pd.read_csv(f'cogs/datos/pedidos.csv',delimiter=";")

def tokenizar(message):
	tokens=nltk.word_tokenize(message.content,"spanish")
	tokens_limpios=[] 
	tokens = [token.lower() for token in tokens]
	for token in tokens: 
		if token not in palabras_funcionales:
			tokens_limpios.append(token)
		print(tokens_limpios)
		return tokens_limpios