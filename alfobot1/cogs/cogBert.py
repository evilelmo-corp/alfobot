#Cog Bert - Integración
import discord 
from discord.ext import commands
from cogs import modeloBert



class CogBert(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.client.user:
        	intencion=modeloBert.rayo_sesamo(message.content)
        	await message.channel.send(str(intencion))


def setup(client):
    client.add_cog(CogBert(client))