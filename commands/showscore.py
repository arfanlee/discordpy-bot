import discord
from discord.ext import commands
import asyncio
from getdatabase import connect

records = connect()

class Showscore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=['score', 'scores'])
    async def showscore(self, ctx, member:discord.Member=None):
        if not member: # if a member is not specified, the author will be the member
            member = ctx.message.author
        player = records.find_one({'userID': str(member.id)})
        rpsWin = player['rpsWin']
        rpsLose = player['rpsLose']
        flipWin = player['flipWin']
        flipLose = player['flipLose']
        diceWin = player['diceWin']
        diceLose = player['diceLose']
        embedShow = discord.Embed(colour = 0x2F3136) # The greyish colour same as discord background

        embedShow.set_author(name=f"{member.display_name}'s Game Scores",icon_url=member.avatar_url)
        embedShow.add_field(name="Rock, paper, scissor",value=f"**Total win:** {rpsWin}\n**Total lose:** {rpsLose}")
        embedShow.add_field(name="Dice", value = f"**Total win:** {diceWin}\n**Total lose:** {diceLose}")
        embedShow.add_field(name="Coin flip", value = f"**Total win:** {flipWin}\n**Total lose:** {flipLose}")
        embedShow.set_footer(text=f'Total Games: {rpsWin + rpsLose + flipWin + flipLose + diceWin + diceLose}')
        await ctx.send(embed=embedShow)

def setup(bot):
    bot.add_cog(Showscore(bot))
