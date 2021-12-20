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
		if (message.author != self.client.user):
			if "random" in message.content.lower():
				modelo="RF"
			elif "knn" in message.content.lower():
				modelo="RF"
			else:
				await message.channel.send("Si quisiste decir un modelo no se entendió, o no es optimizable. Cuando tengas algo decente avísame.")
				with open(f'funciones/cogactivo.txt',"w") as ca:
					ca.write("False")
				self.client.unload_extension(f'cogs.cogOptimo')
			await message.channel.send("Pasé información")


def setup(client):
	client.add_cog(CogOptimo(client))
