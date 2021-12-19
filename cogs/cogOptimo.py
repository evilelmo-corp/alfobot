#CogOptimizador
import discord 
from discord.ext import commands

class CogOptimo(commands.Cog):
	def __init__(self, client):
		self.client = client
		self._last_member = None
	@commands.Cog.listener()
	async def preguntasIniciales(message):
		print("hi",message)
		await message.channel.send("Pasé información")

def setup(client):
    client.add_cog(CogOptimo(client))