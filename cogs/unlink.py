import discord
import json
import datetime
from discord.ext import commands

with open('config.json', 'r') as file:
	config = json.load(file)

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['unlink', 'Unlink'])
    async def mUnlink(self, ctx, member:discord.Member = None):
        prefix = config["settings"]["prefix"]
        date = datetime.datetime.now().strftime("**%Y.%m.%d** в **%H.%M**")
        role = discord.utils.find(lambda r: r.id == config["settings"]["id_role_moderator"], ctx.guild.roles)
        author = ctx.author

        if role in author.roles:
            if member is None:
                embed4 = discord.Embed(title='Помощь "Отвязка"',description=f'Укажи - **[пользователь]**\nПример: **{prefix}unlink @Люк**',colour=discord.Colour.blurple())
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

            embed = discord.Embed(description=f"Аккаунт пользователя **{member.mention}** отвязан!\nДискорд аккаунт{member.mention} был полностью отвязан!",colour=discord.Colour.green())
            embed.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            embed2 = discord.Embed(title=f'Отвязка',description=f"**{member.mention}**, твой аккаунт отвязан\nДискорд аккаунт {member.mention} был отвязан от аккаунта майнкрафт\n Обратись к модерации",colour=discord.Colour.green())
            embed2.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            embed3 = discord.Embed(title='Логирование',description=f"Аккаунт пользователя **{member.mention}** отвязан\nДискорд аккаунт{member.mention} был отвязан!\nДата {date}",colour=discord.Colour.green())
            embed3.set_thumbnail(url=ava_member)
            embed3.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)

            await ctx.send(embed=embed)
            await member.send(embed=embed2)
            await channelmod.send(embed=embed3)
            await channel.send(f'discord unlink {member.id}')

        else:
            embed = discord.Embed(description=f'**у вас нет прав!**')
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(User(client))