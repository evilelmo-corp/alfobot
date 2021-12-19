import discord 
from discord.ext import commands
# from tokenizador_frases import tokenizar
# import keep_alive
# from datetime import datetime
import random
import pandas as pd
# import nltk
# import re
# import math

#client = commands.Bot(command_prefix='Alfobot ', description="PROFEMODE")
#Ingreso de datos
df_data=pd.io.json.read_json(f'cogs/datos/datacheat.json')
df_data=df_data.T
df_data=df_data.reset_index()
df_data.columns=["key","value"]



#Modo clases
class Profemode(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.client.user:
            #await message.channel.send("funciono")
            if message.content in list(df_data.key):
                await message.channel.send(str(df_data[df_data['key']==str(message.content)]["value"].values[0])+str(self.client.user))
def setup(client):
    client.add_cog(Profemode(client))