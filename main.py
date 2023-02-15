from keep_alive import keep_alive
import discord
import discord.ext
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash import SlashContext
from ch import ChessGame
from utils.send_game import send_game

#Define our bot
client = discord.Client()
games = {"1": None}

client = commands.Bot(
    command_prefix="!"
)  #put your own prefix here, but it wont matter since slash commands default to /

slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game(name='Chess')
                                 )  # Bot status
    print("Bot online"
          )  #will print "bot online" in the console when the bot is online


@slash.slash(name="start", description="start new chess game")
async def start_game(ctx: SlashContext):
    await ctx.send("Starting a new game...")
    games["1"] = ChessGame()
    await ctx.send(file=send_game())


@slash.slash(name="play", description="send user's current game")
async def play(ctx: SlashContext, move: str):
    games["1"].board.push_san("e4")
    await ctx.send("move played")
    games["1"].render_game()
    games["1"].play()
    await ctx.send(file=send_game())


#Run our webserver, this is what we will ping
keep_alive()

#Run our bot
client.run(
    "MTAxMjQyMzQ5NDA5MDM3MTA4Mg.GmHKJx.zxUP9I4fBkwG02-g99oIL3h96sBz1TlVgOXxcA")
