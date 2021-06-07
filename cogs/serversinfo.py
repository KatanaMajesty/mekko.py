# -*- coding: utf8 -*-
import discord
import json
from discord.ext import commands
import time



with open('config.json', 'r') as file:
	config = json.load(file)

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['info', 'Info','сервер','server'])
    async def MInfo(self, ctx):
        urv = ctx.guild.icon_url
        embed = discord.Embed(title='Информация о сервере',description=f'**• Дискорд сервер**\nНазвание **{ctx.guild.name}**\nСоздан {ctx.guild.created_at.strftime("**%Y.%m.%d** в **%H:%M**")}\nВсего **{ctx.guild.member_count}** участников\n\n**• Игровой сервер**\nСтатус: **Закрыт навсегда**',colour=discord.Colour.blurple())
        embed.set_thumbnail(url=urv)
        await ctx.send(embed=embed)
        return




def setup(client):
    client.add_cog(User(client))
