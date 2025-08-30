import discord
from discord.ext import commands
from ch import ChessGame
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
import io

intents = discord.Intents.default()
intents.message_content = True  # Needed to see message text

bot = commands.Bot(command_prefix="!", intents=intents)
games = {"1": None}

def game_viewer():
    with open('games/chess5.svg', 'rb') as f:
        svg_data = f.read()
    svg_img = svg2rlg(io.BytesIO(svg_data))
    pil_img = renderPM.drawToPIL(svg_img)
    png_bytes = io.BytesIO()
    pil_img.save(png_bytes, format='PNG')
    png_bytes.seek(0)
    return discord.File(png_bytes, filename='image.png')

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name='Chess')
    )
    print(f"Bot online as {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return  # ignore the bot's own messages

    content = message.content.strip().lower()

    # Start a new game
    if content.startswith("!start"):
        games["1"] = ChessGame()
        await message.channel.send(file=game_viewer())

    # Play a move
    elif content.startswith("!play"):
        if games.get("1") is None:
            await message.channel.send("No game in progress. Use !start first.")
            return

        parts = content.split(maxsplit=1)
        if len(parts) < 2:
            await message.channel.send("You must specify a move, e.g. !play e2e4")
            return

        move = parts[1]
        try:
            games["1"].board.push_san(move)
            games["1"].play()
            games["1"].render_game()
            await message.channel.send("Move played", file=game_viewer())
        except Exception as e:
            await message.channel.send(f"Invalid move: {e}")


bot.run("TOKEN")

