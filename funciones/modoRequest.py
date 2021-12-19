'''
Función que llama a la función/cog correspondiente de las funcionalidades de request
'''



def whichRequest(num):
    df=pd.read_csv("datos/inputs_evilelmo.csv",columns=['datetime','channel','user','msg','tokens','mentions'])
    lista_tokens = df.at[len(df)-1,'tokens'].values
    if num==1:
        electorCode(lista_tokens)
    elif num==2:
        bitcoin()
    elif num==3:
        grapher()