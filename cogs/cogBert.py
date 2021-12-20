#Cog Bert - Integración
import discord 
from discord.ext import commands
from funciones import modeloBert
from funciones import modoFUN
from funciones import modeloPuntuacion
from funciones import modeloNBrequest
from funciones import modeloMegat

import pandas as pd
import numpy as np
#from cogs import cogOptimo

# Variables globales para electorCode:
global ml_dict
global df_data

# Tabla de nombres de los códigos
ml_dict=pd.read_csv('datos/ml_dict.csv')
# Columnas de ml_dict: codigo, nombre, trigger

# Tabla con los códigos
df_data=pd.io.json.read_json(f'datos/datacheat.json')
df_data=df_data.T
df_data=df_data.reset_index()
df_data.columns=["key","value"]



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
        if (message.author != self.client.user) and ("jaja" not in message.content) and (cog_activo != "True") and len(message.content)>1:
            lista_tokens = modeloMegat.megatizer(message)[1]
            # with open(f'datos/lista_tokens.txt',"w") as ca:
            #     ca.write(lista_tokens)
            intencion=modeloBert.rayo_sesamo(message.content)
            await message.channel.send(str(intencion))
            # Modo Fun
            if int(intencion)==3:
                try:
                    await message.channel.send(modoFUN.funresponse(message,self))
                except:
                    pass
            # Modo Request
            elif int(intencion) == 1:
                tipo_request=modeloNBrequest.decision_request(message.content)
                await message.channel.send(str(tipo_request))
                # Request Elector Code
                if tipo_request == "ML":
                    await message.channel.send(str("TOMAS AQUI VA TU MAGIA"))
                    #self.client.load_extension(f'cogs.cogElectorCode')
                    codigo=[]
                    for i,trigger in enumerate(ml_dict['trigger']):
                        for token in lista_tokens:
                            if len(token)>1:
                                if token in trigger:
                                    codigo.append(ml_dict.at[i,'codigo'])
                    if len(codigo)>1:
                        msg='No me queda claro qué quieres, aclárate!'
                        for i in range(len(codigo)):
                            msg+="\n"+str(i+1)+"    "+str(ml_dict[ml_dict['codigo']==codigo[i]]['nombre'].values[0])

                        await message.channel.send(msg)
                        # Llama al cog que recibe la respuesta
                        #self.client.load_extension(f'cogs.cogElectorCodeAsk')
                        def check(m):
                            return len(m.content)==1 and m.channel == channel

                        message = await client.wait_for('message', timeout = 60.0, check=check)
                        msg='No me entero, crack'
                        for i in range(len(codigo)):
                            if str(i+1) in message.content:
                                ind=i
                                msg='Aquí tienes el código, pedazo de crack \n\n'+str(ml_dict[ml_dict['codigo']==codigo[ind]]['nombre'].values[0])+'\n\n'+str(df_data[df_data['key']==codigo[ind]]['value'].values[0])
                    else:
                        msg='Aquí tienes el código, pedazo de crack \n\n'+str(ml_dict[ml_dict['codigo']==codigo[0]]['nombre'].values[0])+'\n\n'+str(df_data[df_data['key']==codigo[0]]['value'].values[0])

                    await message.channel.send(msg)
                    
                # Request Bitcoin
                elif tipo_request == "Bitcoin":
                    await message.channel.send(str("Bitcoin"))
                # Request Math
                elif tipo_request == "math":
                    await message.channel.send(str("Yo también sé hacer matemática"))
                # Request GridSearch
                elif tipo_request == "grid":
                    
                    await message.channel.send(str("Dime qué optimizar"))
                    #CogOptimo.preguntasIniciales(message)
                    await message.channel.send(str("Optimizatelo tú"))
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