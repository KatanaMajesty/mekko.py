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

    @commands.command(aliases=['relink', 'link', 'Relink', 'Link'])
    async def mRelink(self, ctx, nick = None, member: discord.Member = None):
        prefix = config["settings"]["prefix"]
        date = datetime.datetime.now().strftime("**%Y.%m.%d** в **%H.%M**")
        role = discord.utils.find(lambda r: r.id == config["settings"]["id_role_moderator"], ctx.guild.roles)
        author = ctx.author

        if role in author.roles:
            if nick is None:
                embed4 = discord.Embed(title='Помощь "Перепривязка"',description=f'Укажи - **[ник] [пользователь]**\nПример: **{prefix}relink _LuK__ @Люк**',colour=discord.Colour.blurple())
                await ctx.send(embed=embed4)
                return
            if member is None:
                await ctx.send('Укажи пользователя!')
                return

            channel = self.client.get_channel(config['settings']['server_console'])
            channelmod = self.client.get_channel(config['settings']['log_moderator'])
            author = ctx.author
            ava_moderator = author.avatar_url
            ava_member = member.avatar_url

            embed = discord.Embed(description=f"Аккаунт пользователя **{member.mention}** перепривязан!\nНик майнкрафт **{nick}** перепривязан на Дискорд аккаунт {member.mention}",colour=discord.Colour.green())
            embed.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            embed2 = discord.Embed(title=f'Перепривязка',description=f"**{member.mention}**, твой аккаунт перепривязан\nНик майнкрафт **{nick}** перепривязан на Дискорд аккаунт {member.mention}",colour=discord.Colour.green())
            embed2.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            embed3 = discord.Embed(title='Логирование',description=f"Аккаунт пользователя **{member.mention}** перепривязан\nНик майнкрафт **{nick}** перепривязан на Дискорд аккаунт {member.mention}\nДата {date}",colour=discord.Colour.green())
            embed3.set_thumbnail(url=ava_member)
            embed3.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            await ctx.send(embed=embed)
            await member.send(embed=embed2)
            await channelmod.send(embed=embed3)
            await channel.send(f'discord link {nick} {member.id}')

        else:
            embed = discord.Embed(description=f'**у вас нет прав!**')
            await ctx.send(embed=embed)



def setup(client):
    client.add_cog(User(client))