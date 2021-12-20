'''
Función que da el código de modelos de Machine Learning que el usario pida
'''

import discord 
from discord.ext import commands
import pickle
import pandas as pd

# from funciones import funElectorCode

# global mensaje

# mensaje=funElectorCode.mensaje

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


with open(f'funciones/cogactivo.txt',"w") as ca:
    ca.write("True")

with open('file_code', "rb") as file_code:
    codigo = pickle.load(file_code)


class cogElectorCode(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

    #self.client.unload_extension(f'cogs.cogBert')
    @commands.Cog.listener()
    async def on_message(self, message):
        with open('datos/pasarela_ch','rb') as fh:
            df=pickle.load(fh)
        if message.author != self.client.user and (df.at[str(message.channel),'cogElectorCodeAsk']==1):
            msg='No me entero, crack'
            for i in range(len(codigo)):
                if str(i+1) in message.content:
                    msg0='Aquí tienes el código, pedazo de crack \n\n'
                    msg1=str(ml_dict[ml_dict['codigo']==codigo[i]]['nombre'].values[0])
                    msg2='\n\n'+str(df_data[df_data['key']==codigo[i]]['value'].values[0])
                    msg=msg0+msg1+msg2
            await message.channel.send(msg)

        with open(f'funciones/cogactivo.txt',"w") as ca:
            ca.write("False")
        df.at[str(message.channel),'cogElectorCodeAsk']=0
        df.at[str(message.channel),'cogBert']=1
        with open('datos/pasarela_ch','wb') as fh:
            pickle.dump(df,fh)

        self.client.unload_extension(f'cogs.cogElectorCodeAsk')


def setup(client):
    client.add_cog(cogElectorCode(client))