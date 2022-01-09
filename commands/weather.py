import discord
from discord.ext import commands
from getweather import theweather

class Weather(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx, *, location):
        res = theweather(location)
        if res['cod'] != '404':
            icon = res['weather'][0]['icon']
            weather_icon_url = f'OPENWEATHER_API{icon}@2x.png'
            x = res['main']
            location = res['name'] + ', ' + res['sys']['country']
            temperature = str(round(x['temp'])) + '°C'
            feels_like = str(round(x['feels_like'])) + '°C'
            highLow = str(round(x['temp_max'])) + '°C / ' + str(round(x['temp_min'])) + '°C'

            embed = discord.Embed(
                    colour = 0x2F3136
                )
            embed.set_author(name='Weather')
            embed.set_thumbnail(url=weather_icon_url)
            embed.add_field(name='Location:', value=location, inline=False)
            embed.add_field(name='Temperature:', value=temperature, inline=True)
            embed.add_field(name='Feels like:', value=feels_like, inline=True)
            embed.add_field(name='High / Low:', value=str(highLow), inline=False)
            embed.set_footer(text='Powered by: OpenWeather', icon_url="https://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png")
        else:
            embed.set_author(name='Please enter correct city.')

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Weather(bot))
