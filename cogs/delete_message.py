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
    async def on_message_delete(self, message):
        author = message.author
        content = message.content
        channel = message.channel
        bot = self.client.get_user(config["settings"]["id"])
        try:
            if author == bot:
                return
            if content[0] == config["settings"]["prefix"]:
                return
            if channel.id == config['del_message']['id_channel']:
                return
            if channel.id == config['application']['id_channel_1']:
                return
            time = datetime.datetime.now().strftime("%Y.%m.%d в %H.%M")
            channel2 = self.client.get_channel(config['del_message']['id_channel'])
            embed = discord.Embed(title = f'Сообщение удалено', description = f"Канал: `{channel}`\nАвтор:{author.mention}\n\nСообщение: `{content}`", colour=discord.Colour.red())
            embed.set_footer(text = f"Дата: {time}")
            await channel2.send(embed = embed)
        
        except:
            return
def setup(client):
    client.add_cog(User(client))