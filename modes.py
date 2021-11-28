import discord
from discord.ext import commands
import nltk
import pandas as pd
from datetime import datetime
#from main import client 

nltk.download('punkt')
nltk.download('spanish_grammars')
nltk.download('vader_lexicon')
nltk.download('stopwords')
palabras_funcionales=nltk.corpus.stopwords.words("spanish")
palabras_funcionales.extend([".", ",", ":", ";", "!", "?","'" ])
df=pd.io.json.read_json('frasest.json')
df_usuarios=pd.read_csv('pedidos.csv',delimiter=";")

# Sospecho que ela repetición de esto puede afectar
#client = commands.Bot(command_prefix='Alfobot ', description="simplificando DATOS dejé atrás mi forma corpórea")
# habrá que cambiar todos los client por commands.Cog?
class Partymode(client):
    def __init__(self,client):
        #self.client = self.commands.Cog
        self._last_member = None
    @client.listener()
    async def on_message(self, message):
        if message.author != self.client.user:
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
                msg = await self.client.wait_for('message', check=check)
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
                  print(message)
                  await message.channel.send(str(frase_pool.iloc[r][0]))
                  a=1
                  break
                except:
                  pass
                  
            df_usuarios.at[len(df_usuarios)]=[message.author,tokens_limpios,datetime.now()]
            df_usuarios.to_csv("pedidos.csv",sep=";",index=False,encoding='utf-8-sig')