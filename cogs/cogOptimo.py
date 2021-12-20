#CogOptimizador
import discord 
from discord.ext import commands

with open(f'funciones/cogactivo.txt',"w") as ca:
    ca.write("True")
m=0
class CogOptimo(commands.Cog):
	def __init__(self, client):
		self.client = client
		self._last_member = None
		
	@commands.Cog.listener()
	async def on_message(self, message):
		if (message.author != self.client.user):
			if m=0:
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
			elif m=1:
				print("DEBERIA HABER UN ATTACHMENT")
				print(message)
				pass


def setup(client):
	client.add_cog(CogOptimo(client))
