import os
import random

import discord
from discord.ext import commands, tasks

import config
from datetime import datetime, timedelta  # Add this line to import datetime

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all()) 
reminders = []
    
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")
bot.run(config.BOT_TOKEN)