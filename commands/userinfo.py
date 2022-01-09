import discord
import random
from discord.ext import commands
import arrow

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['uinfo'])
    async def userinfo(self, ctx, member:discord.Member=None):
        rolesholder = []

        if not member:  # if member is not mentioned
            member = ctx.message.author  # set the author as the member
        status = str(member.status)
        if status == 'online':
            presence = '🟢'
        elif status == 'idle':
            presence = '🟠'
        elif status == 'dnd':
            presence = '🔴'
        else:
            presence = '⚪'

        for role in member.roles:
            if role.name != "@everyone":
                rolesholder.append(role.mention)
        roles = ", ".join(rolesholder)

        today = arrow.utcnow()
        account_created = arrow.get(member.created_at)
        joined_server = arrow.get(member.joined_at)

        created_ago = account_created.humanize(today)
        joined_ago = joined_server.humanize(today)

        embedGo = discord.Embed(colour = 0x2F3136)
        embedGo.set_author(name=f"{presence} {member}")
        embedGo.set_thumbnail(url=member.avatar_url)
        embedGo.add_field(name="Joined Discord on:", value=f"{account_created.strftime('%#d %b %Y, %I:%M')}\n ({created_ago})")
        embedGo.add_field(name="Joined this server on:", value=f"{joined_server.strftime('%#d %b %Y %H:%M')}\n ({joined_ago})")
        embedGo.add_field(name="Roles:", value=roles,inline=False)
        embedGo.set_footer(text=f"Requested by {ctx.author}")

        await ctx.send(embed=embedGo)


def setup(bot):
    bot.add_cog(Info(bot))
