import discord
from discord.ext import commands
import asyncio

class React(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        chat = message.content.lower()
        if message.author == self.bot.user:
            return None

        if chat.startswith('hello lyra'):
            await message.channel.send(f'Hello {message.author.mention}')
            emoji = '👋'
            await message.add_reaction(emoji)

        if chat.startswith('how are you today lyra'):
            await message.channel.send(f"Feeling electric, thank you 😉. How about you, {message.author.mention}?")

        if chat.startswith('/high touch'):
            await message.channel.send(f'Send me the ✋ {message.author.mention}')

            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '✋'

            try:
                await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await message.channel.send(f'Aww... You left me hanging {message.author.mention}')
            else:
                await message.channel.send('Yay!')

        if chat.startswith("i love you, lyra"):
            await message.channel.send(f'Aww... I love you too, {message.author.display_name}!')

        if chat == 'lol':
            await message.channel.send('lol')

        if chat == 'uwu':
            await message.channel.send('owo')

    @commands.Cog.listener()
    async def on_message_edit(self, old_message, new_message):
        ctx = await self.bot.get_context(new_message)
        if ctx.valid:
            await self.bot.process_commands(new_message)

def setup(bot):
    bot.add_cog(React(bot))
