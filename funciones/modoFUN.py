#funciones-party
import discord 
from discord.ext import commands
import pickle
import pandas as pd
import numpy as np
import random
from funciones import modelolemat

global df_frasest
global tokens_alfonso

df_frasest=pd.io.json.read_json(f'datos/frasest.json')
tokens_alfonso=df_frasest.columns.drop(['frase','tokenizado'])

def funresponse(message,self):
	if message.author != self.client.user:
		tokens_limpios = modelolemat.megatizer(message)[1]
		#try:
		pool = creacionpool(tokens_limpios, 1)
		if len(pool)>0:
			#print(pool)
			respuesta = seleccionrespuesta(pool)
			print(respuesta)
			return respuesta

def creacionpool(tokens_limpios,percentil):
	pool = pd.DataFrame()
	for token_usuario in tokens_limpios:
		if token_usuario in tokens_alfonso:
			frindices = df_frasest[df_frasest[token_usuario]>=1].index.values
			for i in frindices:
				if i in pool.index.values:
					pool.at[i,'num'] = pool.at[i,'num']+1
				else:
					pool.at[i,'num']=1	
	if len(pool)>0:
		# Aplicamos percentil
		pool['num']=pd.to_numeric(pool['num'])		
		corte = np.percentile(pool['num'].values, percentil)
		# df con índice de la frase y num de tokens coincidentes
		pool = pool[pool['num']>=corte]
		pool['frases']=pool.index

		# Añadimos datos de puntuaciones:
		df_puntuacion=pd.io.json.read_json(f'datos/puntuacion.json')
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
	
	df_puntuacion=pd.io.json.read_json(f'datos/puntuacion.json')
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
	df_puntuacion.to_json(f"datos/puntuacion.json")


	return df_frasest.at[ind,'frase']

def risaReaccion():
	reacciones=["Vaya CRACK soy, no?","Es o no es","De qué te ríes","Lo leí en mi twitter jaja", "Pues Adrianbot es más gracioso aún"]
	return random.choice(reacciones)