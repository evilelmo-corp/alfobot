import discord 
from discord.ext import commands
import pandas as pd
import numpy as np
import pickle

from funciones import funBitcoin, funPypi, funGrapher, funElectorCode, analRequest


async def request(lista_tokens,message,client,tipo_request):

    # Request Machine Learning
    if tipo_request == "ML":
        await message.channel.send(str("TOMAS AQUI VA TU MAGIA"))
        #client=self.client
        
        # df.at[str(message.channel),'cogBert']=0
        # with open('datos/pasarela_ch','wb') as fh:
        #     pickle.dump(df,fh)
        await funElectorCode.electorCode(lista_tokens,message,client)
        
    # Request Bitcoin
    elif tipo_request == "Bitcoin":
        await message.channel.send(str("Bitcoin"))
        msg = funBitcoin.bitcoin()
        await message.channel.send(msg)

    # Request Math
    elif tipo_request == "math":
        for i in message.content.split():
            try:
                await message.channel.send('Aquí tienes, no era tan difícil \n'+str(eval(i)))
            except:
                await message.channel.send(str("Mira, no tengo tiempo para esto. Mejor pregúntale a Daniela, que sabe mucho de estas cosas"))

    # Request GridSearch
    elif tipo_request == "grid":
        await message.channel.send(str("Dime qué optimizar"))
        #CogOptimo.preguntasIniciales(message)
        await message.channel.send(str("Dime qué optimizar y yo lo hago:")+str("Necesito un csv con los datos limpio, MUY LIMPIO \n"+"También que me especifiques qué modelo deseas \n")+"Pero vamos en orden, que nada de esto es mágico. ¿Qué tipo de modelo quieres?")
        df.at[str(message.channel),'cogBert']=0
        df.at[str(message.channel),'cogOptimo']=1
        with open('datos/pasarela_ch','wb') as fh:
            pickle.dump(df,fh)                    
        
        self.client.load_extension(f'cogs.cogOptimo')

    # Request install
    elif tipo_request == "Install":
        await message.channel.send(str("PIP lo que quieras"))
        try:
            await message.channel.send(funPypi.pipy(lista_tokens))
        except:
            await message.channel.send('Mira, búscalo y así aprendes')

    # Request Gráfica
    elif tipo_request == "Grafica":
        #await message.channel.send(str("Mi gráfica es mejor"))
        mensaje=message
        try:
            file, embed = funGrapher.grapher(mensaje)
            await message.channel.send(file=file, embed=embed)
        except:
            await message.channel.send('Mejor preguntale a Daniela que sabe mucho de esto')

    # Request Análisis

    elif tipo_request == "Analisis":
        await message.channel.send(str("Te analizo lo que quieras, dame algo"))
        tags = analRequest.tagger(message.content)
        await message.channel.send(str(tags))


