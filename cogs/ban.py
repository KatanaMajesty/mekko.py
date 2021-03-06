import discord
import json
from discord.ext import commands

with open('config.json', 'r') as file:
	config = json.load(file)

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx, member: discord.Member, *, reason = "не указана"):
        await ctx.message.channel.purge(limit = 1)
        
        try:
            channel_console = self.client.get_channel(config["settings"]["server_console"])
            autor = ctx.message.author 

            await channel_console.send(f"ban-ip {member.name} {reason}")

            await member.ban(reason = reason)

            embed = discord.Embed(description = f"{member.mention} был заблокирован на сервере!\n**Причина:** {reason}", colour=discord.Colour.red())
            embed.set_footer(text = f"Осудил: {autor}")
            await ctx.send(embed = embed)

        except:
            return

def setup(client):
    client.add_cog(User(client))