import discord 
from discord.ext import commands

global cliente
cliente=""

def iniciar(): 
	client = commands.Bot(command_prefix='Alfobot ', description="PARTYMODE")
	return client
def correr(client):
	client.run('OTEzMTkxMTk4MTE2Njg3OTIy.YZ65kw.id9oVV8sMjXLkuEpR1FlC6-NNZA')
	global cliente
	cliente=client
	return client
def retorno():
	global cliente
	return cliente