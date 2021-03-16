import discord
from discord.ext import commands

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx, amount = 10):
        await ctx.message.channel.purge(limit = 1)
        try:
            if amount > 100:
                await ctx.send('`Указанное значение больше 100!`', delete_after=3)
                return
            await ctx.message.channel.purge(limit = amount)
            await ctx.send(f"`Было очищенно сообщений: {amount}`", delete_after=3)
       
        except:
            embed = discord.Embed(title='Ошибка!',description=f'У тебя нет прав!', colour= discord.Color.red())
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(User(client))