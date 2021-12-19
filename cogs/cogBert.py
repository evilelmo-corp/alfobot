#Cog Bert - Integración
import discord 
from discord.ext import commands
from funciones import modeloBert
from funciones import modoFUN
from funciones import modeloPuntuacion
from funciones import modeloNBrequest


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
                try:
                    await message.channel.send(modoFUN.funresponse(message,self))
                except:
                    pass
            elif int(intencion) == 1:
                tipo_request=modeloNBrequest.decision_request(message.content)
                await message.channel.send(str(tipo_request))
                if tipo_request == "ML":
                    await message.channel.send(str("TOMAS AQUI VA TU MAGIA"))
                elif tipo_request == "Bitcoin":
                    await message.channel.send(str("Bitcoin"))
                elif tipo_request == "math":
                    await message.channel.send(str("Yo también sé hacer matemática"))
                elif tipo_request == "grid":
                    await message.channel.send(str("Optimizatelo tú"))
                elif tipo_request == "Install":
                    await message.channel.send(str("PIP lo que quieras"))
                elif tipo_request == "Grafica":
                    await message.channel.send(str("Mi gráfica es mejor"))
                elif tipo_request == "Analisis":
                    await message.channel.send(str("Te analizo lo que quieras"))
            elif int(intencion) == 2:
                pass #hay que hacer
            else:
                pass

def setup(client):
    client.add_cog(CogBert(client))