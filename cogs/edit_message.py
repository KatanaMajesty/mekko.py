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

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        author = after.author
        before_cont = before.content
        after_cont = after.content
        channel = before.channel
        avatar_author = author.avatar_url
        content = before.content
        if 'https' in content or 'http' in content:
            return
        if author.bot:
            return
        if channel.id == config['edit_message']['id_channel']:
            return
        time = datetime.datetime.now().strftime("%Y.%m.%d в %H.%M")
        channel2 = self.client.get_channel(config['edit_message']['id_channel'])
        embed = discord.Embed(title = f'Редактирование', description = f"Канал: <#{channel.id}>\nАвтор: {author.mention}\n\nСообщение до: `{before_cont}`\nСообщение после: `{after_cont}`", colour=discord.Colour.orange())
        embed.set_footer(text = f"Дата: {time}", icon_url=avatar_author)
        await channel2.send(embed = embed)

def setup(client):
    client.add_cog(User(client))