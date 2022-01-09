import discord
import asyncio
import datetime
import pytz
import random
from discord.ext import commands
from gettime import thetime

morningPhrases = ["Good morning, everyone!", "Rise and shine, everyone!", "The sun is up, everyone!"]
afternoonPhrases = ["Good afternoon, everyone!", "It's high noon!", "It's lunch time!"]
eveningPhrases = ["Good evening, everyone!", "It's high tea!" ,"It's tea time!"]
nightPhrases = ["Good night, everyone!", "It's dinner time!"]
midnightPhrases = ["The clock has hit midnight!", "Lights out, everyone!", "The night is still young!"]

async def greet(ctx): # It is it's own coroutine to be invoked
        called = False

        while True:
            morningGreet = random.choice(morningPhrases)
            afternoonGreet = random.choice(afternoonPhrases)
            eveningGreet = random.choice(eveningPhrases)
            nightGreet = random.choice(nightPhrases)
            midnightGreet = random.choice(midnightPhrases)

            currentTime = thetime()
            active = currentTime.strftime('%H:%M') # Just stringify the time for trigger event

            embedTime = discord.Embed(
                colour = discord.Colour.green()
            )
            embedTime.add_field(name='Time: ', value=currentTime.strftime('%I:%M %p\n'), inline=False)
            embedTime.add_field(name='Date: ', value=currentTime.strftime('%A, %d %B %Y'), inline=False)
            embedTime.set_footer(text=currentTime.strftime('(GMT%z)'))
            
            if active == '00:00':
                if called == False:
                    await ctx.send(midnightGreet)
                    called = True
                else:
                    pass # To let just release the event

            elif active == '08:00':
                if called == False:
                    await ctx.send(morningGreet)
                    await ctx.send(embed=embedTime)
                    called = True
                else:
                    pass
            
            elif active == '12:00':
                if called == False:
                    await ctx.send(afternoonGreet)
                    called = True
                else:
                    pass

            elif active == '17:00':
                if called == False:
                    await ctx.send(eveningGreet)
                    called = True
                else:
                    pass

            elif active == '20:00':
                if called == False:
                    await ctx.send(nightGreet)
                    called = True
                else:
                    pass
            
            else:
                called = False

            await asyncio.sleep(1)

class Greeting(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            if message.content == "I'm up!":
                ctx = await self.bot.get_context(message)
                await greet(ctx)

def setup(bot):
    bot.add_cog(Greeting(bot))