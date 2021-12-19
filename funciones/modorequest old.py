'''
Funciones usadas cuando la intención es request
'''
import discord 
from discord.ext import commands
import pandas as pd
import numpy as np


# Variables globales para electorCode:
global ml_dict
global df_data

# Tabla de nombres de los códigos
ml_dict=pd.read_csv('cogs/datos/ml_dict.csv')
# Columnas de ml_dict: code, nombre, trigger

# Tabla con los códigos
df_data=pd.io.json.read_json(f'cogs/datos/datacheat.json')
df_data=df_data.T
df_data=df_data.reset_index()
df_data.columns=["key","value"]


class CogRequest(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

    def whichRequest(num):
        lista_tokens=pd.read_csv("ARCHIVO donde guardariamos el input megatizado?")['col1'].values[0]
        if num==1:
            electorCode(lista_tokens)
        elif num==2:
            bitcoin()
        elif num==3:
            grapher()

    # Elector Code:
    def electorCode(lista_tokens):
        codigo=[]
        for i,trigger in enumerate(ml_dict['trigger']):
            for token in lista_tokens:
                if len(token>1):
                    if token in trigger:
                        codigo.append(ml_dict.at[i,'code'])
        if len(codigo)>1:
            msg='No me queda claro qué quieres, aclárate!'
            for i in range(len(codigo)):
                msg+="\n"+str(i+1)+"    "+str(ml_dict[ml_dict['codigo']==codigo[i]]['nombre'].values[0])

            message.channel.send(msg)

            @commands.Cog.listener()
            async def on_message(self, message):
                if message.author != self.client.user:
                    msg='No me entero, crack'
                    for i in range(len(codigo)):
                        if str(i+1) in message.content:
                            ind=i
                            msg='Aquí tienes el código, pedazo de crack \n\n'+str(ml_dict[ml_dict['codigo']==codigo[ind]]['nombre'].values[0])+'\n\n'+str(df_data[df_data['key']==codigo[ind]]['value'].values[0])

        else:
            msg='Aquí tienes el código, pedzado de crack \n\n'+str(ml_dict[ml_dict['codigo']==codigo[0]]['nombre'].values[0])+'\n\n'+str(df_data[df_data['key']==codigo[0]]['value'].values[0])

        message.channel.send(msg)

    async def bitcoin():
        import requests
        from bs4 import BeautifulSoup
        url = "https://markets.businessinsider.com/currencies/btc-eur"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        bitcoin_value = 'NaN'
        bitcoin_value = soup.find("span", class_ = "price-section__current-value").text
        #if not bitcoin_value: bitcoin_value = 'NaN'
        await message.channel.send(f'El bitcoin está ahora a {bitcoin_value}€. A qué estás esperando?')

    
    def grapher():

        import numpy as np
        from numpy import sin, cos, tan, arcsin, arccos, arctan, hypot, arctan2, degrees, radians, sinh, cosh, tanh, arcsinh, arccosh, arctanh, exp, log, log10, log2 
        import matplotlib.pyplot as plt
        import math

        return message.channel.send("Escribe la ecuación que quieres graficar")

        @commands.Cog.listener()
        async def on_message(self, message):
            try:
                y=message.content.split('=')[1]

                plt.rcParams["figure.figsize"] = [7.00, 3.50]
                # plt.rcParams["figure.autolayout"] = True
                x = np.arange(-10., 10., 0.2)
                #y = arctanh(x)
                fig = plt.figure()
                ax = fig.add_subplot(1, 1, 1)
                ax.spines['left'].set_position('center')
                ax.spines['bottom'].set_position('center')
                ax.spines['right'].set_color('none')
                ax.spines['top'].set_color('none')
                plt.plot(x, y, label="y=x^2", c='blue')
                plt.legend(loc=1)
                plt.savefig('datos/elmoline.png',dpi=150)#, bbox_inches='tight') # Guarda la imagen
                
                # Envía la imagen
                embed = discord.Embed(color=discord.Colour.blue())
                file = discord.File("datos/elmoline.png", filename="elmoline.png")
                embed.set_image(url="attachment://elmoline.png")
                await message.channel.send(file=file, embed=embed)
            except:
                
                await message.channel.send('Mejor preguntale a Daniela que sabe mucho de esto')

        



def setup(client):
    client.add_cog(CogRequest(client))