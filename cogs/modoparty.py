import discord 
from discord.ext import commands
from tokenizador_frases import tokenizar
import keep_alive
from datetime import datetime
import random
import pandas as pd
import nltk
import re
import math
import json
import aiohttp

from cogs import modelolemat
from cogs import modelopuntuacion

apiGiphy='jL3uqKUkUBo2yiw9zOOimLlx8VDI3IiT'

commands_lista=[
    'Alfobot despierta',
    'Alfobot duerme',
    'Alfobot profe',
    'Alfobot party',
    'Alfobot tokeniza']

#df_recepcion=pd.read_csv("recep.csv",delimiter=";")
#df_recepcion=pd.io.json.read_json(f'cogs/datos/recep.json')

#Modo party
class Partymode(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None
    #Respuesta a los mensajes que recibe Alfobot
    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author != self.client.user) and (message.content not in commands_lista):
            irradiated,tokens_limpios=modelolemat.lemmatizer(message)
            #modelolemat.guardadoinputs(message,tokens_limpios)
            a=0
            if 'hola' in tokens_limpios:
              await message.channel.send('Hola, ¿Quieres un hack de vida?')
              a=1
              def check(m):
                return m.content == 'si'
              try:
                msg = await self.client.wait_for('message', check=check)
                # r=random.randint(0,len(df)-1)
                # await message.channel.send(str(df.iloc[r][0]))
              except:
                await message.channel.send('Chicos, No os escucho! ¿Queréis o no?')
            # elif 'elmo' in tokens_limpios:
            #   await message.channel.send('Es el verdadero Dios')
            #   a=1
            # elif 'jc' in tokens_limpios:
            #   await message.channel.send('JC? Quién es JC? si nunca puso cámara no existe.')
            #   a=1
            # elif 'hack' in tokens_limpios:
            #   r=random.randint(0,len(df)-1)
            #   await message.channel.send(str(df.iloc[r][0]))
            # elif "kahoot" in tokens_limpios:
            #   await message.channel.send('NOOOOOOO que me deprime')
            #   a=1
            # elif "daniela" in tokens_limpios:
            #   await message.channel.send('Seguid el canal de Daniela, que es una crack. \n https://www.youtube.com/channel/UCtYNTthydqffzioKVhFrX5A')
            #   a=1
            # elif 'hackaton' in tokens_limpios:
            #   r=random.randint(0,len(df)-1)
            #   await message.channel.send(str("Van a hacer una regresión de la puta ostia, si han sido mis alumnos"))
            # # elif "consumir" in tokens_limpios or "consume" in tokens_limpios or "consumes" in tokens_limpios or "consumo" in tokens_limpios:
            elif "bitcoin" in tokens_limpios:
              import requests
              from bs4 import BeautifulSoup
              url = "https://markets.businessinsider.com/currencies/btc-eur"
              response = requests.get(url)
              soup = BeautifulSoup(response.text, "html.parser")
              bitcoin_value = 'NaN'
              bitcoin_value = soup.find("span", class_ = "price-section__current-value").text
              #if not bitcoin_value: bitcoin_value = 'NaN'
              await message.channel.send(f'El bitcoin está ahora a {bitcoin_value}€. A qué estás esperando?')
              a = 1
            if a == 0:
              try:
                pool = modelolemat.creacionpool(tokens_limpios, 50)
                print(pool)
                respuesta = modelolemat.seleccionrespuesta(pool)
                print(respuesta)
                await message.channel.send(respuesta)
                def checkRisa(m):
                  return bool(re.search(r'jaj',m.content))
                risa = False
                try:
                  risa = await self.client.wait_for('message', timeout = 5.0, check = checkRisa) # Comprueba si se rien en los 5s siguientes
                except:
                  pass
                if risa != False:
                  modelopuntuacion.guardarjaja(respuesta)
                  await message.channel.send(str("Soy un puto genio"))
                  
                  # Envia gif con giphy
                  embed = discord.Embed(colour=discord.Colour.blue())
                  session = aiohttp.ClientSession()

                  # Gif aleatorio:
                  response = await session.get('https://api.giphy.com/v1/gifs/random?api_key='+apiGiphy)
                  data = json.loads(await response.text())
                  embed.set_image(url=data['data']['images']['original']['url'])

                  # Gif sobre temática 'search':

                  # search.replace(' ', '+')
                  # response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=API_KEY_GOES_HERE&limit=10')
                  # data = json.loads(await response.text())
                  # gif_choice = random.randint(0, 9)
                  # embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

                  await session.close()
                  await message.channel.send(embed=embed)

                # except:
                #   await message.channel.send('Si no me creen es su problema')
                a = 1
              except:
                pass
            
    #Guardado de reacciones a las propias reacciones
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.client.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.client.fetch_user(payload.user_id)
        emoji = payload.emoji
        modelopuntuacion.guardarreacciones(self.client.user, message,emoji)
def setup(client):
    client.add_cog(Partymode(client))
