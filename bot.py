import discord
import os
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix = '.',intents=intents)
bot.remove_command('help')

movies = ['I, Robot','Terminator','Chappie','Ex Machina','WALL-E','Robocop','The Terminator','Ghost in the Shell','Gurenn Lagan']
statuses = ["I'm up!", "I'm alive!", "I'm ready!"]
@bot.event
async def on_ready():
    aMovie = random.choice(movies)
    activity = discord.Activity(name=aMovie, type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    print('Bot is online.')

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')

bot.run('DISCORD_API')
