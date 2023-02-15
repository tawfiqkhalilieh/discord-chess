from keep_alive import keep_alive
import discord
import discord.ext
from discord.ext import commands

from discord_slash import SlashCommand
from discord_slash import SlashContext
from ch import ChessGame
from svglib.svglib import svg2rlg

# define our bot
client = discord.Client()

# define the dict for the games
# struct example:
# games: {
#   "user1id": ChessGame Object
#   "user2id": ChessGame Object
# }

games = {"1": None}

client = commands.Bot(
    command_prefix="!"
)  #put your own prefix here, but it wont matter since slash commands default to /

slash = SlashCommand(client, sync_commands=True)

def game_viewer():
    from PIL import Image
    import svglib
    import io

    svg_data = open('games/chess5.svg', 'rb').read()
    svg_img = svglib.svglib.svg2rlg(io.BytesIO(svg_data))

    from reportlab.graphics import renderPM
    pil_img = renderPM.drawToPIL(svg_img)
    png_bytes = io.BytesIO()
    pil_img.save(png_bytes, format='PNG')
    png_bytes.seek(0)
    return discord.File(png_bytes, filename='image.png')

@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name='Chess')
    )
    print("Bot online")  


@slash.slash(name="start", description="start new chess game")
async def start_game(ctx: SlashContext):
    games["1"] = ChessGame()
    await ctx.send(file=game_viewer())
    

@slash.slash(name="play", description="send user's current game")
async def play(ctx: SlashContext, move: str):
    print(games)
    games["1"].board.push_san(move)
    await ctx.send("move played")
    
    games["1"].play()
    games["1"].render_game()

    await ctx.send(file=game_viewer())
    

# for now no need to run the bot in the backend

# #Run our webserver, this is what we will ping
# keep_alive()

#Run our bot
client.run(
    "MTAxMjQyMzQ5NDA5MDM3MTA4Mg.GmHKJx.zxUP9I4fBkwG02-g99oIL3h96sBz1TlVgOXxcA")
