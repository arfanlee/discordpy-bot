import discord
import random
import datetime
from discord.ext import commands

class Ball(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['8ball'])
    async def _8ball(self, ctx, *args): # single star to turn the string into list, double is nothing is accepted
        member = ctx.message.author
        question = " ".join(args)
        if question == "":
            await ctx.send('Please enter your question!')
        else:
            found_word = False
            valid = ['will', 'am', 'should', 'are', 'is', 'does', 'what', 'did']
            responses = ['Yes','No','Maybe','There is a chance','Most likely','Well yes, but actually no']
            answer = random.choice(responses)

            for line in args:
                word = line.lower()
                for search in valid:
                    if word == search:
                        found_word = True
                        break
                    continue
                break

            embedGo = discord.Embed(
                colour = discord.Colour.green()
            )
            embedGo.set_author(name='The Magic 8ball',icon_url='https://i.imgur.com/l2cAnbA.png')
            embedGo.add_field(name='Question', value=question.capitalize(), inline=False)
            embedGo.add_field(name='Answer', value=answer, inline=False)
            embedGo.timestamp = datetime.datetime.utcnow()
            embedGo.set_footer(text=f'Asked by: {member.display_name}')

            if found_word is True:
                if len(args) > 2:
                    await ctx.send(embed=embedGo)
                else:
                    await ctx.send('That is not a valid question!')
            else:
                await ctx.send('That is not a valid question!')

def setup(bot):
    bot.add_cog(Ball(bot))