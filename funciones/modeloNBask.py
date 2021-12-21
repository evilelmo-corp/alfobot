#Modelo Decisión de Request
import pickle

with open(f'datos/modelo_ask','rb') as files:
	global NBa
	NBa = pickle.load(files)

def decision_ask(frase):
	global NBa
	return NBa.predict([frase])[0]
