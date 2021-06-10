# -*- coding: utf8 -*-
import discord
from discord import colour
from discord.embeds import EmbedProxy
from discord.ext import commands, tasks
from discord.utils import get
from discord_components import *
import asyncio
import random
from random import *


class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["tictac","tic","крестики","нолики","крестики_нолики","крестикинолики","гомуку","кн","тик","так","тиктак","тик_так"])
    async def tictactoe(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        try:
            if member is None:
                embed = discord.Embed(description = f"Укажи соперника для игры!", colour=discord.Color.red())
                embed.set_author(name="Ошибка!")
                await ctx.send(embed=embed, delete_after=5)
                return
            if ctx.author.id == member.id:
                embed = discord.Embed(description = f"Вы не можете играть сами с собой!", colour=discord.Color.red())
                embed.set_author(name="Ошибка!")
                await ctx.send(embed=embed, delete_after=5)
                return
            if member.bot:
                embed = discord.Embed(description = f"Вы не можете играть с ботом!", colour=discord.Color.red())
                embed.set_author(name="Ошибка!")
                await ctx.send(embed=embed, delete_after=5)
                return

            com = [[Button(style = ButtonStyle.green, label = 'Да', id = "0"),Button(style = ButtonStyle.red, label = 'Нет', id = "1")]]

            embed = discord.Embed(description = f"Пользователь {ctx.author.mention} приглашает вас поиграть!\nДля принятия приглашения у вас есть 3 минуты", colour=discord.Colour.from_rgb(47,49,54)) 
            embed.set_author(name="Крестики-Нолики⁣ ⁣⁣ ⁣   ⁣⁣⁣ ⁣   ⁣      ")
            msg = await ctx.send(f"{ctx.author.mention} | {member.mention}", embed=embed,components = com)

            res = await self.client.wait_for("button_click", check = lambda res: res.author.id == member.id and res.message.id == msg.id, timeout=180)
            if res.component.label == 'Нет':
                com_2 = []
                embed = discord.Embed(description = f"Приглашение от {ctx.author.mention} отклонено!", colour=discord.Colour.from_rgb(47,49,54)) 
                embed.set_author(name="Крестики-Нолики⁣ ⁣⁣ ⁣   ⁣⁣⁣ ⁣   ⁣      ")
                await msg.edit(" ", embed=embed, components = com_2)
                return
            if res.component.label == 'Да':
                await res.respond(type=InteractionType.DeferredUpdateMessage ,content = f"fdgdfgdf")
                try:
                    player1 = choice([ctx.author, member])
                    if player1 == ctx.author:
                        player2 = member
                    else:
                        player2 = ctx.author

                    player_1 = player1.id
                    player_2 = player2.id

                    win = 0 # 1 - победа хоста, 2 - победа противника. 4 (или 5, не помню) - ничья
                    move = 1 # этот статус чей ход
                    global q
                    q = 0 #это штука для блокировки ячеек, перестраховка так сказать, ну и для остановки цикла проверки

                    components = [
                        [Button(style = ButtonStyle.gray, label = ' ', id = "00"),
                        Button(style = ButtonStyle.gray, label = ' ', id = "01"),
                        Button(style = ButtonStyle.gray, label = ' ', id = "02")],
                        [Button(style = ButtonStyle.gray, label = ' ', id = "10"),
                        Button(style = ButtonStyle.gray, label = ' ', id = "11"),
                        Button(style = ButtonStyle.gray, label = ' ', id = "12")],
                        [Button(style = ButtonStyle.gray, label = ' ', id = "20"),
                        Button(style = ButtonStyle.gray, label = ' ', id = "21"),
                        Button(style = ButtonStyle.gray, label = ' ', id = "22")]] # само поле для клкточек
                    d = [[0,0,0],[0,0,0],[0,0,0]] # статус клеток. 0 - пустая, 1 - нолик, 2 - крестик.
                    
                    embed = discord.Embed(description = f"Ход - {player1.mention}", colour=discord.Colour.from_rgb(47,49,54)) 
                    embed.set_author(name="Крестики-Нолики⁣ ⁣⁣ ⁣   ⁣⁣⁣ ⁣   ⁣      ")
                    await msg.edit(" ",embed=embed, components = components)
                    
                    while q != 3:

                        global blocking
                        def blocking(win, d, components, q):  #это функция для блокировки пустых ячеек, кстати вообще моя первая функция старндартная в пайтоне!!
                            if win != 0:
                                while 0 in d[0] or 0 in d[1] or 0 in d[2]:
                                    if 0 in d[0]:
                                        c0 = d[0].index(0)           
                                        components[0][c0] = Button(style = ButtonStyle.gray, label = ' ', id = 0, disabled=True)
                                        d[0][c0] = 3
                                        if 0 not in d[0]:
                                            q = q + 1
                                    if 0 in d[1]:
                                        c1 = d[1].index(0)
                                        components[1][c1] = Button(style = ButtonStyle.gray, label = ' ', id = 0, disabled=True)
                                        d[1][c1] = 3
                                        if 0 not in d[1]:
                                            q = q + 1
                                    if 0 in d[2]:
                                        c2 = d[2].index(0)
                                        components[2][c2] = Button(style = ButtonStyle.gray, label = ' ', id = 0, disabled=True)
                                        d[2][c2] = 3
                                        if 0 not in d[2]:
                                            q = q + 1
                                            
                        if move == 1: #ход 1 (нолик)
                            res = await self.client.wait_for("button_click", check = lambda res: res.author.id == player_1 and res.message.id == msg.id, timeout=180)
                            if res.user.id != player_1:
                                await res.respond(type=InteractionType.DeferredUpdateMessage ,content = f"fdgdfgdf")
                                return
                            id = res.component.id
                            components[int(id[0])][int(id[1])] = Button(style = ButtonStyle.red, label = '◯', id = str(id[0]) + str(id[1]), disabled=True)
                            d[int(id[0])][int(id[1])] = 1
                            embed = discord.Embed(description = f"Ход - {player1.mention}", colour=discord.Colour.from_rgb(47,49,54))
                            embed.set_author(name="⁣⁣⁣⁣Крестики-Нолики⁣ ⁣⁣ ⁣   ⁣⁣⁣ ⁣   ⁣      ")
                            await res.respond(type=InteractionType.DeferredUpdateMessage ,content = f"fdgdfgdf")
                            await msg.edit(" ",embed=embed, components = components)
                            move = 2

                            global embed1
                            embed1 = discord.Embed(description = f"Выиграл - {player1.mention}", colour=discord.Colour.from_rgb(47,49,54))
                            embed1.set_author(name="⁣Крестики-Нолики⁣ ⁣⁣ ⁣   ⁣⁣⁣ ⁣   ⁣      ")

                            if d[0][0] == 1 and d[0][1] == 1 and d[0][2] == 1:
                                win = 1
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed1, components = components)
                                return 
                            if d[1][0] == 1 and d[1][1] == 1 and d[1][2] == 1:
                                win = 1
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed1, components = components)
                                return 
                            if d[2][0] == 1 and d[2][1] == 1 and d[2][2] == 1:
                                win = 1
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed1, components = components)
                                return 
                            if d[0][0] == 1 and d[1][0] == 1 and d[2][0] == 1:
                                win = 1
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed1, components = components)
                                return 
                            if d[0][1] == 1 and d[1][1] == 1 and d[2][1] == 1:
                                win = 1
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed1, components = components)
                                return 
                            if d[0][2] == 1 and d[1][2] == 1 and d[2][2] == 1:
                                win = 1
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed1, components = components)
                                return 
                            if d[0][0] == 1 and d[1][1] == 1 and d[2][2] == 1:
                                win = 1
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed1, components = components)
                                return 
                            if d[0][2] == 1 and d[1][1] == 1 and d[2][0] == 1:
                                win = 1
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed1, components = components)
                                return 
                            if d[0][0] != 0 and d[0][1] != 0 and d[0][2] != 0 and d[1][0] != 0 and d[1][1] != 0 and d[1][2] != 0 and d[2][0] != 0 and d[2][1] != 0 and d[2][2] != 0:
                                embed = discord.Embed(description = f"⁣⁣⁣**Ничья!**⁣⁣⁣", colour=discord.Colour.from_rgb(47,49,54))
                                embed.set_author(name="Крестики-Нолики⁣ ⁣⁣ ⁣   ⁣⁣⁣ ⁣   ⁣      ")
                                await msg.edit(" ",embed=embed, components = components)
                                win = 5
                                return
                            

                        if move == 2: #ход 2 (крестик)
                            res = await self.client.wait_for("button_click", check = lambda res: res.author.id == player_2 and res.message.id == msg.id, timeout=180)
                            if res.user.id != player_2:
                                await res.respond(type=InteractionType.DeferredUpdateMessage ,content = f"fdgdfgdf")
                                return
                            id = res.component.id
                            components[int(id[0])][int(id[1])] = Button(style = ButtonStyle.blue, label = '✘', id = str(id[0]) + str(id[1]), disabled=True)
                            d[int(id[0])][int(id[1])] = 2
                            embed = discord.Embed(description = f"Ход - {player2.mention}", colour=discord.Colour.from_rgb(47,49,54))
                            embed.set_author(name="Крестики-Нолики⁣ ⁣⁣ ⁣   ⁣⁣⁣ ⁣   ⁣      ")
                            await msg.edit(" ",embed=embed, components = components)
                            await res.respond(type=InteractionType.DeferredUpdateMessage ,content = f"fdgdgdf")
                            move = 1
                    
                            global embed2
                            embed2 = discord.Embed(description = f"Выиграл - {player2.mention}", colour=discord.Colour.from_rgb(47,49,54))
                            embed2.set_author(name="Крестики-Нолики⁣ ⁣⁣ ⁣   ⁣⁣⁣ ⁣   ⁣      ")

                            if d[0][0] == 2 and d[0][1] == 2 and d[0][2] == 2:
                                win = 2
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed2, components = components)
                                return 
                            if d[1][0] == 2 and d[1][1] == 2 and d[1][2] == 2:
                                win = 2
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed2, components = components)
                                return 
                            if d[2][0] == 2 and d[2][1] == 2 and d[2][2] == 2:
                                win = 2
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed2, components = components)
                                return 
                            if d[0][0] == 2 and d[1][0] == 2 and d[2][0] == 2:
                                win = 2
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed2, components = components)
                                return 
                            if d[0][1] == 2 and d[1][1] == 2 and d[2][1] == 2:
                                win = 2
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed2, components = components)
                                return 
                            if d[0][2] == 2 and d[1][2] == 2 and d[2][2] == 2:
                                win = 2
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed2, components = components)
                                return 
                            if d[0][0] == 2 and d[1][1] == 2 and d[2][2] == 2:
                                win = 2
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed2, components = components)
                                return 
                            if d[0][2] == 2 and d[1][1] == 2 and d[2][0] == 2:
                                win = 2
                                blocking(win, d, components, q)
                                await msg.edit(" ",embed=embed2, components = components)
                                return 
                            if d[0][0] != 0 and d[0][1] != 0 and d[0][2] != 0 and d[1][0] != 0 and d[1][1] != 0 and d[1][2] != 0 and d[2][0] != 0 and d[2][1] != 0 and d[2][2] != 0:
                                embed = discord.Embed(description = f"**Ничья!**⁣⁣⁣", colour=discord.Colour.from_rgb(47,49,54))
                                embed.set_author(name="Крестики-Нолики⁣ ⁣⁣ ⁣   ⁣⁣⁣ ⁣   ⁣      ")
                                await msg.edit(" ",embed=embed, components = components)
                                win = 5
                                return

                except asyncio.TimeoutError: #если время вышло
                    while 0 in d[0] or 0 in d[1] or 0 in d[2]:
                        if 0 in d[0]:
                            c0 = d[0].index(0)           
                            components[0][c0] = Button(style = ButtonStyle.gray, label = ' ', id = 0, disabled=True)
                            d[0][c0] = 3
                            if 0 not in d[0]:
                                q = q + 1
                        if 0 in d[1]:
                            c1 = d[1].index(0)
                            components[1][c1] = Button(style = ButtonStyle.gray, label = ' ', id = 0, disabled=True)
                            d[1][c1] = 3
                            if 0 not in d[1]:
                                q = q + 1
                        if 0 in d[2]:
                            c2 = d[2].index(0)
                            components[2][c2] = Button(style = ButtonStyle.gray, label = ' ', id = 0, disabled=True)
                            d[2][c2] = 3
                            if 0 not in d[2]:
                                q = q + 1
                        if q == 3:
                            embed = discord.Embed(description = f"⁣**Время вышло!**⁣", colour=discord.Colour.from_rgb(47,49,54))
                            embed.set_author(name="Крестики-Нолики⁣ ⁣⁣ ⁣   ⁣⁣⁣ ⁣   ⁣      ")
                            await msg.edit(" ",embed=embed, components = components)
                            return
        except asyncio.TimeoutError: 
            com_2 = []
            embed = discord.Embed(description = f"Время для принятия приглашения от {ctx.author.mention} вышло!", colour=discord.Colour.from_rgb(47,49,54)) 
            embed.set_author(name="Крестики-Нолики⁣ ⁣⁣ ⁣   ⁣⁣⁣ ⁣   ⁣      ")
            await msg.edit(" ", embed=embed, components = com_2)
            return


def setup(client):
    client.add_cog(User(client))
    