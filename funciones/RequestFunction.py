import discord 
from discord.ext import commands
from funciones import modeloBert
from funciones import modoFUN
from funciones import modeloPuntuacion
from funciones import modeloNBrequest
from funciones import modeloMegat
from funciones import funElectorCode
from funciones import analRequest

# Para gráficas
import numpy as np
from numpy import sin, cos, tan, arcsin, arccos, arctan, hypot, arctan2, degrees, radians, sinh, cosh, tanh, arcsinh, arccosh, arctanh, exp, log, log10, log2 
import matplotlib.pyplot as plt
import math

import pandas as pd
import pickle

async def decide_req(tipo_request)
         
    # Request Elector Code
    if tipo_request == "ML":
        client=self.client
        # df.at[str(message.channel),'cogBert']=0
        # with open('datos/pasarela_ch','wb') as fh:
        #     pickle.dump(df,fh)
        await funElectorCode.electorCode(lista_tokens,message,client)
        
    # Request Bitcoin
    elif tipo_request == "Bitcoin":
        import requests
        from bs4 import BeautifulSoup
        url = "https://markets.businessinsider.com/currencies/btc-eur"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        bitcoin_value = 'NaN'
        bitcoin_value = soup.find("span", class_ = "price-section__current-value").text
        #if not bitcoin_value: bitcoin_value = 'NaN'
        await message.channel.send(f'El bitcoin está ahora a {bitcoin_value}€. A qué estás esperando?')

    # Request Math
    elif tipo_request == "math":
        a=0
        for i in message.content.split():
            try:
                await message.channel.send('Aquí tienes, no era tan difícil \n'+str(eval(i)))
                a=1
            except:
                pass
        if a==0:
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

    #Request Graficar
    elif tipo_request == "Grafica":
        #await message.channel.send(str("Mi gráfica es mejor"))

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

    #Request Analisis
    elif tipo_request == "Analisis":
        await message.channel.send(analRequest.analizador(message.content))