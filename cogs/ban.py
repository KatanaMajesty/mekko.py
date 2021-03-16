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

    @commands.command(aliases=['mineban', 'banmine', 'ban', 'banm', 'Banm', 'Mban'])
    async def mBan(self, ctx, member:discord.Member = None, *, reason = None):
        prefix = config["settings"]["prefix"]
        role = discord.utils.find(lambda r: r.id == config["settings"]["id_role_moderator"], ctx.guild.roles)
        author = ctx.author

        if role in author.roles:
            if member is None:
                embed4 = discord.Embed(title='Помощь "Бан"', description=f'Укажи - **[пользователь] [причина]**\nПример: **{prefix}mban @Люк Читер**', colour = discord.Colour.blurple())
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
            joined = member.joined_at.timestamp()
            guildtime = int((datetime.datetime.now().timestamp() - joined) / (60 * 60 * 24))
            date = datetime.datetime.now().strftime("**%Y.%m.%d** в **%H.%M**")

            embed = discord.Embed(description=f"**{member.mention}** заблокирован в Дискорд и игре!\nПричина: {reason}", colour=discord.Colour.red())
            embed.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            embed2 = discord.Embed(title = f'Блокировка', description=f"{member.mention}, ты получил блокировку в Дискорд и игровом сервере!\nПричина: {reason}\nЕсли это ошибка либо вы хотите обговорить снятие блокировки свяжитесь с **Люк#3989**", colour=discord.Colour.red())
            embed2.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            embed3 = discord.Embed(title ='Логирование',description=f"**{member.mention}** получил блокировку в Дискорд и игре!\nПричина: {reason}\n Дата блокировки {date}\nОн играл на сервере **{guildtime}** дня",colour=discord.Colour.red())
            embed3.set_thumbnail(url=ava_member)
            embed3.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            await ctx.send(embed=embed)
            await member.send(embed=embed2)
            await channelmod.send(embed=embed3)
            await channel.send(f'ban-ip {member.display_name} {reason}')
            await member.ban(reason=reason)

        else:
            embed = discord.Embed(description=f'**у вас нет прав!**')
            await ctx.send(embed=embed)

    @commands.command(aliases=['mineunban', 'unbanmine', 'munban', 'unbanm', 'Unbanm', 'Munban'])
    async def mUnban(self, ctx, id = None, *, nick = None):
        channel = self.client.get_channel(config['settings']['server_console'])
        channelmod = self.client.get_channel(config['settings']['log_moderator'])
        prefix = config["settings"]["prefix"]
        date = datetime.datetime.now().strftime("**%Y.%m.%d** в **%H.%M**")
        role = discord.utils.find(lambda r: r.id == config["settings"]["id_role_moderator"], ctx.guild.roles)
        author = ctx.author

        if role in author.roles:
            if id is None:
                embed4 = discord.Embed(title='Помощь "Разбан"', description=f'Укажи - **[id] [ник]**\nПример: **{prefix}munban 783276328632836 _LuK__**', colour = discord.Colour.blurple())
                await ctx.send(embed=embed4)
                return
            if nick is None:
                await ctx.send('Укажи ник!')
                return

            ava_moderator = author.avatar_url
            user = await self.client.fetch_user(id)

            embed = discord.Embed(description=f"**<@{id}>** блокировка снята в Дискорд и игре\nНик **{nick}**, пользователь **<@{id}>**", colour=discord.Colour.red())
            embed.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            embed3 = discord.Embed(title ='Логирование',description=f"**<@{id}>** блокировка снята в Дискорд и игре!\nДата снятия блокировки {date}",colour=discord.Colour.red())
            embed3.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            await ctx.send(embed=embed)
            await channelmod.send(embed=embed3)
            await channel.send(f'unban {nick}')
            await channel.send(f'discord link {nick} {id}')
            await ctx.guild.unban(user)

        else:
            embed = discord.Embed(title='Ошибка!',description=f'У тебя нет прав!', colour= discord.Color.red())
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(User(client))