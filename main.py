import discord 
from discord.ext import commands
from funciones import mantenimiento

#Set del BOT
client = commands.Bot(command_prefix = 'Alfobot ', description = "Simplificando DATOS dejé atrás mi forma corpórea")

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
	client.load_extension(f'cogs.cogBert')
	await ctx.send('Chicos estoy aquí, hablen')

# Comando dormir
@client.command()
async def duerme(ctx):
	client.unload_extension(f'cogs.cogBert')
	await ctx.send('Oh no, se me acabó el café')
	try:
		mantenimiento.actualizarpickles()
	except FileNotFoundError:
		print("No hay nada pickelizable")

#TOKEN
client.run('OTEzNzA4MzA4MTE5MDMxODA5.YaCbLA.z8UODdgSP2VgIITnApqCGgkGKE8')