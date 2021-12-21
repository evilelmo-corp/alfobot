# Cuando no solo necesitas que despierte, sino que ASCIENDA

import discord 
from discord.ext import commands
from funciones.comandos import lista_comandos
from funciones import funElectorCode, funBitcoin, funPypi, funGrapher, modoFUN, funSecretT
import pandas as pd
import numpy as np
import pickle


class CogAscension(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None
    @commands.Cog.listener()
    async def on_message(self, message):
        client=self.client
        with open('datos/pasarela_ch','rb') as fh:
            df=pickle.load(fh)
        if (message.author != self.client.user) and ("jaja" not in message.content) and (df.at[str(message.channel),'cogAscension']==1) and (message.content not in lista_comandos):
            msglower=message.content.lower()
            lista_tokens=message.content.lower().split()

            if ('cod' in lista_tokens) or ('codigo' in lista_tokens) or ('código' in lista_tokens):
                await funElectorCode.electorCode(lista_tokens,message,client)

            elif 'bitcoin' in lista_tokens:
                msg = funBitcoin.bitcoin()
                await message.channel.send(msg)

            elif ('calcula' in lista_tokens) or ('resuelve' in lista_tokens):
                for i in lista_tokens:
                    try:
                        await message.channel.send('Aquí tienes, no era tan difícil \n'+str(eval(i)))
                    except:
                        await message.channel.send(str("Mira, no tengo tiempo para esto. Mejor pregúntale a Daniela, que sabe mucho de estas cosas"))
            
            elif 'optimiza' in lista_tokens:
                await message.channel.send(str("Dime qué optimizar"))
                #CogOptimo.preguntasIniciales(message)
                await message.channel.send(str("Dime qué optimizar y yo lo hago:")+str("Necesito un csv con los datos limpio, MUY LIMPIO \n"+"También que me especifiques qué modelo deseas \n")+"Pero vamos en orden, que nada de esto es mágico. ¿Qué tipo de modelo quieres?")
                df.at[str(message.channel),'cogAscension']=0
                df.at[str(message.channel),'cogOptimo']=1
                with open('datos/pasarela_ch','wb') as fh:
                    pickle.dump(df,fh)                    
                self.client.load_extension(f'cogs.cogOptimo')
            
            elif 'install' in lista_tokens:
                try:
                    await message.channel.send(funPypi.pipy(lista_tokens))
                except:
                    await message.channel.send('Mira, búscalo y así aprendes')
            
            elif 'grafica' in lista_tokens:
                mensaje=message
                try:
                    file, embed = funGrapher.grapher(mensaje)
                    await message.channel.send(file=file, embed=embed)
                except:
                    await message.channel.send('Mejor preguntale a Daniela que sabe mucho de esto')

            elif 'analiza' in lista_tokens:
                await message.channel.send(str("Te analizo lo que quieras"))
            
            elif 'youtube' in lista_tokens:
                import urllib.parse, urllib.request, re

                search = message.content.lower().split('youtube')[1].split()

                query_string = urllib.parse.urlencode({'search_query': search})
                htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
                search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode() )
                msg='http://www.youtube.com/watch?v=' + search_results[0]
                await message.channel.send(msg)

            elif 'google' in msglower:
                from googlesearch import search
                
                query = msglower.split('google')[1].split()
                for j in search(query, tld="co.in", num=5, stop=5, pause=3):
                    await message.channel.send(j)

            else:
                try:
                    await message.channel.send(modoFUN.funresponse(message,self))
                except:
                    pass

            await funSecretT.secretT(lista_tokens,message,client)


def setup(client):
    client.add_cog(CogAscension(client))
            


            

