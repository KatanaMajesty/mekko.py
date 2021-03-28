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

    @commands.Cog.listener()
    async def on_message(self, message):
        content = message.content
        if '<@!227117061011144704>' in content or '<@!385425624082284544>' in content or '<@!743039233484259338>' in content:
            await message.add_reaction("💖")

    """@commands.Cog.listener()
    async def on_command_error(self, ctx, error): 
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'Команда не найдена!')
        #if isinstance(error, commands.CommandInvokeError):
            #await ctx.send(f'Ошибка!')
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f'Указанный пользователь не найден!')"""
            
def setup(client):
    client.add_cog(User(client))
