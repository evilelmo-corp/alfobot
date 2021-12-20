#CogOptimizador
import discord 
from discord.ext import commands
import requests
import pandas as pd

with open(f'funciones/cogactivo.txt',"w") as ca:
    ca.write("True")

global m
m=0

class CogOptimo(commands.Cog):
	def __init__(self, client):
		self.client = client
		self._last_member = None
		
	@commands.Cog.listener()
	async def on_message(self, message):
		if (message.author != self.client.user):
			global m
			if m==0:
				if ("random" not in message.content.lower()) and ("knn" not in message.content.lower()):
					await message.channel.send("Si quisiste decir un modelo no se entendió, o no es optimizable. Cuando tengas algo decente avísame.")
					with open(f'funciones/cogactivo.txt',"w") as ca:
						ca.write("False")
					self.client.unload_extension(f'cogs.cogOptimo')
				elif "random" in message.content.lower():
					modelo="RF"
					m=1
				elif "knn" in message.content.lower():
					modelo="RF"
					m=1
				await message.channel.send("Ahora necesito que me pases el data set en *.csv LIMPIO")
			elif m==1:
				print("DEBERIA HABER UN ATTACHMENT")
				print(message.attachments)
				print(message.attachments[0])
				url=message.attachments[0]
				r = requests.get(url, allow_redirects=True)
				with open(f'datos/arc.csv', 'wb') as arc:
					arc.write(r.content)
				df=pd.read_csv('datos/arc.csv')
				await message.channel.send("Indicame cuál de la siguientes es la columna clase: (Señala el índice de la columna)")
				columnas=list(df.columns)
				await message.channel.send(columnas)

				y=df[columnas[int(message.content)]]
				X=df.drop([columnas[int(message.content)]],axis=1)

				pass


def setup(client):
	client.add_cog(CogOptimo(client))
