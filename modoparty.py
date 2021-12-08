import discord 
from discord.ext import commands 
from datetime import datetime
import random
import pandas as pd
import nltk
import re
import math 
import cliente

#Ingreso de datos

nltk.download('punkt')
nltk.download('spanish_grammars')
nltk.download('vader_lexicon')
nltk.download('stopwords')
palabras_funcionales=nltk.corpus.stopwords.words("spanish")
palabras_funcionales.extend([".", ",", ":", ";", "!", "?","'","jaja","jaj","jajaj","ja","jajaja","jajajajaj","jajaja" ])
df=pd.io.json.read_json('frasest.json')
tokens_frases=df.columns.drop(['frase','tokenizado'])
df_usuarios=pd.read_csv('pedidos.csv',delimiter=";")

sep=";.;..;.;;"

#df_recepcion=pd.read_csv("recep.csv",delimiter=";")
df_recepcion=pd.io.json.read_json("recep.json")
#Modo party
class Partymode(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None
    #Respuesta a los mensajes que recibe Alfobot
    @commands.Cog.listener()
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
            elif 'hackaton' in tokens_limpios:
              r=random.randint(0,len(df)-1)
              await message.channel.send(str("Van a hacer una regresión de la puta ostia, si han sido mis alumnos"))
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
            if a==0:
              frase_pool_pool=[]
              for tok_mes in tokens_limpios:
                le=math.ceil(len(tok_mes)*(2/3))
                for tok_fra in tokens_frases:
                  if tok_fra.startswith(tok_mes[:le]):
                  #if tok_mes[:le] in tok_fra:
                    frase_pool_pool.append(df[df[tok_fra]>0])
              try:
                r1=random.randint(0,len(frase_pool_pool)-1)
                frase_pool=frase_pool_pool[r1]
                r2=random.randint(0,len(frase_pool)-1)
                print(frase_pool)
                print(r2)
                await message.channel.send(str(frase_pool.iloc[r2][0]))
                a=1
              except:
                pass
            df_usuarios.at[len(df_usuarios)]=[message.author,tokens_limpios,datetime.now()]
            df_usuarios.to_csv("pedidos.csv",sep=";",index=False,encoding='utf-8-sig')
            with open("inputs.csv","a") as fh:
                fh.write("\n"+str(datetime.now())+sep+str(message.author)+sep+"'"+str(message.content)+"'"+sep+str(tokens_limpios))
    #Guardado de reacciones a las propias reacciones
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.client.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.client.fetch_user(payload.user_id)
        emoji = payload.emoji
        if self.client.user == message.author:
            num_frase=df[df["frase"]==message.content].index.values[0]
            if num_frase in df_recepcion['Frases'].values:
                print(df_recepcion[df_recepcion["Frases"]==num_frase].index.values)
                linea=df_recepcion[df_recepcion["Frases"]==num_frase].index.values
                conjunto=df_recepcion.columns
                if emoji.name in conjunto:
                    df_recepcion[emoji.name].iat[linea[0]]+=1
                    print("encontrado")
                else:
                    print("no encontrado")
                    df_recepcion[emoji.name]=0
                    df_recepcion[emoji.name].iat[linea[0]]=1
            else:
                u_linea=len(df_recepcion)
                linea_ceros=[0 for x in range(len(df_recepcion.columns))]
                linea_ceros[0]=num_frase
                df_recepcion.at[u_linea]=linea_ceros
                conjunto=set(df_recepcion.columns)
                if emoji.name in conjunto:
                    df_recepcion[emoji.name].iat[u_linea]+=1
                    print("encontrado-primeravez")
                else:
                    print("no encontradoprimeravez")
                    #conjunto.add(emoji)
                    df_recepcion[emoji.name]=0
                    df_recepcion[emoji.name].iat[u_linea]=1
        df_recepcion.to_csv("recep.csv",index=False, sep=";")
        df_recepcion.to_json("recep.json")
def setup(client):
    client.add_cog(Partymode(client))
