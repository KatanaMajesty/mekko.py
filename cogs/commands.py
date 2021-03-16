import discord
from discord.ext import commands
import json

with open('config.json', 'r') as file:
	config = json.load(file)
    
prefix = config["settings"]["prefix"]
class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['helpmod', 'commands'])
    async def modhelp(self, ctx):
        role = discord.utils.find(lambda r: r.id == config["settings"]["id_role_moderator"], ctx.guild.roles)
        author = ctx.author
        guild = ctx.guild
        ava = guild.icon_url
        if role in author.roles:
            embed = discord.Embed(title='Команды модерации',description = f"`{prefix}ban` - блокировка пользователя\n`{prefix}mute` - выдаёт мут пользователю\n`{prefix}kick` - кикает пользователя\n`{prefix}warn` - выдаёт предупреждение пользователю\n`{prefix}reacc` - смена аккаунта Майнкрафт\n`{prefix}unlink` - отвязывает пользователя\n`{prefix}relink` - смена Дискорд аккаунта\n`{prefix}clear` - очистка\n\nПодробную информацию о командах ты можешь \nузнать введя нужную команду - **'{prefix}mute'**", colour = discord.Colour.blurple())
            embed.set_thumbnail(url=ava)
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title='Ошибка!',description=f'У тебя нет прав!', colour= discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(aliases=['команды', 'Help'])
    async def help(self, ctx):
        guild = ctx.guild
        ava = guild.icon_url
        embed = discord.Embed(title='Список команд',description = f"`{prefix}server` - информация о серверах\n`{prefix}player [ник]` - информация об игроке\n`{prefix}skin [ник]` - скин игрока\n`{prefix}member [участник]` - информация об участнике\n`{prefix}ava [участник]` - аватарка участника", colour = discord.Colour.blurple())
        embed.set_thumbnail(url=ava)
        await ctx.send(embed = embed)



def setup(client):
    client.add_cog(User(client))