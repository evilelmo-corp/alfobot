'''
modeloLemat
funciones:
    lemmascrapper()
    megatizer()
'''

import discord 
import pickle
from discord.ext import commands
from datetime import datetime
import random
import pandas as pd
import re
import numpy as np
import math
import requests
from bs4 import BeautifulSoup
from collections import Counter
from os import remove

#megatizer
global nombres_propios
global palabras_funcionales
global puntuacion
global lemma_ray

nombres_propios=pd.DataFrame(columns=["nombre"])
try:
    nombres_propios=pd.read_csv(f'datos/nombres_propios.txt')
except:
    pass
#nombres_propios.columns='nombre'

with open(f'datos/palabras_funcionales.txt','r') as fh:
    palabras_funcionales=[line.strip().strip(',').strip("'") for line in fh]

puntuacion = (',','"',"'",'.',';',':','(',')','[',']','-','<','>','!','¡','?','¿','—','#','_','`','´','..','...')

palabras_funcionales.extend(puntuacion)

with open(f'datos/rayo_lemmatizador' , 'rb') as f:
	lemma_ray = pickle.load(f)



# lemmascrapper
def lemmascrapper(token):
    '''
    Escrapea en the free dictionary la palabra recibida y busca su lema, 
    si no lo encuentra devuelve un error
    '''
    url="https://es.thefreedictionary.com/"+token
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    req = requests.get(url, headers=headers)
    soup= BeautifulSoup(req.text, "lxml")
    resultado=soup.find('div', class_="content-holder")
    # print(resultado.h1.text,"RESULTADO SCRAP")
    #Control de que sea una palabra real
    if soup.find('div', id="Definition") == None:
        raise ValueError("Esta palabra no lleva a ningún lema")
    else:
        tipo=soup.find('i')
        return resultado.h1.text,tipo.text[0]


# Megatizer
def megatizer(message):
    m=5
    lista_tokens=message.content.split()
    clean_tokens=[]
    all_tokens=[]
    
    for token in lista_tokens:
        if len(token)==0:
            pass
        elif re.search('[0-9]+', token) is not None:
            pass
        else:
            token=token.lower() 
            if token not in palabras_funcionales:
                if 'jaja' not in token:
                    # Funcion limpiadora (será lenta?)
                    for i in puntuacion:
                        token=token.strip(i)
                    clean_tokens.append(token)
    #print(clean_tokens)
    
    for token in lista_tokens:
        if len(token)==0:
            pass
        token=token.lower()
        a=0
        for i in puntuacion:
            if i in token:
                a=1
                token2=token.strip(i)
                if token[0]==i:
                    all_tokens.append(i)
                    all_tokens.append(2)
                    
                elif token[len(token)-1]==i:
                    all_tokens.append(token2)
                    all_tokens.append(i)
                break
        if a==0:
            all_tokens.append(token)
                    
    
                    
    lemmas, toklemmas, all_lemmas = [],[],[]
    
    for token in clean_tokens:
        try:
            # Busca la palabra en la lista de lemmas
            lemmas.append(lemma_ray[lemma_ray['Form']==token].lemma.values[0].lower())
            toklemmas.append(lemma_ray[lemma_ray['Form']==token].lemma.values[0].lower())
            #print(token,'encontrado en lemma_ray')
        except:
            # Busca la palabra en nombres_propios
            if token in nombres_propios['nombre']:
                if len(token)<(m):
                    lemmas.append(token)
                    #print(token,'encontrado en nombres_propios, corto')
                else:
                    lemmas.append(token[:int(len(token)*((m-1)/m))])
                    #print(token,'encontrado en nombres_propios, largo')
                toklemmas.append(token)
            else:
                try:
                    # Busca la palabra en internet
                    lemma,tipo =lemmascrapper(token)
                    lemmas.append(str(lemma).lower())
                    toklemmas.append(str(lemma).lower())
                    #print(token,'encontrado en la web')
                    # Guarda la palabra encontrada en a_pickelizar
                    with open(f"datos/a_pickelizar.txt","a") as fh:
                        try:
                            fh.write(str(lemma)+","+str(tipo)+";")
                        except UnicodeEncodeError:
                            pass
                            #print(str(lemma), str(tipo))
                except:
                    # Si no la encuentra
                    if len(token)<(m):
                        lemmas.append(token)
                        #print(token,'no encontrado, corto')
                    else:
                        lemmas.append(token[:int(len(token)*((m-1)/m))])
                        #print(token,'no encontrado, largo')
                    toklemmas.append(token)
                    # Guarda la palabra en nombres_propios
                    nombres_propios.at[len(nombres_propios),'nombre']=token
                    with open(f"datos/nombres_propios.txt","a") as fh:
                        try:
                            fh.write(str(token)+"\n")
                        except UnicodeEncodeError:
                            pass
                        
    for token in all_tokens:
        try:
            # Busca la palabra en la lista de lemmas
            all_lemmas.append(lemma_ray[lemma_ray['Form']==token].lemma.values[0].lower())
            #print(token,'encontrado en lemma_ray')
        except:
            # Busca la palabra en nombres_propios
            if token in nombres_propios['nombre']:
                all_lemmas.append(token)
            else:
                try:
                    # Busca la palabra en internet
                    lemma,tipo =lemmascrapper(token)
                    all_lemmas.append(str(lemma).lower())
                    #print(token,'encontrado en la web')
                    # Guarda la palabra encontrada en a_pickelizar
                    with open(f"datos/a_pickelizar.txt","a") as fh:
                        try:
                            fh.write(str(lemma)+","+str(tipo)+";")
                        except UnicodeEncodeError:
                            pass
                            #print(str(lemma), str(tipo))
                except:
                    # Si no la encuentra
                    all_lemmas.append(token)
                    # Guarda la palabra en nombres_propios
                    nombres_propios.at[len(nombres_propios),'nombre']=token
                    # with open(f"/cogs/datos/nombres_propios.txt","a") as fh:
                    #     try:
                    #         fh.write(str(token)+"\n")
                    #     except UnicodeEncodeError:
                    #         pass
            
    return lemmas, toklemmas, all_lemmas



