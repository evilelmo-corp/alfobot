import discord 
from discord.ext import commands
import pandas as pd
import numpy as np
import pickle

from funciones import modoFUN
from funciones import funRequest

# Modo ask:
async def tipo_preg(lista_tokens,message,client,tipo_request,self):
#ASK Generar
    if tipo_request == "Generar":
        await message.channel.send(str("*GENERANDO CONTENIDO*"))
        try:
            await message.channel.send(modoFUN.funresponse(message,self))
        except:
            pass

#ASK Busqueda
    elif tipo_request == 'Busqueda':
        msglower = message.content.lower()
        # Búsqueda en Youtube
        if "youtube" in msglower:
            import urllib.parse, urllib.request, re

            search = msglower.split('youtube')[1].split()

            query_string = urllib.parse.urlencode({'search_query': search})
            htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
            search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode() )
            msg='http://www.youtube.com/watch?v=' + search_results[0]
            await message.channel.send(msg)

        #Búsqueda en google
        if "google" in msglower:
            from googlesearch import search
            
            query = msglower.split('google')[1].split()
            for j in search(query, tld="co.in", num=5, stop=5, pause=3):
                await message.channel.send(j)

        #Busca en google todo el mensaje si no detecta algo
        else:
            from googlesearch import search
            query = message.content
            for j in search(query, tld="co.in", num=5, stop=5, pause=3):
                await message.channel.send(j)

#ASK Inseguro
    elif tipo_request=='Inseguro':
        mensaje = message.content.replace('?','')
        tipo_request_ins=modeloNBrequest.decision_request(mensaje)
        await funRequest.request(lista_tokens,message,client,tipo_request_ins)