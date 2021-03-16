# -*- coding: utf8 -*-
import discord
from discord.ext import commands
from discord.ext.commands import MemberNotFound

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['Ава', 'аватарка', 'Ava', 'ava', 'аватар', 'ава'])
    async def avatar(self, ctx, *, member: discord.Member = None):
        author = ctx.message.author
        emoji = discord.utils.get(ctx.message.guild.emojis, name='m2_cateeee')
        channel = ctx.message.channel
        try:

            if member is None:
                author_avatar = author.avatar_url
                embedVar = discord.Embed(description=f'{emoji}  Ваша аватарка, **{author.display_name}**', colour=discord.Colour.blurple())
                embedVar.set_image(url=f'{author_avatar}')
                await channel.send(embed=embedVar)

            else:
                avatar = member.avatar_url
                embedVar = discord.Embed(description=f'{emoji}  Аватарка пользователя **{member.display_name}**', colour=discord.Colour.blurple())
                embedVar.set_image(url=f'{avatar}')
                await channel.send(embed=embedVar)
                
        except:
            return


def setup(client):
    client.add_cog(User(client))