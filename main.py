import discord 
from discord.ext import commands
import tokenizador_frases as tkf
import keep_alive
from datetime import datetime
import random
import pandas as pd
import nltk
import re
import math

global modoprofe
global modoparty
modoprofe=False
modoparty=False

#Set del BOT
client = commands.Bot(command_prefix = 'Alfobot ', description = "Simplificando DATOS dejé atrás mi forma corpórea")

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name = "simplificar DATOS dejé atrás mi forma corpórea"))
    print('My bot is ready')



#Comando de encendido
@client.command()
async def despierta(ctx):
    global modoprofe
    global modoparty
    if modoprofe == False:
        client.load_extension(f'cogs.modoprofe')
        #client.add_cog(Profemode(client))
        modoprofe=True
        await ctx.send('Chicos, vamos serios. Hablad.')
        try:
          client.unload_extension(f'cogs.modoparty')
          #client.remove_cog('Partymode')
          modoparty=False
        except:
          pass
    else:
        await ctx.send(str(client.user) + 'Os estoy esperando en Zoom, HABLAD!')

# Modo profe
@client.command()
async def profe(ctx):
    global modoprofe
    global modoparty
    if modoprofe == False:
        client.load_extension(f'cogs.modoprofe')
        #client.add_cog(Profemode(client))
        modoprofe=True
        await ctx.send('Chicos, vamos serios. Hablad')
        try:
          client.unload_extension(f'cogs.modoparty')
          #client.remove_cog('Partymode')
          modoparty=False
        except:
          pass
    else:
        await ctx.send(str(client.user) + 'Os estoy esperando en Zoom. HABLAD!')

# Modo party
@client.command()
async def party(ctx):
    global modoparty
    global modoprofe
    if modoparty==False:
        client.load_extension(f'cogs.modoparty')
        #client.add_cog(Partymode(client))
        modoparty=True
        await ctx.send('Chicos estoy aquí, hablen')
        try:
          #client.remove_cog('Profemode')
          client.unload_extension(f'cogs.modoprofe')
          modoprofe=False
        except:
          pass
    else:
        await ctx.send('Soy omnipresente')

# Comando dormir
@client.command()
async def duerme(ctx):
    global modoparty
    global modoprofe
    if modoprofe == True:
        client.unload_extension(f'cogs.modoprofe')
        #client.remove_cog('Profemode')
        modoprofe=False
        await ctx.send('Chao chicos, nos vemos mañana')
    elif modoparty == True:
        client.unload_extension(f'cogs.modoparty')
        #client.remove_cog('Partymode')
        modoparty=False
        # await ctx.send('¿Quién dijo que me voy a dormir?')
        await ctx.send('Oh no, se me acabó el café')
    else: # modoprofe == False and modoparty == False:
        # await ctx.send('Si me necesitan, me pueden despertar')
        await ctx.send('ZzZzZzZzZzZ...')

# Refrescar frases party:
@client.command()
async def tokeniza(ctx, arg):
    print(arg)
    await ctx.send(tkf.tokenizador_frase_unica(arg))


keep_alive.keep_alive()

client.run('OTEzMTkxMTk4MTE2Njg3OTIy.YZ65kw.id9oVV8sMjXLkuEpR1FlC6-NNZA')
