import discord
from discord.ext import commands
import json

with open('config.json', 'r') as file:
	config = json.load(file)
    
prefix = config["settings"]["prefix"]
class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def commands(self, ctx):
        embed = discord.Embed(description = f"`{prefix}commands` - список команд \n`{prefix}ban @user причина` - бан игрока\n`{prefix}mute @user time(10h, 2d) причина` - мут игрока\n`{prefix}unmute @user` - снять мут с игрока\n`{prefix}clear (число сообщений)` - удалить сообщение в чате", colour = discord.Colour.light_gray())
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(User(client))