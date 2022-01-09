import discord
from discord.ext import commands
import asyncio

answer = ''

class Clear(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, *args, member:discord.Member=None):
        def check(reaction,user):
            global answer
            answer = str(reaction.emoji)
            return user == ctx.author and answer in reactions

        no = '❌'
        yes = '⭕'
        reactions = [yes, no]

        if len(args) > 1:
            await ctx.send("That's an invalid parameters!")

        elif len(args) < 1:
            await ctx.send("You need to enter a value!")

        elif len(args) == 1:
            amount = "".join(args)
            
            if amount.isdigit():
                await ctx.channel.purge(limit=int(amount)+1)
                done_deleted = await ctx.send(f'{amount} messages deleted!')
                await asyncio.sleep(2)
                await done_deleted.delete()
            
            elif amount == "all":
                msg_all = await ctx.send("Are you sure you want to delete all messages in this channel?")

                # Adding emojis to the msg above
                for line in reactions:
                    await msg_all.add_reaction(line)

                try:
                    await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                except asyncio.TimeoutError:
                    await msg_all.delete()
                    slow = await ctx.send('Woops, too slow!')
                    await asyncio.sleep(2)
                    await slow.delete()
                else:
                    if answer == yes:
                        await ctx.channel.purge(limit=None)
                        await ctx.send('https://i.imgflip.com/30y5fr.jpg')
                    elif answer == no:
                        await msg_all.delete()
                        nvm = await ctx.send('Purging all messages is canceled.')
                        await asyncio.sleep(2)
                        await nvm.delete()

            else:
                await ctx.send('You need to enter proper value!')
                
    @clear.error
    async def clear_error(error, ctx):
        if isinstance(error, commands.MissingPermissions):
            msg = f"Sorry, you need {commands.MissingPermissions} to use this command"
            await ctx.send(msg)

def setup(bot):
    bot.add_cog(Clear(bot))
