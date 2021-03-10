# -*- coding: utf8 -*-
import discord
import datetime
import json
from discord.ext import commands

with open('config.json', 'r') as file:
	config = json.load(file)

class User(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(aliases=['minekick', 'kickmine', 'mkick', 'kickm', 'Kickm', 'Mkick'])
    async def mKick(self, ctx, member: discord.Member = None, *, reason = None):
        prefix = config["settings"]["prefix"]
        channel = self.client.get_channel(config['settings']['server_console'])
        channelmod = self.client.get_channel(config['settings']['log_moderator'])
        date = datetime.datetime.now().strftime("**%Y.%m.%d** в **%H.%M**")
        role = discord.utils.find(lambda r: r.id == config["settings"]["id_role_moderator"], ctx.guild.roles)
        author = ctx.author

        if role in author.roles:
            if member is None:
                embed4 = discord.Embed(title='Помощь "Кик"', description=f'Укажи - **[пользователь] [причина]**\nПример: **{prefix}mkick _LuK__ Спам**', colour = discord.Colour.blurple())
                await ctx.send(embed= embed4)

                return

            if reason is None:
                await ctx.send('Укажи причину!')
                
                return

            ava_moderator = author.avatar_url
            ava_member = member.avatar_url

            embed1 = discord.Embed(title='Логирование',description=f'{member.mention} успешно кикнут с игрового сервера\nПричина: **{reason}**\n Дата кика {date}', colour=discord.Colour.red())
            embed1.set_thumbnail(url=ava_member)
            embed1.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)
            await channelmod.send(embed=embed1)

            embed2 = discord.Embed(title='Кик',description=f'{member.mention}, ты был кикнут с Дискорд и игрового сервера\nПричина: **{reason}**\n Дата кика {date}\nCсылка: https://discord.gg/gJsddSPgfS', colour=discord.Colour.red())
            embed2.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)
            await member.send(embed=embed2)

            embed3 = discord.Embed(title='Кик',description=f'{member.mention} успешно кикнут с игрового сервера\nПричина: **{reason}**', colour=discord.Colour.red())
            embed3.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)
            await ctx.send(embed=embed3)

            await channel.send(f'kick {member.display_name} {reason}')
            await member.kick()

        else:
            embed = discord.Embed(description=f'**у вас нет прав!**')
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(User(client))
