# TODO add durations inputs
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument

class Mute(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member:discord.Member=None, *reasonList):
        await ctx.message.delete()
        guild = ctx.guild
        reason = " ".join(reasonList)
        if len(reasonList) == 0:
            reason = "Not specified."
        if not member:
            await ctx.send("Please enter a valid member name.")
        if member is not None:
            if member.top_role < ctx.author.top_role:
                role = discord.utils.get(member.guild.roles, name='muted')
                if role not in guild.roles:
                    await guild.create_role(name="muted") # Creating the role and added the role perms in every text channel
                    role = discord.utils.get(member.guild.roles, name='muted')
                    for textChannel in ctx.guild.text_channels: # Finding all text channel in the server
                        await textChannel.set_permissions(role, send_messages=False)
                    for voiceChannel in ctx.guild.voice_channels:
                        await voiceChannel.set_permissions(role, view_channel=False)
                    await member.add_roles(role)
                    mute_msg = await ctx.send(f'{member} has been muted. Reason: {reason}')
                    await ctx.send(f"The role {role.mention} was not available, so I've created it for you.")
                else:
                    if role in member.roles:
                        mute_msg = await ctx.send(f'{member} already has been muted.')
                    else:
                        await member.add_roles(role)
                        mute_msg = await ctx.send(f'{member} has been muted. Reason: {reason}')
                await mute_msg.delete(delay=2)
            else:
                await ctx.send("You can only mute member with role lower than you!")

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member:discord.Member=None):
        await ctx.message.delete()
        if not member:
            await ctx.send("Please enter a valid member name.")
        if member is not None:
            if member.top_role < ctx.author.top_role:
                role = discord.utils.get(member.guild.roles, name='muted')
                if role in member.roles:
                    await member.remove_roles(role)
                    mute_msg = await ctx.send(f'{member} has been unmuted.')
                else:
                    mute_msg = await ctx.send(f'{member} is not muted.')
            else:
                await ctx.send("You can only unmute member with role lower than you!")
            await mute_msg.delete(delay=2)

    @mute.error
    async def mute_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, MissingPermissions):
            await ctx.send(error)
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Missing a required argument: {error.param}")
        else:
            await ctx.send("There is no such member on the server.")

    @unmute.error
    async def unmute_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, MissingPermissions):
            await ctx.send(error)
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Missing a required argument: {error.param}")
        else:
            await ctx.send("There is no such member on the server.")
def setup(bot):
    bot.add_cog(Mute(bot))