import discord 
from discord.ext import commands
from funciones import mantenimiento

import pandas as pd
import os
import pickle

# Alfobot Oficial token:
#token='OTEzMTkxMTk4MTE2Njg3OTIy.YZ65kw.id9oVV8sMjXLkuEpR1FlC6-NNZA'

# AlfobotZ token
token='OTE3NzQzMTI3OTI0NzIzNzYy.Ya9I5A.c48WKkw4qsM5B0-OBscAB0C6baE'


#Set del BOT
client = commands.Bot(command_prefix = 'minibot ', description = "minificar datos")

# Crea df en pickle vacío con las columnas de los cogs para que lo use funPasarelaChannel
cogs_lista = [i[:-3] for i in os.listdir('./cogs') if i.startswith('cog')]
print(cogs_lista)
df=pd.DataFrame(columns=cogs_lista)
print(df)

with open('datos/pasarela_ch','wb') as fh:
	pickle.dump(df,fh)


#COG ESPIA GUARDA LA INFORMACIÓN RELEVANTE
@client.event
async def on_ready():
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name = "minificar datos"))
    #Espía
    client.load_extension(f'cogs.cogEvilelmo')
    print('My bot is ready')

#Comando de encendido
@client.command()
async def despierta(ctx):
	with open('datos/pasarela_ch','rb') as fh:
		df=pickle.load(fh)
	df.at[str(ctx.channel),'cogBert']=1
	with open('datos/pasarela_ch','wb') as fh:
		pickle.dump(df,fh)
	try:
		client.load_extension(f'cogs.cogBert')
	except:
		pass
	await ctx.send('Chicos estoy aquí, hablen')

# Comando dormir
@client.command()
async def duerme(ctx):
	with open('datos/pasarela_ch','rb') as fh:
		df=pickle.load(fh)
	df.at[str(ctx.channel),'cogBert']=0
	with open('datos/pasarela_ch','wb') as fh:
		pickle.dump(df,fh)
	#client.unload_extension(f'cogs.cogBert')
	await ctx.send('Oh no, se me acabó el café')
	try:
		mantenimiento.actualizarpickles()
	except FileNotFoundError:
		print("No hay nada pickelizable")

#TOKEN
client.run(token)