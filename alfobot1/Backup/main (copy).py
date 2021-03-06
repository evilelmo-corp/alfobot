import discord 
from discord.ext import commands 
from datetime import datetime
import random
import pandas as pd
import nltk
from tokenizador_frases import tokenizar
import re
import keep_alive 

#Ingreso de datos
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
df=pd.io.json.read_json('frasest.json')
df_usuarios=pd.read_csv('pedidos.csv',delimiter=";")

sep=";.;..;.;;"


# Variables de control de reproducción
global modoprofe
global modoparty
modoprofe=False
modoparty=False

#Set del BOT
client = commands.Bot(command_prefix='Alfobot ', description="simplificando DATOS dejé atrás mi forma corpórea")

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
        client.add_cog(Profemode(client))
        modoprofe=True
        await ctx.send('Chicos, vamos serios. Hablad.')
        try:
          client.remove_cog('Partymode')
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
        client.add_cog(Profemode(client))
        modoprofe=True
        await ctx.send('Chicos, vamos serios. Hablad')
        try:
          client.remove_cog('Partymode')
          modoparty=False
        except:
          pass
    else:
        await ctx.send('Os estoy esperando en Zoom. HABLAD!')

@client.command()
async def party(ctx):
    global modoparty
    global modoprofe
    if modoparty==False:
        client.add_cog(Partymode(client))
        modoparty=True
        await ctx.send('Chicos estoy aquí, hablen')
        try:
          client.remove_cog('Profemode')
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
        client.remove_cog('Profemode')
        modoprofe=False
        await ctx.send('Chao chicos, nos vemos mañana')
    elif modoparty == True:
        client.remove_cog('Partymode')
        modoparty=False
        # await ctx.send('¿Quién dijo que me voy a dormir?')
        await ctx.send('Oh no, se me acabó el café')
    else: # modoprofe == False and modoparty == False:
        # await ctx.send('Si me necesitan, me pueden despertar')
        await ctx.send('ZzZzZzZzZzZ...')
        
#Modo clases
class Profemode(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != client.user:
            print(list(df_data.key))
            print(message)
            if message.content in list(df_data.key):
                await message.channel.send(str(df_data[df_data['key']==str(message.content)]["value"].values[0]))

class Partymode(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != client.user:
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
            # elif "consumir" in tokens_limpios or "consume" in tokens_limpios or "consumes" in tokens_limpios or "consumo" in tokens_limpios:
            elif "bitcoin" in tokens_limpios:
              import requests
              from bs4 import BeautifulSoup
              url = "https://markets.businessinsider.com/currencies/btc-eur"
              response = requests.get(url)
              soup = BeautifulSoup(response.text, "html.parser")
              bitcoin_value='NaN'
              bitcoin_value = soup.find("span", class_="price-section__current-value").text
              #if not bitcoin_value: bitcoin_value = 'NaN'
              await message.channel.send(f'El bitcoin está ahora a {bitcoin_value}€. A qué estás esperando? ')
              a=1
            else:
              try:
                r = re.compile("consum*")
                if len( list(filter(r.match, tokens_limpios)) ) > 0:
                  await message.channel.send('¿Hay que reducir el consumo? Puede ser. Pero también hay que reducir el paro juvenil, el consumo de procesados y la polarización radical...')
                  a=1
              except:
                pass
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

            #Guardando los mensajes completos con append (más ligero)
            #(El separador es raro porque creo que debe ser una combinacion de caracteres que nunca se ponga en el chat, para no romper el csv)
            with open("inputs.csv","a") as fh:
              fh.write("\n"+str(datetime.now())+sep+str(message.author)+sep+"'"+str(message.content)+"'"+sep+str(tokens_limpios))


# Refrescar frases party:
@client.command()
async def tokeniza(ctx):
    await tokenizar()

keep_alive.keep_alive()

client.run('OTEzMTkxMTk4MTE2Njg3OTIy.YZ65kw.id9oVV8sMjXLkuEpR1FlC6-NNZA')