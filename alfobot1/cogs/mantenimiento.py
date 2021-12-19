import pickle
import pandas as pd
import numpy as np
from datetime import datetime



def guardadoinputs(message,tokens_limpios):
	sep=";--;"
	with open(f"cogs/datos/inputs_espia.csv","a") as fh:
		fh.write("\n"+str(datetime.now())+sep+str(message.channel)+sep+str(message.author)+sep+"'"+str(message.clean_content)+"'"+sep+str(tokens_limpios)+sep+str(message.mentions))


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
