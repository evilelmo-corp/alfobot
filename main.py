import discord 
from discord.ext import commands 
from datetime import datetime
import random
import pandas as pd
import nltk
from tokenizador_frases import tokenizar
import re
import keep_alive
import math
import cliente 

global modoprofe
global modoparty
modoprofe=False
modoparty=False

#Set del BOT
client = cliente.iniciar()
#client = commands.Bot(command_prefix='Alfobot ', description="simplificando DATOS dejé atrás mi forma corpórea")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="simplificando DATOS dejé atrás mi forma corpórea"))
    print('My bot is ready')

#Comandos de encendido y apagado de modos
@client.command()
async def despierta(ctx):
    global modoprofe
    global modoparty
    if modoprofe == False:
        client.load_extension(f'modoprofe')
        #client.add_cog(Profemode(client))
        modoprofe=True
        await ctx.send('Chicos, vamos serios. Hablad.')
        try:
          client.unload_extension(f'modoparty')
          #client.remove_cog('Partymode')
          modoparty=False
        except:
          pass
    else:
        #await ctx.send('Ya estoy aquí')
        await ctx.send('Os estoy esperando en Zoom, HABLAD!')
## Otra sintaxis para el modo profe, no sé si se puede ahorrar código de alguna forma
@client.command()
async def profe(ctx):
    global modoprofe
    global modoparty
    if modoprofe == False:
        client.load_extension(f'modoprofe')
        #client.add_cog(Profemode(client))
        modoprofe=True
        await ctx.send('Chicos, vamos serios. Hablad')
        try:
          client.unload_extension(f'modoparty')
          #client.remove_cog('Partymode')
          modoparty=False
        except:
          pass
    else:
        await ctx.send('Os estoy esperando en Zoom. HABLAD!'+str(client.user))

@client.command()
async def party(ctx):
    global modoparty
    global modoprofe
    if modoparty==False:
        client.load_extension(f'modoparty')
        #client.add_cog(Partymode(client))
        modoparty=True
        await ctx.send('Chicos estoy aquí, hablen')
        try:
          #client.remove_cog('Profemode')
          client.unload_extension(f'modoprofe')
          modoprofe=False
        except:
          pass
    else:
        await ctx.send('Soy omnipresente')
@client.command()
async def duerme(ctx):
    global modoparty
    global modoprofe
    if modoprofe == True:
        client.unload_extension(f'modoprofe')
        #client.remove_cog('Profemode')
        modoprofe=False
        await ctx.send('Chao chicos, nos vemos mañana')
    elif modoparty == True:
        client.unload_extension(f'modoparty')
        #client.remove_cog('Partymode')
        modoparty=False
        # await ctx.send('¿Quién dijo que me voy a dormir?')
        await ctx.send('Oh no, se me acabó el café')
    else: # modoprofe == False and modoparty == False:
        # await ctx.send('Si me necesitan, me pueden despertar')
        await ctx.send('ZzZzZzZzZzZ...')
# Refrescar frases party:
@client.command()
async def tokeniza(ctx):
    await tokenizar()

keep_alive.keep_alive()

cliente.correr(client)
