#Cog Bert - Integración
import discord 
from discord.ext import commands
from funciones import modeloBert
from funciones import modoFUN
from funciones import modeloPuntuacion
from funciones import modeloNBrequest
from funciones import modeloMegat
from funciones import funElectorCode
from funciones import RequestFunction

# Para gráficas
import numpy as np
from numpy import sin, cos, tan, arcsin, arccos, arctan, hypot, arctan2, degrees, radians, sinh, cosh, tanh, arcsinh, arccosh, arctanh, exp, log, log10, log2 
import matplotlib.pyplot as plt
import math

import pandas as pd
import pickle
#from cogs import cogOptimo




class CogBert(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None
    @commands.Cog.listener()
    async def on_message(self, message):
        with open('datos/pasarela_ch','rb') as fh:
            df=pickle.load(fh)
        client=self.client
        try:
            with open(f'funciones/cogactivo.txt',"r") as ca:
                cog_activo=ca.read()
        except:
            cog_activo=False

        if (message.author != self.client.user) and ("jaja" not in message.content) and (cog_activo != "True") and (len(message.content)>1) and (df.at[str(message.channel),'cogBert']==1):
            msglower=message.content.lower()
            lista_tokens = modeloMegat.megatizer(message)[1]
            intencion=modeloBert.rayo_sesamo(message.content)
            
            # Intenciones:
            # 0: Info   1: Request  2: Ask  3: Fun
            await message.channel.send(str(intencion))

            # Modo Fun (3)
            if int(intencion)==3:
                try:
                    await message.channel.send(modoFUN.funresponse(message,self))
                except:
                    pass

            # Modo Request (1)
            elif int(intencion) == 1:
                tipo_request=modeloNBrequest.decision_request(message.content)
                print('aqui viene la magia')
                await message.channel.send(RequestFunction.decide_req(tipo_request))

            # Modo ask:
            elif int(intencion)==2:
                # Búsqueda en Youtube
                if "youtube" in msglower:
                    import urllib.parse, urllib.request, re

                    search = msglower.split('youtube')[1].split()

                    #search=['pollo mercadona', 'data']

                    query_string = urllib.parse.urlencode({'search_query': search})
                    htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
                    search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode() )
                    msg='http://www.youtube.com/watch?v=' + search_results[0]
                    await message.channel.send(msg)

            # if time:
            if ("calcula" in msglower) or ("resuelve" in msglower) or ("resolv" in msglower):
                a=0
                for i in msglower.split():
                    try:
                        await message.channel.send('Aquí tienes, no era tan difícil \n'+str(eval(i)))
                        a=1
                    except:
                        pass
                if a==0:
                    await message.channel.send(str("Mira, no tengo tiempo para esto. Mejor pregúntale a Daniela, que sabe mucho de estas cosas"))
            if "youtube" in msglower:
                import urllib.parse, urllib.request, re

                search = msglower.split('youtube')[1].split()

                #search=['pollo mercadona', 'data']

                query_string = urllib.parse.urlencode({'search_query': search})
                htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
                search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode() )
                msg='http://www.youtube.com/watch?v=' + search_results[0]
                await message.channel.send(msg)

def setup(client):
    client.add_cog(CogBert(client))