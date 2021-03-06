import discord
from discord.ext import commands

class User(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):    
        activity= discord.Streaming(name="на сервере Chimekko!", url="https://www.youtube.com/watch?v=2QxvFAiYDJs&t=976s")
        await self.client.change_presence(activity=activity)
        print("Бот готов")

def setup(client):
    client.add_cog(User(client))