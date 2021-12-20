#Cog Bert - Integración
import discord 
from discord.ext import commands
from funciones import modeloBert
from funciones import modoFUN
from funciones import modeloPuntuacion
from funciones import modeloNBrequest
from funciones import modeloMegat
#from cogs import cogOptimo



class CogBert(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            with open(f'funciones/cogactivo.txt',"r") as ca:
                cog_activo=ca.read()
        except:
            cog_activo=False
        if (message.author != self.client.user) and (message.content not in ["jaja","jajajaj","jajaj","jaj"]) and (cog_activo != "True"):
            lista_tokens = modeloMegat.megatizer(message)[0]
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
                    self.client.load_extension(f'cogs.cogElectorCode')

                    message.channel.send(msg)
                elif tipo_request == "Bitcoin":
                    await message.channel.send(str("Bitcoin"))
                elif tipo_request == "math":
                    await message.channel.send(str("Yo también sé hacer matemática"))
                elif tipo_request == "grid":
                    
                    await message.channel.send(str("Dime qué optimizar y yo lo hago:")+str("Necesito un csv con los datos limpio, MUY LIMPIO \n"+"También que me especifiques qué modelo deseas \n")+"Pero vamos en orden, que nada de esto es mágico. ¿Qué tipo de modelo quieres?")
                    self.client.load_extension(f'cogs.cogOptimo')
                elif tipo_request == "Install":
                    #await message.channel.send(str("PIP lo que quieras"))

                    # Buscador de instalador:
                    import requests
                    from bs4 import BeautifulSoup
                    search="pytorch"
                    for search in lista_tokens:
                        try:
                            url = "https://pypi.org/project/{}/".format(search)
                            response = requests.get(url)
                            soup = BeautifulSoup(response.text, "html.parser")
                            pip = soup.find(class_ = "banner").find(class_="package-header__pip-instructions").find(id="pip-command").text
                    
                            await message.channel.send(pip)
                        except:
                            pass

                elif tipo_request == "Grafica":
                    #await message.channel.send(str("Mi gráfica es mejor"))
                    import numpy as np
                    from numpy import sin, cos, tan, arcsin, arccos, arctan, hypot, arctan2, degrees, radians, sinh, cosh, tanh, arcsinh, arccosh, arctanh, exp, log, log10, log2 
                    import matplotlib.pyplot as plt
                    import math

                    try:
                        y=message.content.split('=')[1]

                        plt.rcParams["figure.figsize"] = [7.00, 3.50]
                        # plt.rcParams["figure.autolayout"] = True
                        x = np.arange(-10., 10., 0.01)
                        #y = arctanh(x)
                        fig = plt.figure()
                        ax = fig.add_subplot(1, 1, 1)
                        ax.spines['left'].set_position('center')
                        ax.spines['bottom'].set_position('center')
                        ax.spines['right'].set_color('none')
                        ax.spines['top'].set_color('none')
                        plt.plot(x, y, label='y='+str(y), c='blue',marker='.')
                        plt.legend(loc=1)
                        plt.savefig('datos/elmoline.png',dpi=150)#, bbox_inches='tight') # Guarda la imagen
                        
                        # Envía la imagen
                        embed = discord.Embed(color=discord.Colour.blue())
                        file = discord.File("datos/elmoline.png", filename="elmoline.png")
                        embed.set_image(url="attachment://elmoline.png")
                        await message.channel.send(file=file, embed=embed)
                    except:
                        
                        await message.channel.send('Mejor preguntale a Daniela que sabe mucho de esto')

                elif tipo_request == "Analisis":
                    await message.channel.send(str("Te analizo lo que quieras"))
                elif int(intencion) == 2:
                    pass #hay que hacer
                else:
                    pass

def setup(client):
    client.add_cog(CogBert(client))