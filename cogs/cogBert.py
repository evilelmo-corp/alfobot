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
        if message.author != self.client.user:
            intencion=modeloBert.rayo_sesamo(message.content)
            await message.channel.send(str(intencion))
            if int(intencion)==3:
                await message.channel.send(modoFUN.funresponse(message,self))
                def checkRisa(m):
                    return bool(re.search(r'jaj',m.content))
                risa = False
                try:
                    risa = await self.client.wait_for('message', timeout = 30.0, check = checkRisa) # Comprueba si se rien en los 5s siguientes
                except:
                    pass
                if risa != False:
                    modeloPuntuacion.guardarjaja(respuesta)
                    await message.channel.send(modoFUN.risaReaccion())
                    print('risa detectada')
                    # Envía gif:
                    embed = discord.Embed(colour=discord.Colour.blue())
                    session = aiohttp.ClientSession()

                    # Gif sobre temática 'search':

                    search=random.choice(tokens_limpios)
                    
                    response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key='+apiGiphy+'&limit=10')
                    data = json.loads(await response.text())
                    gif_choice = random.randint(0, 9)
                    embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])
                    await session.close()

                    await message.channel.send(embed=embed)
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