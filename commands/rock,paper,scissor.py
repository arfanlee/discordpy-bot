import discord
from discord.ext import commands
import asyncio
import random
import json
from getdatabase import connect

records = connect()

userhand = ""

def findUser(userID):
    return records.find_one({'userID':userID})

def addNewPlayer(userID):
    # Values to be appended
    newPlayer = {
                    "userID": userID,
                    "rpsWin": 0,
                    "rpsLose": 0
                }
    # appending new player into database
    records.insert_one(newPlayer)

def addWin(userID):
    player = findUser(userID)
    currentWin = player['rpsWin'] # We want the user's total win value only
    new_value = currentWin + 1
    user_update = {'rpsWin': new_value}
    records.update_one({'userID': userID},{'$set':user_update})

def addLose(userID):
    player = findUser(userID)
    currentLose = player['rpsLose'] # We want the user's total lose value only
    new_value = currentLose + 1
    user_update = {'rpsLose': new_value}
    records.update_one({'userID': userID},{'$set':user_update})

async def play(self,ctx,member,userID):
    rock = '✊🏽'
    paper = '🖐🏽'
    scissor = '✌🏽'
    hand = [rock,paper,scissor]

    game = await ctx.send('Choose your weapon.')

    # Adding bot's reaction to the message
    for line in hand:
        bothand = random.choice(hand)
        await game.add_reaction(line)

    def check(reaction, user):
        global userhand
        userhand = str(reaction.emoji) # Getting the users weapon from reaction button
        return user == ctx.author and userhand in hand

    try:
        await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Woops, too slow!')
        await game.delete()
    else:
        await game.delete()
        if bothand == rock:
            if userhand == rock:
                await ctx.send(f'{userhand}🆚{bothand}')
                await ctx.send("It's a draw!")
            if userhand == paper:
                await ctx.send(f'{userhand}🆚{bothand}')
                await ctx.send(f"{member.mention}, you've won!")
                addWin(userID)
            if userhand == scissor:
                await ctx.send(f'{userhand}🆚{bothand}')
                addLose(userID)
                await ctx.send(f'{member.mention}, you lose!')
        if bothand == paper:
            if userhand == rock:
                await ctx.send(f'{userhand}🆚{bothand}')
                addLose(userID)
                await ctx.send(f'{member.mention}, you lose!')
            if userhand == paper:
                await ctx.send(f'{userhand}🆚{bothand}')
                await ctx.send("It's a draw!")
            if userhand == scissor:
                await ctx.send(f'{userhand}🆚{bothand}')
                await ctx.send(f"{member.mention}, you've won!")
                addWin(userID)
        if bothand == scissor:
            if userhand == rock:
                await ctx.send(f'{userhand}🆚{bothand}')
                await ctx.send(f"{member.mention}, you've won!")
                addWin(userID)
            if userhand == paper:
                await ctx.send(f'{userhand}🆚{bothand}')
                addLose(userID)
                await ctx.send(f'{member.mention}, you lose!')
            if userhand == scissor:
                await ctx.send(f'{userhand}🆚{bothand}')
                await ctx.send("It's a draw!")

class RPS(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rps(self, ctx, member: discord.Member=None):
        member = ctx.message.author
        userID = str(member.id)

        exists = findUser(userID)
        if exists == None:
            # Create new player data
            addNewPlayer(userID)
        await play(self,ctx,member,userID)

def setup(bot):
    bot.add_cog(RPS(bot))
