
import discord 
from discord.ext import commands
import pandas as pd
import numpy as np
import pickle

# global mensaje


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

async def electorCode(lista_tokens,message,client):
    # mensaje=message
    with open('datos/pasarela_ch','rb') as fh:
        df=pickle.load(fh)
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
        with open('file_code', "wb") as file_code:
            pickle.dump(codigo, file_code)

        # Si llama a cogElectorCodeAsk
        df.at[str(message.channel),'cogBert']=0
        df.at[str(message.channel),'cogElectorCodeAsk']=1
        with open('datos/pasarela_ch','wb') as fh:
            pickle.dump(df,fh)
        # Llama al cog que recibe la respuesta
        client.load_extension(f'cogs.cogElectorCodeAsk')
        
    else:
        msg0='Aquí tienes el código, pedazo de crack \n\n'
        msg1=str(ml_dict[ml_dict['codigo']==codigo[0]]['nombre'].values[0])
        msg2='\n\n'+str(df_data[df_data['key']==codigo[0]]['value'].values[0])
        msg=msg0+msg1+msg2

        await message.channel.send(msg)


        df.at[str(message.channel),'cogBert']=1
        with open('datos/pasarela_ch','wb') as fh:
            pickle.dump(df,fh)