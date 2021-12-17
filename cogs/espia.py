#Cog Espía
import discord 
from discord.ext import commands
from cogs import modelolemat
from cogs import mantenimiento

class Espia(commands.Cog):
	def __init__(self, client):
		self.client = client
		self._last_member = None
	@commands.Cog.listener()
	async def on_message(self, message):
		print(message.author,
			message.content,
			message.channel,
			message.clean_content,
			message.flags,
			message.mentions
			)
		tokens_limpios=modelolemat.megatizer(message)[1]
		mantenimiento.guardadoinputs(message, tokens_limpios)

def setup(client):
    client.add_cog(Espia(client))