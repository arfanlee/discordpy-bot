import discord
import random
from discord.ext import commands
from getdatabase import connect

records = connect()

def findUser(userID):
    return records.find_one({'userID':userID})

def addWin(userID):
    player = findUser(userID)
    currentWin = player['flipWin'] # We want the user's total win value only
    new_value = currentWin + 1
    user_update = {'flipWin': new_value}
    records.update_one({'userID': userID},{'$set':user_update})

def addLose(userID):
    player = findUser(userID)
    currentLose = player['flipLose'] # We want the user's total lose value only
    new_value = currentLose + 1
    user_update = {'flipLose': new_value}
    records.update_one({'userID': userID},{'$set':user_update})

def chkguess(flipped, guess, member):
    if flipped == guess:
        addWin(str(member.id))
        embed = discord.Embed(colour = discord.Colour.green(), description = f"You guessed {guess} and you're correct!")
    else:
        addLose(str(member.id))
        embed = discord.Embed(colour = discord.Colour.red(), description = f"You guessed {guess} and you're wrong!")
    return embed

class CoinFlip(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def flip(self, ctx, headtail=None):
        member = ctx.message.author
        passed = True
        if headtail is not None:
            guess = headtail.lower()
            if guess == 'heads' or guess == 'head' or guess == 'h':
                guess = 'head'
            elif guess == 'tails' or guess == 'tail' or guess == 't':
                guess = 'tail'
            else:
                passed = False
                await ctx.send("It's either heads or tails")

        if passed == True:
            # at this point it should be no error, as it has been clause guarded
            coin = ['head','tail']
            flipped = random.choice(coin)

            if flipped == 'head':
                if headtail is not None: 
                    embedHead = chkguess(flipped, guess, member)
                else:
                    embedHead = discord.Embed(colour = discord.Colour.green()) # if they don't guess, just initialized empty embed
                embedHead.set_author(name=f'{member.display_name} flipped {flipped}')
                embedHead.set_thumbnail(url='https://cdn.discordapp.com/attachments/276763774822645761/674568323412787212/1_coins.png')
                await ctx.send(embed=embedHead)
            else:
                if headtail is not None:
                    embedTail = chkguess(flipped, guess, member)
                else:
                    embedTail = discord.Embed(colour = discord.Colour.green())
                embedTail.set_author(name=f'{member.display_name} flipped {flipped}')
                embedTail.set_thumbnail(url='https://cdn.discordapp.com/attachments/276763774822645761/674555216695263252/1_coins.png')
                await ctx.send(embed=embedTail)

def setup(bot):
    bot.add_cog(CoinFlip(bot))
