import cairosvg
from io import BytesIO
import discord

def send_game():
  with open('chess5.svg', 'rb') as svg_file:
          # Convert the SVG image to a PNG format
          png_data = cairosvg.svg2png(bytestring=svg_file.read())
  
          # Create a file-like object from the PNG data
          png_file = BytesIO(png_data)
  
          # Create a discord.py File object from the PNG file
          return discord.File(png_file, "game.png")
  
          