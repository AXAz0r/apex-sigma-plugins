import aiohttp
import discord


async def chucknorris(cmd, message, args):
    embed = discord.Embed(color=0xFFDC5D)
    joke_url = 'https://api.chucknorris.io/jokes/random'
    async with aiohttp.ClientSession() as session:
        async with session.get(joke_url) as data:
            joke_json = await data.json()
    joke = joke_json['value']
    embed.add_field(name='💪 A Chuck Norris Joke', value=joke)
    await message.channel.send(None, embed=embed)
