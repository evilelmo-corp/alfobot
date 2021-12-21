import pandas as pd
import numpy as np
import pickle

def camerino(frase):
    with open('datos/columnas', 'rb') as files:
        colum=pickle.load(files)
    df = pd.DataFrame(columns = ['Lemma', 'Punct','Mayus', 'Ultima', 'Primera',
                                 'Suf_sus', 'Suf_adj','Suf_ver','Suf_adv',
                                 'Afi_dim', 'Afi_aum', 'Afi_des'])
    frase = frase.split()
    for i in range(len(frase)):
        tupla = listalizador(frase,i)
        df.at[i,:] = tupla
    listas=[]
    for i in range(len(df)):
        conjunto=list(colum)
        lista_metible=[0 for x in range(len(colum))]
        if df.Lemma.iloc[i] in conjunto:
            indice=conjunto.index(df.Lemma.iloc[i])
            lista_metible[indice]=1
        for co in df.columns:
            if co in conjunto:
                indice=conjunto.index(co)
                lista_metible[indice]=df[co].iloc[i]
        listas.append(lista_metible)
    return listas


def listalizador(frase, indice):
#Sufijos. #Simplificandodummies    
    palabra = frase[indice]
    puntuacion = (',','"',"'",'.',';',':','(',')','[',']','-','<','>','!','¡','?','¿','—')
    sustantivadores = ('ada', 'eda', 'ado', 'ero', 'aje', 'era', 'al', 'ismo', 'ar', 'ista',
                   'ato','azgo', 'azo', 'ancia', 'ez', 'encia','eza', 'dad', 'ismo',
                   'edad', 'ada', 'idad', 'itud', 'tad', 'or', 'ería', 'ada','era', 'ado',
                   'ición', 'aje', 'sión','ante', 'ido', 'ente' ,'amento', 'iente' ,'amiento'
                   'ción', 'imiento', 'ación','dor', 'ura')
    adjetivadores = ('al', 'iento', 'ienta', 'ario', 'aria', 'il', 'ero', 'era', 'ista',
                     'esco','esca','oso', 'osa', 'izo', 'iza','oide', 'able', 'ible',
                     'ante', 'dor','ente', 'iente', 'ivo', 'iva', 'or', 'ano', 'ana', 'ío')
    verbalizadores = ('ar', 'ear', 'ecer', 'izar', 'ar', 'ficar')
    aumentativos = ('ón', 'ona', 'azo', 'aza', 'ote', 'ota', 'udo', 'uda')
    diminutivos = ('ito', 'ita', 'ico', 'ica', 'illo', 'illa', 'ete', 'eta', 'ín', 'ina',
              'ejo', 'eja', 'uelo', 'huela')
    despectivo = ('aco', 'acho', 'acha', 'ajo', 'aja', 'ales', 'alla',
              'ángano', 'ángana', 'ango', 'anga', 'astre', 'astro',
              'astra', 'engue', 'ingo', 'ingue', 'orio', 'orrio',
              'orro', 'orra', 'uco', 'uca', 'ucho', 'ucha', 'ujo',
              'uja', 'ute', 'uza')       
    lista = []        
    lista.append(lemmatizer(palabra)) #LEMMA !!!!!!
    lista.append(1 if palabra in puntuacion else 0) #es puntuacion
    #lista.append(lemmatizer(frase[indice-1])if indice > 0 else ' ') #LEMMA PREVIO!!!!
    #lista.append(lemmatizer(frase[indice+1])if indice<len(frase)-1 else ' ') #LEMMA POSTERIOR!!!!
    lista.append(1 if palabra[0] == palabra[0].upper() else 0) #mayuscula?
    lista.append(1 if indice == len(frase)-1 else 0) #es la última?
    lista.append(1 if indice == 0 else 0) #es la primera?
    
    
    if len(palabra)>3: 
        #ciclo sustantivos
        for i in range(2,8):
            if palabra[-i:] in sustantivadores: 
                lista.append(1)
                break
        if len(lista)<6:
            lista.append(0)
        #ciclo adjetivos
        for i in range(2,6):
            if palabra[-i:] in adjetivadores: 
                lista.append(1)
                break
        if len(lista)<7:
            lista.append(0)
        #ciclo verbos
        for i in range(2,6):
            if palabra[-i:] in verbalizadores: 
                lista.append(1)
                break
        if len(lista)<8:
            lista.append(0)
                       
        lista.append(1 if palabra[-5:] == 'mente' else 0)
       
    
        #ciclo diminutivos: generalmente sustantivos, también ADJ
        for i in range(2,6):
            if palabra[-i:] in diminutivos: 
                lista.append(1)
                break
        if len(lista)<10:
            lista.append(0)
        #ciclo aumentativos: generalmente sustantivos, también ADJ
        for i in range(2,4):
            if palabra[-i:] in aumentativos: 
                lista.append(1)
                break
        if len(lista)<11:
            lista.append(0)
        #ciclo despectivos: generalmente sustantivos, también ADJ
        for i in range(3,7):
            if palabra[-i:] in despectivo: 
                lista.append(1)
                break
        if len(lista)<12:
            lista.append(0)

    else:
        for i in range(7):
            lista.append(0)
        
        
    return tuple(lista)

def lemmatizer(palabra):
    with open('rayo_lemmatizador' , 'rb') as f:
        rl = pickle.load(f)
    try:
        return rl[rl['Form']==palabra].iloc[0,1]
    except:
        return 'No lemma'