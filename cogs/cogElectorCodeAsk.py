'''
Función que da el código de modelos de Machine Learning que el usario pida
'''

import discord 
from discord.ext import commands

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


class cogElectorCode(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

    #self.client.unload_extension(f'cogs.cogBert')

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

        self.client.channel.send(msg)

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

    self.client.load_extension(f'cogs.cogBert')


def setup(client):
    client.add_cog(cogElectorCode(client))