import os
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
WOLFRAM_APP_ID = os.getenv('WOLFRAM_APP_ID')

class HomeworkHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def solve(self, ctx, *, query: str):
        result = self.wolfram_alpha_query(query)
        if result:
            await ctx.send(result)
        else:
            await ctx.send("Sorry, I couldn't process that request.")

    @commands.command()
    async def explain(self, ctx, *, topic: str):
        result = self.wolfram_alpha_query(topic)
        if result:
            await ctx.send(result)
        else:
            await ctx.send("Sorry, I couldn't process that request.")

    def wolfram_alpha_query(self, query: str) -> str:
        base_url = "http://api.wolframalpha.com/v1/result"
        params = {
            "i": query,
            "appid": WOLFRAM_APP_ID
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            return response.text
        else:
            return None  # Return None if there's an error, so we can handle it in the command methods

async def setup(bot):  # This function is synchronous
    await bot.add_cog(HomeworkHelp(bot))
