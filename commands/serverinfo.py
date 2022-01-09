import discord
from discord.ext import commands
import arrow

def turingtest(humans, bots, user:discord.Member=None):
    if user.bot is True:
        bots += 1
    else:
        humans += 1
    return humans, bots
    
class ServerInfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True,aliases=['sinfo'])
    async def serverinfo(self, ctx):
        # Initialized all the informations needed
        humans, bots = 0, 0
        onlineMembers = 0
        offlineMembers = 0
        idleMembers = 0
        dndMembers = 0
        serverName = ctx.guild.name
        guild_created = ctx.guild.created_at
        total_text_channels = 0
        total_voice_channels = 0
        total_channels = 0

        for channel in ctx.guild.text_channels:
            total_text_channels += 1

        for channel in ctx.guild.voice_channels:
            total_voice_channels += 1

        for member in ctx.guild.members:
            x, y = 0, 0
            status = str(member.status) # Stringify the member's status

            if status == 'online':
                x, y = turingtest(humans, bots, member)
                onlineMembers += 1
            elif status == 'idle':
                x, y = turingtest(humans, bots, member)
                idleMembers += 1
            elif status == 'dnd':
                x, y = turingtest(humans, bots, member)
                dndMembers += 1
            else:
                x, y = turingtest(humans, bots, member)
                offlineMembers += 1
            humans = x
            bots = y
        totalMembers = onlineMembers + offlineMembers + idleMembers + dndMembers

        today = arrow.utcnow()
        server_created = arrow.get(guild_created)
        created_ago = server_created.humanize(today)

        embed = discord.Embed(color=discord.Colour.teal())
        embed.set_author(name=serverName)
        embed.description = f"Created on {server_created.strftime('%a, %#d %B %Y %H:%M')}.\nThat's over {created_ago}!"
        embed.add_field(name='Members:', value=f"""Users online: **{onlineMembers}/{totalMembers}**\nHumans: **{humans}** Bots: **{bots}**
🟢 **{onlineMembers}** • 🟠 **{idleMembers}** \n🔴 **{dndMembers}** • ⚪ **{offlineMembers}**""")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name='Channels', value=f'💬 Text: {total_text_channels}\n🔊 Voice: {total_voice_channels}')

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ServerInfo(bot))
