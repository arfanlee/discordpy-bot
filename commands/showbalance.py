import discord
from discord.ext import commands
from getdatabase import connect

records = connect()

class Balance(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member:discord.Member=None): 

        if not member:
            member = ctx.message.author
        
        player = records.find_one({'userID': str(member.id)})
        wallet = player['wallet']
        bank = player['bank']
        embed = discord.Embed(colour = discord.Colour.green(), description=f'👛 **Cash**: {wallet} 👛\n🏧 **Bank**: {bank} 🏧')
        embed.set_author(name=f"{member.display_name}'s balance", icon_url=member.avatar_url)
        embed.set_footer(text=f'Total: {bank + wallet}')
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Balance(bot)) 
