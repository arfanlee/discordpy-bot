import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author

        if author.bot:
            return

        embed = discord.Embed(
            colour = discord.Colour.orange()
        )
        embed.set_author(name='Help')
        embed.add_field(name='ping', value='Returns Pong!\n', inline=False)
        embed.add_field(name='work', value='Work to claim paycheck every hour\n', inline=False)
        embed.add_field(name='8ball <question>', value='Think of an answer that can be answered in Yes or No.\n', inline=False)
        embed.add_field(name='flip', value='Will flip a coin for you.\n', inline=False)
        embed.add_field(name='rolldice | roll  | dice', value='Will roll a D6 for you.\n', inline=False)
        embed.add_field(name='rps', value='Fight Rock, Paper, Scissor with a bot.\n', inline=False)
        embed.add_field(name='time <Continent/City_Name>', value='Shows the current time in the specified location.', inline=False)
        embed.add_field(name='userinfo | uinfo', value="Show user's info.", inline=False)
        embed.add_field(name='serverinfo | sinfo', value="Show server's info")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
