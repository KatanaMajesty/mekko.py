# -*- coding: utf8 -*-
import discord
import json
import datetime
from discord.ext import commands

with open('config.json', 'r') as file:
	config = json.load(file)

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['warn', 'Warn'])
    async def mWarn(self, ctx, member:discord.Member = None, *, reason = None):
        prefix = config["settings"]["prefix"]
        role = discord.utils.find(lambda r: r.id == config["settings"]["id_role_moderator"], ctx.guild.roles)
        author = ctx.author
        if role in author.roles:
            if member is None:
                embed4 = discord.Embed(title='Помощь "Варн"', description=f'Укажи - **[пользователь] [причина]**\nПример: **{prefix}mwarn @Люк Построил минато**', colour = discord.Colour.blurple())
                await ctx.send(embed=embed4)
                return
            if reason is None:
                await ctx.send('Укажи причину!')
                return

            channel = self.client.get_channel(config['settings']['server_console'])
            channelmod = self.client.get_channel(config['settings']['log_moderator'])
            author = ctx.author
            ava_moderator = author.avatar_url
            ava_member = member.avatar_url
            date = datetime.datetime.now().strftime("**%Y.%m.%d** в **%H.%M**")

            embed = discord.Embed(description=f"**{member.mention}** предупреждён в игре!\nПричина: {reason}", colour=discord.Colour.red())
            embed.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            embed2 = discord.Embed(title = f'Предупреждение', description=f"{member.mention}, ты получил предупреждение на игровом сервере!\nПричина: {reason}\nЕсли это ошибка свяжитесь с **Люк#3989**", colour=discord.Colour.red())
            embed2.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            embed3 = discord.Embed(title ='Логирование',description=f"**{member.mention}** получил предупреждение в игре!\nПричина: {reason}\n Дата предупреждения {date}",colour=discord.Colour.red())
            embed3.set_thumbnail(url=ava_member)
            embed3.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            await ctx.send(embed=embed)
            await member.send(embed=embed2)
            await channelmod.send(embed=embed3)
            await channel.send(f'warn {member.display_name} {reason}')
        else:
            embed = discord.Embed(title='Ошибка!',description=f'У тебя нет прав!', colour= discord.Color.red())
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(User(client))