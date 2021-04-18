# -*- coding: utf8 -*-
import discord
import json
from discord.ext import commands
import minestat
import time
import requests



with open('config.json', 'r') as file:
	config = json.load(file)

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['info', 'Info','сервер','server'])
    async def MInfo(self, ctx):
        ms1 = minestat.MineStat('138.201.182.132', 25565)
        if ms1.online:
            ip = 'join.chimekko.site'

            url2 = f'https://minecraft-statistic.net/api/server/info/138.201.182.132_25565/'
            response = requests.get(url2)
            list = response.json()["info"]["players_list"]

            online = response.json()["info"]["players"]
            list_count = int(online) - int(len(list)) 
        

            if online == 12:
                count = '.'
            elif online < 12:
                count = '.'
            elif online > 12:
                count = f' и ещё {list_count} игроков'
            
    

            ms = minestat.MineStat('138.201.182.132', 25565)
            urv = ctx.guild.icon_url
            embed = discord.Embed(title='Информация о сервере',description=f'''**• Дискорд сервер**\nНазвание **{ctx.guild.name}**\nСоздан {ctx.guild.created_at.strftime('**%Y.%m.%d** в **%H:%M**')}\nВсего **{ctx.guild.member_count}** участников\n\n**• Игровой сервер**\nСтатус: **Онлайн**\nСейчас онлайн **{online}/{ms.max_players}**\nИгроки на сервере: **`{str(list).replace("[","").replace("]","").replace("'","")}{count}`**\nIP сервера - **{ip}**\nЯдро и версия **{ms.version}**''',colour=discord.Colour.blurple())
            embed.set_thumbnail(url=urv)
            embed.set_footer(text='Данные взяты с "minecraft-statistic.net" и могут быть не точными')
            await ctx.send(embed=embed)
            return
        else:
            urv = ctx.guild.icon_url
            embed = discord.Embed(title='Информация о сервере',description=f'**• Дискорд сервер**\nНазвание **{ctx.guild.name}**\nСоздан {ctx.guild.created_at.strftime("**%Y.%m.%d** в **%H:%M**")}\nВсего **{ctx.guild.member_count}** участников\n\n**• Игровой сервер**\nСтатус: **Закрыт**',colour=discord.Colour.blurple())
            embed.set_thumbnail(url=urv)
            await ctx.send(embed=embed)



def setup(client):
    client.add_cog(User(client))
