# Para gráficas
import numpy as np
from numpy import sin, cos, tan, arcsin, arccos, arctan, hypot, arctan2, degrees, radians, sinh, cosh, tanh, arcsinh, arccosh, arctanh, exp, log, log10, log2 
import matplotlib.pyplot as plt
import math

def grapher(mensaje):
    
    y=mensaje.content.split('=')[1]

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

    return file, embed
    #await message.channel.send(file=file, embed=embed)