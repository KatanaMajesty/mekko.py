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

        try:
            bot = self.client.get_user(config["settings"]["id"])
            if author == bot:
                return
            if channel.id == config['edit_message']['id_channel']:
                return
            time = datetime.datetime.now().strftime("%Y.%m.%d в %H.%M")
            channel2 = self.client.get_channel(config['edit_message']['id_channel'])
            embed = discord.Embed(title = f'Сообщение изменено', description = f"Канал: `{channel}`\nАвтор:{author.mention}\n\nСообщение было: `{before_cont}`\nСообщение стало: `{after_cont}`", colour=discord.Colour.orange())
            embed.set_footer(text = f"Дата: {time}")
            await channel2.send(embed = embed)
            
        except:
            return

def setup(client):
    client.add_cog(User(client))