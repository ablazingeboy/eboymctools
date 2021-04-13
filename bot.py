import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from mojang import MojangAPI
from mcstatus import MinecraftServer

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix='e!')
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

#-----------------------------------------------------------------------------#
# Commands #

@bot.command(name='avatar', help='Gets the face of the inputted user.')
async def avatar(ctx, *args):
    if not args:
        embed=discord.Embed(title="Error!", description="No username was provided.", color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        await pull_crafatar(ctx, args[0], 'avatars', 'Avatar', '?overlay')

@bot.command(name='head', help='Renders the head of the inputted user.')
async def headrender(ctx, *args):
    if not args:
        embed=discord.Embed(title="Error!", description="No username was provided.", color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        await pull_crafatar(ctx, args[0], 'renders/head', 'Head', '?overlay')

@bot.command(name='body', help='Renders the body of the inputted user.')
async def bodyrender(ctx, *args):
    if not args:
        embed=discord.Embed(title="Error!", description="No username was provided.", color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        await pull_crafatar(ctx, args[0], 'renders/body', 'Body', '?overlay')

@bot.command(name='skin', help='provides the skin file of the inputted user.')
async def bodyrender(ctx, *args):
    if not args:
        embed=discord.Embed(title="Error!", description="No username was provided.", color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        await pull_crafatar(ctx, args[0], 'skins', 'Skin', '')

@bot.command(name='servstat', help='Displays the status of TG and other Minecraft servers.')
async def servstat(ctx):
    print('Checking Server Statuses')
    iplist = ['mc.rteenagers.com','play.pvplegacy.net', 'mc.hypixel.net']
    embed = discord.Embed(title="Server Status", color = discord.Color.purple())
    for ip in iplist:
        try:
            server = MinecraftServer.lookup(ip)
            output = f":green_circle: Server has **{server.status().players.online}** players and replied in **{server.status().latency}** ms"
        except:
            output = ":red_circle: **Uh oh, this server seems to be offline!**"
        print(output)
        embed.add_field(name=f"`{ip}`", value=output, inline=True)
    await ctx.send(embed=embed)

#-----------------------------------------------------------------------------#
# Helper Methods #

async def image_embed(ctx, title, imageurl):
    image_embed = discord.Embed(title=title, color=discord.Color.purple())
    image_embed.set_image(url=imageurl)
    await ctx.send(embed=image_embed)

async def pull_crafatar(ctx, query, urlbit, title, options):
    uuid = MojangAPI.get_uuid(query)
    if uuid == None:
        embed=discord.Embed(title="Error!", description="There is no user with this Minecraft username.", color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        title = f'{query}\'s {title}'
        imageurl = f'https://crafatar.com/{urlbit}/{uuid}{options}'
        await image_embed(ctx, title, imageurl)

#-----------------------------------------------------------------------------#
# Basic Stuff #

@bot.command(name='info', help='Displays information about the bot.')
async def info(ctx):
    info_embed = discord.Embed(
        title="Info",
        description=f'This is eboy\'s mc tools, a small personal bot that does stuff thats useful to me. Avatars and other renders are courtesy of Crafatar. This bot is currently in **{len(bot.guilds)}** servers!', 
        color=discord.Color.purple()
    )
    info_embed.set_footer(text='Made with <3 by ABlazingEBoy#7375')
    await ctx.send(embed=info_embed)

@bot.command(name='help', help='Shows this page.')
async def help(ctx, args=None):
    help_embed = discord.Embed(title="Command Usage", color=discord.Color.purple())
    command_names_list = [x.name for x in bot.commands]

    if not args:
        help_embed.add_field(
            name="List of supported commands:",
            value="\n".join([str(i+1)+".  `"+x.name+"`" for i,x in enumerate(bot.commands)]),
            inline=False
        )
        help_embed.set_footer(
            text="Type \'e!help <command name>\' for more details about each command."
        )

    elif args in command_names_list:
        help_embed.add_field(
            name='`=' + args + '`',
            value=bot.get_command(args).help
        )

    else:
        help_embed.add_field(
            name="Umm ackchually,",
            value="that command doesn't exist."
        )

    await ctx.send(embed=help_embed)

@bot.command(name='ping', help='Basically useless, just tells you if the bot is running.')
async def ping(ctx):
    if round(bot.latency * 1000) <= 50:
        embed=discord.Embed(title="Pong!", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x44ff44)
    elif round(bot.latency * 1000) <= 100:
        embed=discord.Embed(title="Pong!", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0xffd000)
    elif round(bot.latency * 1000) <= 200:
        embed=discord.Embed(title="Pong!", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0xff6600)
    else:
        embed=discord.Embed(title="Pong!", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x990000)
    await ctx.send(embed=embed)

#-----------------------------------------------------------------------------#

bot.run(TOKEN)