#modelo_de_puntuacion_de_frases
import pandas as pd


def apertura():
	df_frases=pd.io.json.read_json('frasest.json')
	df_recepcion=pd.io.json.read_json("recep.json")
	df_puntuacion=pd.io.json.read_json("puntuacion.json")
	return df_frases,df_recepcion,df_puntuacion

def recopilacion(df_frases,df_recepcion,df_puntuacion):
	for f in range(len(df_recepcion)):
		num_frase=df_recepcion["Frases"].iloc[f]
		numero_reacciones= df_recepcion.iloc[f].sum()
		if num_frase in df_puntuacion['frases'].values:
			index_punt = df_puntuacion[df_puntuacion['frases']==num_frase].index.values[0]
			df_puntuacion['num_reacciones'].iat[index_punt]=numero_reacciones
		else:
			u_linea=len(df_puntuacion)
			linea_ceros=[0 for x in range(len(df_puntuacion.columns))]
			linea_ceros[0]=num_frase
			df_puntuacion.at[u_linea]=linea_ceros
			df_puntuacion['num_reacciones'].iat[index_punt]=numero_reacciones
	df_puntuacion.to_json("puntuacion.json")

def guardarreacciones(usuario, mensaje,emoji):
	df_frases=pd.io.json.read_json('frasest.json')
	df_recepcion=pd.io.json.read_json("recep.json")
	if usuario == mensaje.author:
		num_frase=df[df["frase"]==mensaje.content].index.values[0]
		if num_frase in df_recepcion['Frases'].values:
			print(df_recepcion[df_recepcion["Frases"]==num_frase].index.values)
			linea=df_recepcion[df_recepcion["Frases"]==num_frase].index.values
			conjunto=df_recepcion.columns
			if emoji.name in conjunto:
				df_recepcion[emoji.name].iat[linea[0]]+=1
				print("encontrado")
			else:
				print("no encontrado")
				df_recepcion[emoji.name]=0
				df_recepcion[emoji.name].iat[linea[0]]=1
		else:
			u_linea=len(df_recepcion)
			linea_ceros=[0 for x in range(len(df_recepcion.columns))]
			linea_ceros[0]=num_frase
			df_recepcion.at[u_linea]=linea_ceros
			conjunto=set(df_recepcion.columns)
			if emoji.name in conjunto:
				df_recepcion[emoji.name].iat[u_linea]+=1
				print("encontrado-primeravez")
			else:
				print("no encontradoprimeravez")
				#conjunto.add(emoji)
				df_recepcion[emoji.name]=0
				df_recepcion[emoji.name].iat[u_linea]=1
		df_recepcion.to_csv("recep.csv",index=False, sep=";")
		df_recepcion.to_json("recep.json")

#x,y,z=apertura()
#recopilacion(x,y,z)
