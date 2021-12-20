import discord 
from discord.ext import commands
from funciones import mantenimiento

import pandas as pd
import os
import pickle

#Set del BOT
client = commands.Bot(command_prefix = 'Alfobot ', description = "Simplificando DATOS dejé atrás mi forma corpórea")

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
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name = "simplificar DATOS dejé atrás mi forma corpórea"))
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
	client.load_extension(f'cogs.cogBert')
	await ctx.send('Chicos estoy aquí, hablen')

# Comando dormir
@client.command()
async def duerme(ctx):
	with open('datos/pasarela_ch','rb') as fh:
		df=pickle.load(fh)
	df.at[str(ctx.channel),'cogBert']=0
	with open('datos/pasarela_ch','wb') as fh:
		pickle.dump(df,fh)
	client.unload_extension(f'cogs.cogBert')
	await ctx.send('Oh no, se me acabó el café')
	try:
		mantenimiento.actualizarpickles()
	except FileNotFoundError:
		print("No hay nada pickelizable")

#TOKEN
client.run('OTEzNzA4MzA4MTE5MDMxODA5.YaCbLA.z8UODdgSP2VgIITnApqCGgkGKE8')