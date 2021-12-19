#Modelo Decisión de Request
import pickle

with open(f'datos/modelo_request','rb') as files:
	global NB
	NB = pickle.load(files)

def decision_request(frase):
	global NB
	return NB.predict([frase])[0]