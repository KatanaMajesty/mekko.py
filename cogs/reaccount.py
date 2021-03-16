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

    @commands.command(aliases=['reacc', 'acc', 'Acc', 'Reacc'])
    async def mReacc(self, ctx, nick1 = None, nick2 = None ,member: discord.Member = None):
        prefix = config["settings"]["prefix"]
        date = datetime.datetime.now().strftime("**%Y.%m.%d** в **%H.%M**")
        role = discord.utils.find(lambda r: r.id == config["settings"]["id_role_moderator"], ctx.guild.roles)
        author = ctx.author

        if role in author.roles:
            if nick1 is None:
                embed4 = discord.Embed(title='Помощь "Перепривязка"', description=f'Укажи - **[старый ник] [новый ник][пользователь]**\nПример: **{prefix}reacc luke65 _LuK__ @Люк**',colour=discord.Colour.blurple())
                await ctx.send(embed=embed4)
                return
            if nick2 is None:
                embed4 = discord.Embed(title='Помощь "Перепривязка"', description=f'Укажи - **[ник] [пользователь]**\nПример: **{prefix}relink _LuK__ @Люк**', colour=discord.Colour.blurple())
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

            embed = discord.Embed(description=f"Аккаунт пользователя **{member.mention}** отредактирован:\nСтарый ник - **{nick1}**, новый ник - **{nick2}**",colour=discord.Colour.green())
            embed.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            embed2 = discord.Embed(title=f'Перепривязка',description=f"*{member.mention}**, твой аккаунт отредактирован:\nСтарый ник - **{nick1}**, новый ник - **{nick2}**\nУдачной игры :smiling_face_with_3_hearts: \n*Обратись к модерации в случае ошибки!*",colour=discord.Colour.green())
            embed2.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            embed3 = discord.Embed(title='Логирование',description=f"Аккаунт пользователя **{member.mention}** отредактирован:\nСтарый ник - **{nick1}**, новый ник - **{nick2}**\nДата {date}",colour=discord.Colour.green())
            embed3.set_thumbnail(url=ava_member)
            embed3.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)
            
            await ctx.send(embed=embed)
            await member.send(embed=embed2)
            await channelmod.send(embed=embed3)
            await channel.send(f'discord unlink {member.id}')
            await channel.send(f'whitelist remove {nick1}')
            await channel.send(f'whitelist add {nick2}')
            await channel.send(f'discord link {nick2} {member.id}')

        else:
            embed = discord.Embed(title='Ошибка!',description=f'У тебя нет прав!', colour= discord.Color.red())
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(User(client))