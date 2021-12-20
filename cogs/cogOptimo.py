#CogOptimizador
import discord 
from discord.ext import commands

with open(f'funciones/cogactivo.txt',"w") as ca:
    ca.write("True")

class CogOptimo(commands.Cog):
	def __init__(self, client):
		self.client = client
		self._last_member = None
	#def preguntasIniciales(message):
		#print("hi*********************************************************************************************************",message)
		
	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author != self.client.user:
			await message.channel.send("Pasé información")
			
	# @commands.command()
	# async def fin():
	# 	await self.client.load(f'cog.cogBert')


def setup(client):
	client.add_cog(CogOptimo(client))
	#client.unload_extension(f'cog.cogBert')