import discord 
from discord.ext import commands

async def secretT(lista_tokens,message,client):
    if ('mejor' in message.content.lower()) and ('clase' in message.content.lower()):
        img='https://lh3.googleusercontent.com/pw/AM-JKLW1lyeeM_hitJnEhnHupmQQ9eIkSjt3W_6aIwiPWomgliBwa7OXX7a19MJRAZT4M3yEkBKkJjQCjoavF983jM10z-tp-eXwBj6w5YSxtnVNrAM1nnNfPYKe3fmsYatwAVWqRwkP4beXAmq7MG2W42g=w1024-h768-no'

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_image(url=img)
        msg='Mi mejor clase? No tengo duda:'

        await message.channel.send(msg)
        await message.channel.send(embed=embed)

    if ('musica pop en español' in message.content.lower()) or ('música pop en español' in message.content.lower()):
        msg='Lo primero es lo primero'

        await message.channel.send(msg)

    if ('idbootcamps' in message.content.lower()) or ('elmo' in message.content.lower()) or ('bootcamp' in message.content.lower()) or ('alumno' in message.content.lower()):
        img='https://lh3.googleusercontent.com/wm3ntqbaUT68lWVCicxJI5_pACBLMuZ2RwMREt2DW3Fsd1bL6QX7DQlHc4tVfyoNTkfd9VunULN-65GlzzAaPVFH4oJXpnubc0UOC5aDMo1Zfs-NjXUy8ufy8PTGcqMij2UIhN0GI9Y70p5CS14M6_2v-MWQsmsW2rauRJly-VYIxbLmsTJBjqZuCCeBJm5YS7hqY8DqNtiRY1gr_bkus4GOhQ946HnPzmKO-LUJYC1lM_KtzFkU4PZ1wMPGg1Efwb6p1JaSSeqrfbKL3934DgPHjgK8-Rbru17o7meQcggUv-j7z2W_Xq3jLlm-7F5rH3Cj9iVlTRcBqL8J44CZO_anJrtN-OL-QO5hQ7M_Sq-hfgCVzJIXoEq-8C0_x9dacHZtVFkS0lAkPmekYEkj5KeN2EnTYsDfGdrQx2u12VlQgLqWiKNVgOqAaa6eEaCY_9ROTNlwEFPiwGy9fTlUU8fsHEpYoTmSm8gU7Phtk5l5jZTdXH3OJ9WgRr94CTYFJKzMj_9hcfAD71hoaDgDt0dIQgO0_cvrPoGb49T_zLJYhE2BnQlO4a2gNS3VHl7dWYwYsEHdQjIDxvlXjX6MtVh5QbbSawh6WFXgnrtCKBd8xA_47-_c00awqIJ0Ns6_oh0eCUbvLba1initi-BhjZVK1SOti4EaeyPre-o-GjwJmIzTvK9jjzhqNLBRpKhREs9ygNMlTlR5_2JuMFoZhQ=w500-h426-no?authuser=1'
        msg='Por cierto chicos, tenemos un alumno nuevo en el bootcamp. Sed buenos con él'

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_image(url=img)

        await message.channel.send(msg)
        await message.channel.send(embed=embed)
