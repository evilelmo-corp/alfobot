#Cog Espía
import discord 
from discord.ext import commands
from funciones import modeloMegat
from funciones import mantenimiento
from funciones import modeloPuntuacion
import re
import aiohttp
import json
import random

class Espia(commands.Cog):
	def __init__(self, client):
		self.client = client
		self._last_member = None

	@commands.Cog.listener()
	async def on_message(self, message):
		# print(message.author,
		# 	message.content,
		# 	message.channel,
		# 	message.clean_content,
		# 	message.flags,
		# 	message.mentions
		# 	)
		tokens_limpios=modeloMegat.megatizer(message)[0]
		mantenimiento.guardadoinputs(message, tokens_limpios)

		if (message.author == self.client.user) and (message.content not in ["0","1","2","3"]):

			print("mensaje de ALFO",message)
			def checkRisa(m):
				return bool(re.search(r'jaj',m.content))
			risa = False
			try:
				risa = await self.client.wait_for('message', timeout = 60.0, check = checkRisa) # Comprueba si se rien en los 5s siguientes
				# print("risaencontrada")
			except:
				# print(risa)
				pass
			if risa != False:
				try:
					modeloPuntuacion.guardarjaja(message.content)
					await message.channel.send(modoFUN.risaReaccion())
				except:
					pass
				
				# print('risa detectada')

				# Envía gif:
				embed = discord.Embed(colour=discord.Colour.blue())
				session = aiohttp.ClientSession()

				# Gif sobre temática 'search':
				search=random.choice(tokens_limpios)
				apiGiphy='jL3uqKUkUBo2yiw9zOOimLlx8VDI3IiT'
				response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key='+apiGiphy+'&limit=10')
				data = json.loads(await response.text())
				gif_choice = random.randint(0, 9)
				embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])
				await session.close()

				await message.channel.send(embed=embed)

	# Guarda reacciones		
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		channel = await self.client.fetch_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		user = await self.client.fetch_user(payload.user_id)
		emoji = payload.emoji
		modeloPuntuacion.guardarreacciones(self.client.user, message,emoji)

def setup(client):
    client.add_cog(Espia(client))