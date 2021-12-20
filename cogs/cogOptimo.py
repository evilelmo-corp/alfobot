#CogOptimizador
import discord 
from discord.ext import commands

with open(f'funciones/cogactivo.txt',"w") as ca:
    ca.write("True")

class CogOptimo(commands.Cog):
	def __init__(self, client):
		self.client = client
		self._last_member = None
		
	@commands.Cog.listener()
	async def on_message(self, message):
		with open('datos/pasarela_ch','rb') as fh:
			df=pickle.load(fh)
		m=0
		if (message.author != self.client.user) and (df.at[str(message.channel),'cogOptimo']==1):
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
				print(message)
				pass
		df.at[str(message.channel),'cogOptimo']=0
		df.at[str(message.channel),'cogBert']=1
		with open('datos/pasarela_ch','wb') as fh:
			pickle.dump(df,fh)


def setup(client):
	client.add_cog(CogOptimo(client))
