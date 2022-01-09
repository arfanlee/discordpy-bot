import arrow
from discord.ext import commands
import discord
from getdatabase import connect
import random

records = connect()

class Work(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.cooldown(1, 1, commands.BucketType.user) # 1 sec cooldown
    async def work(self, ctx):
        userID = str(ctx.message.author.id)
        user_name = ctx.message.author.name
        player = records.find_one({'userID': userID})

        current_time = arrow.utcnow() # get current time
        last_shift = player['last_shift'] # retrieve datetime from database
        next_shift = arrow.get(last_shift).shift(hours=1) # convert datetime type to arrow type also shift forward to check if it's ready

        if current_time > next_shift:
            random_coins = random.randint(200, 500)
            wallet = player['wallet']
            new_total = wallet + random_coins 
            wallet_update = {'wallet': new_total}
            records.update_one({'userID': userID},{'$set':wallet_update})
            shift_update = {'last_shift': current_time.datetime} # Convert back arrow type to datetime type
            records.update_one({'userID': userID},{'$set':shift_update})
            embed = discord.Embed(colour = discord.Colour.green(), description=f"{user_name}, you've claimed your {random_coins} coins paycheck")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour = discord.Colour.red(),
                    description=f"{user_name}, you've already claimed your paycheck. Your next pay is {next_shift.humanize(current_time)}")
            await ctx.send(embed=embed)

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Please don't spam. Try again in {error.retry_after:.2f}s.")
def setup(bot):
    bot.add_cog(Work(bot))
