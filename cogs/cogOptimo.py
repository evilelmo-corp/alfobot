#CogOptimizador
import discord 
from discord.ext import commands
import pickle
from sklearn.model_selection import train_test_split
import requests
import pandas as pd
import re

global m
m=0

# with open(f'funciones/cogactivo.txt',"w") as ca:
#     ca.write("True")

class CogOptimo(commands.Cog):
	def __init__(self, client):
		self.client = client
		self._last_member = None
		
	@commands.Cog.listener()
	async def on_message(self, message):
		global m
		with open('datos/pasarela_ch','rb') as fh:
			df=pickle.load(fh)
		# print(df)
		# print(df.at[str(message.channel),'cogOptimo']==1)
		# print(m)
		if (message.author != self.client.user) and (df.at[str(message.channel),'cogOptimo']==1):
			if m==0:
				if ("random" not in message.content.lower()) and ("knn" not in message.content.lower()):
					await message.channel.send("Si quisiste decir un modelo no se entendió, o no es optimizable. Cuando tengas algo decente avísame.")
					with open(f'funciones/cogactivo.txt',"w") as ca:
						ca.write("False")
					df.at[str(message.channel),'cogOptimo']=0
					df.at[str(message.channel),'cogBert']=1
					with open('datos/pasarela_ch','wb') as fh:
						pickle.dump(df,fh)
					self.client.unload_extension(f'cogs.cogOptimo')
				elif "random" in message.content.lower():
					modelo="RF"
					m=1
					await message.channel.send("Ahora necesito que me pases el data set en *.csv LIMPIO")
				elif "knn" in message.content.lower():
					modelo="RF"
					m=1
					await message.channel.send("Ahora necesito que me pases el data set en *.csv LIMPIO")
			elif m==1:
				# print("DEBERIA HABER UN ATTACHMENT")
				# print(message.attachments)
				# print(message.attachments[0])
				url=message.attachments[0]
				r = requests.get(url, allow_redirects=True)
				with open(f'datos/arc.csv', 'wb') as arc:
					arc.write(r.content)
				df_trabajo=pd.read_csv('datos/arc.csv')
				await message.channel.send("Indicame cuál de la siguientes es la columna clase: (Señala el índice de la columna)")
				columnas=list(df_trabajo.columns)
				await message.channel.send(columnas)
				m=2
			elif m==2:
				columna_y = False
				if bool(re.search(r'[0-9]',message.content)):
					columna_y=int(message.content)
				else:
					await message.channel.send("Creo que no me entendieron.")
					m=1
				if columna_y != False:
					await message.channel.send("Soy bueno, pero tampoco una máquina. Esto puede tardar un ratillo")
					try:
						# print('risa detectada')
						df_trabajo=pd.read_csv('datos/arc.csv')
						columnas=list(df_trabajo.columns)
						y=df_trabajo[columnas[int(message.content)]]
						X=df_trabajo.drop([columnas[int(message.content)]],axis=1)
						X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,stratify=y)
						from sklearn.ensemble import RandomForestClassifier
						from sklearn.model_selection import GridSearchCV
						from sklearn.metrics import accuracy_score
						from sklearn.metrics import f1_score, make_scorer,recall_score
						params={'n_estimators': [100,200,300],
							'criterion':['gini','entropy'],
							#'max_depth': [3,4,5],# Maxima pofundidad del arbol
							#'max_features': [2, 3], # numero de features a considerar en cada split
							'max_leaf_nodes': [8], # maximo de nodos del arbol
							#'min_impurity_decrease' : [0.02,0.3], # un nuevo nodo se hará si al hacerse se decrece la impurity en un threshold por encima del valor
							'min_samples_split': [2,5] # The minimum number of samples required to split an internal node
							}
						scorers = {"f1_macro","accuracy","recall_macro"}
						clf = RandomForestClassifier()
						grid_solver = GridSearchCV(estimator = clf, 
							param_grid = params, 
							scoring=scorers,
							cv = 5,
							refit="accuracy",
							n_jobs=-1)
						
						model_result = grid_solver.fit(X_train,y_train)

						# print(model_result.cv_results_["mean_test_recall_macro"].mean())
						# print(model_result.cv_results_["mean_test_f1_macro"].mean())
						# print(model_result.cv_results_["mean_test_accuracy"].mean())
						# print(model_result.best_score_)
						# print(model_result.best_params_)
						await message.channel.send("tus mejores resultados son:")
						await message.channel.send(model_result.best_params_)
					except:
						await message.channel.send("Me pasaste un csv mal, recuerda que solo tolero data sets numéricos. \n Cuando lo tengas volvemos a hablar.")
						m=0
				else:
					await message.channel.send("Buen chicos si no hablan, yo magia no puedo hacer")
					m=0
				df.at[str(message.channel),'cogOptimo']=0
				df.at[str(message.channel),'cogBert']=1
				with open('datos/pasarela_ch','wb') as fh:
					pickle.dump(df,fh)
				with open(f'funciones/cogactivo.txt',"w") as ca:
						ca.write("False")
				# print(df)


def setup(client):
	client.add_cog(CogOptimo(client))
