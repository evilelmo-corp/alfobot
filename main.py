import discord 
from discord.ext import commands 
from datetime import datetime
import random
import pandas as pd
import nltk
from tokenizador_frases import tokenizar # asi!!Exacto!:D jaja
from modes import profe_mode

df_data=pd.io.json.read_json('datacheat.json')
df_data=df_data.T
df_data=df_data.reset_index()
df_data.columns=["key","value"]

nltk.download('punkt')
nltk.download('spanish_grammars')
nltk.download('vader_lexicon')
nltk.download('stopwords')
palabras_funcionales=nltk.corpus.stopwords.words("spanish")
palabras_funcionales.extend([".", ",", ":", ";", "!", "?","'" ])

client = commands.Bot(command_prefix='Alfobot ', description="this is a testing bot")

df=pd.io.json.read_json('frasest.json')
df_usuarios=pd.read_csv('pedidos.csv',delimiter=";")


@client.command()
# Modo party:
async def despierta(ctx):
  await ctx.send('Chicos estoy aquí, hablen')
  @client.command() 
  async def profe(ctx):
    profe_mode() # no se si funcionará así
  # Para apacar el bot por completo:
  #@client.command() 
  # async def logout(ctx):
  #   await ctx.send('Shutting down')
  #   await client.logout() ova con BOT, porrque lo llamamos client
  @client.event
  async def on_message(message):
    if message.author != client.user:
      if "duerme" in message.content:
        await client.logout()
      tokens=nltk.word_tokenize(message.content,"spanish")
      tokens_limpios=[] 
      tokens = [token.lower() for token in tokens]
      for token in tokens: 
          if token not in palabras_funcionales: 
              tokens_limpios.append(token)

      print(tokens_limpios)
      a=0

      if 'hola' in tokens_limpios:
          await message.channel.send('Hola, ¿Quieres un hack de vida?')
          a=1
          # def check(reaction, user):
          #     return user == message.author and (reaction == 'si' or reaction == 'sí')
          #try:
          def check(m):
            return m.content == 'si'

          try:
            msg = await client.wait_for('message', check=check)
            r=random.randint(0,len(df)-1)
            await message.channel.send(str(df.iloc[r][0]))
          except:
            await message.channel.send('Chicos, No os escucho! ¿Queréis o no?')
      elif 'elmo' in tokens_limpios:
        await message.channel.send('Es el verdadero Dios')
        a=1
      elif 'jc' in tokens_limpios:
        await message.channel.send('JC? Quién es JC? si nunca puso cámara no existe.')
        a=1
      elif 'hack' in tokens_limpios:
        r=random.randint(0,len(df)-1)
        await message.channel.send(str(df.iloc[r][0]))
      elif "kahoot" in tokens_limpios:
        await message.channel.send('NOOOOOOO que me deprime')
        a=1
      elif "daniela" in tokens_limpios:
        await message.channel.send('Seguid el canal de Daniela, que es una crack. \n https://www.youtube.com/channel/UCtYNTthydqffzioKVhFrX5A')
        a=1

      elif "coca" in tokens_limpios:
        await message.channel.send('¿Hay que reducir el consumo? Puede ser. Pero también hay que reducir el paro juvenil, el consumo de procesados y la polarización radical...')
        a=1
      
      if a==0:
        for token in tokens_limpios:
          
          try:
            frase_pool=df[df[token]>0]
            print(frase_pool['frase'])
            r=random.randint(0,len(frase_pool)-1)
            await message.channel.send(str(frase_pool.iloc[r][0]))
            a=1
            break
          except:
            pass

      df_usuarios.at[len(df_usuarios)]=[message.author,tokens_limpios,datetime.now()]
      df_usuarios.to_csv("pedidos.csv",sep=";",index=False,encoding='utf-8-sig')

# Modo profesor: 
@client.command()     
async def profe(ctx):
  profe_mode()


  # await ctx.send('Chicos vamos serios, hablen')
  # @client.event
  # async def on_message(message):
  #   if message.author != client.user:
  #     if "duerme" in message.content:
  #       await client.logout()
  #     if message.content in list(df_data.key):
  #       await message.channel.send(df_data[df_data['key']==str(message.content)]["value"])

# Refrescar frases party:
@client.command()
async def tokeniza(ctx):
  tokenizar()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="_help"))
    print('My bot is ready')

client.run('OTEzMTkxMTk4MTE2Njg3OTIy.YZ65kw.id9oVV8sMjXLkuEpR1FlC6-NNZA')
