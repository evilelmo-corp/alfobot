#Cog Bert - Integración
import discord 
from discord.ext import commands
from funciones import modeloBert
from funciones import modoFUN
from funciones import modeloPuntuacion



class CogBert(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None
    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author != self.client.user) and (message.content not in ["jaja","jajajaj","jajaj","jaj"]):
            intencion=modeloBert.rayo_sesamo(message.content)
            await message.channel.send(str(intencion))
            if int(intencion)==3:
                await message.channel.send(modoFUN.funresponse(message,self))
            elif int(intencion) == 1:
                pass #ADRI lo hizo
                #tipo_request=modelo.adri(message.content)
                #if tipo_request == x:

            elif int(intencion) == 2:
                pass #hay que hacer
            else:
                pass

def setup(client):
    client.add_cog(CogBert(client))