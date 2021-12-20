
import pandas as pd
import os
import pickle

os.chdir('../cogs')
cogs_lista = [x for i in os.listdir() if x.startswith('cog')]

df=pd.DataFrame(columns=cogs_lista)

def pasarelaChannel(channel):
    with open('/datos/pasarela_ch','rb') as fh:
	    df = pickle.load(df,fh)
