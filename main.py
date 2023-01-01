import discord
import os
import time
import aiohttp
import asyncio
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
TOKEN = os.getenv("MAGPIE")
bot = commands.Bot(command_prefix='m!', case_insensitive=True, intents=intents, help_command=None)


@bot.event
async def on_ready():
    print('syncing commands')
    await bot.tree.sync()
    print("MAGPIE IS READY TO CHASE YOU")
    await bot.change_presence(activity=discord.Game('With your mind - m!help'), status=discord.Status.online)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, this command does not exist. Contact unseeyou#2912 if you think this should be added.")


@bot.listen()
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="general")
    embed = discord.Embed(color=0x4a3d9a)
    embed.add_field(name=f"Welcome to {member.guild.name}!", value=f"{member.name} has joined the server!",
                    inline=False)
    await channel.send(embed=embed)


@bot.hybrid_command(help='shows the ping of the bot, usage: `m!ping`')
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong! My ping is `{int(ping)}ms`")
    print(f'Ping: `{int(ping)} ms`')


@bot.hybrid_command(name='8ball', help='usage: `m!8ball {question}`')
async def _8ball(ctx, message=None):
    if message is not None:
        llist = ['my sources say yes', 'hell no', 'ask again later', "idk man you're on your own", 'sure, why not?',
                 'how about... no?']
        await ctx.reply(random.choice(llist))
    else:
        await ctx.reply('ask me a question')


@bot.hybrid_command(aliases=['doggo', 'dogs', 'dogfacts', 'dogfact', 'pup', 'pupper', 'puppy'],
             help='cute dog images, usage: `m!dog`')
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog')
        dogjson = await request.json()
        request2 = await session.get('https://some-random-api.ml/facts/dog')
        factjson = await request2.json()
    dogbed = discord.Embed(title='DOGGY', colour=discord.Colour.dark_gold())
    dogbed.set_image(url=dogjson['link'])
    dogbed.set_footer(text=factjson['fact'])
    await ctx.send(embed=dogbed)


@bot.hybrid_command(aliases=['kitty', 'kitten', 'meow', 'catfact', 'catfacts'], help='cute cat images, usage: `m!cat`')
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        request1 = await session.get('https://some-random-api.ml/img/cat')
        catjson = await request1.json()
        request22 = await session.get('https://some-random-api.ml/facts/cat')
        factjson1 = await request22.json()
    catty = discord.Embed(title='KITTY', colour=discord.Colour.dark_gold())
    catty.set_image(url=catjson['link'])
    catty.set_footer(text=factjson1['fact'])
    await ctx.send(embed=catty)


@bot.hybrid_command(name='help', help='list of all the commands')
async def _help(ctx):
    help_embed = discord.Embed(title="HELP CENTRE FOR SUFFERERS OF MAGPIE",
                               description="Don't worry! This helpful guide will let you master the magpie!",
                               colour=discord.Color.brand_green())
    help_embed.add_field(name='cat and dog pics', value="usage: `m!dog` or `m!cat`", inline=False)
    help_embed.add_field(name="8ball", value="usage: `m!8ball {question}`", inline=False)
    help_embed.add_field(name="ping", value="`usage: m!ping`", inline=False)
    help_embed.add_field(name="xkcd comics", value="`usage: m!xkcd`", inline=False)
    help_embed.add_field(name="polls", value="`usage: m!createpoll {title} {description} {options divided by semicolons (;)}`", inline=False)
    help_embed.add_field(name="epic", value="`usage: m!epic {object/name}`", inline=False)
    help_embed.set_footer(text="made by unseeyou")
    help_embed.set_author(name="aaaa its a magpie oh no")
    await ctx.send(embed=help_embed)


async def main():
    async with bot:
        await bot.load_extension("cogs.epic")
        await bot.load_extension("cogs.poll")
        await bot.load_extension("cogs.xkcd")
        await bot.start(TOKEN)


asyncio.run(main())
