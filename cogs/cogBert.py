#Cog Bert - Integración
import discord 
from discord.ext import commands
from funciones import modeloBert
from funciones import modoFUN
from funciones import modeloPuntuacion
from funciones import modeloNBrequest
from funciones import modeloMegat
from funciones import modeloNBask
from funciones import funRequest
from funciones import funSecretT
from funciones import funAsk
from funciones.comandos import lista_comandos


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

        if (message.author != self.client.user) and ("jaja" not in message.content) and (cog_activo != "True") and (len(message.content)>1) and (df.at[str(message.channel),'cogBert']==1) and (message.content not in lista_comandos):
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
                await message.channel.send(str(tipo_request))
                # Llama a la megafución request
                await funRequest.request(lista_tokens,message,client,tipo_request)

            # Modo ask (2):
            elif int(intencion)==2:

                tipo_request=modeloNBask.decision_ask(message.content)
                await message.channel.send(str(tipo_request))
                await funAsk.tipo_preg(lista_tokens,message,client,tipo_request, self)
                
            await funSecretT.secretT(lista_tokens,message,client)


def setup(client):
    client.add_cog(CogBert(client))