import discord
from discord.ext import commands
import random

# get food list
with open("food.txt", "r", encoding="UTF-8") as f:
    FOOD = f.read().split(",")


class Menu(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    # menu recommend
    @commands.hybrid_command(name="메뉴", description="메뉴 추천")
    async def menu(self, ctx: commands.Context) -> None:
        result = random.randint(0, len(FOOD) - 1)
        lotto = random.randint(1, 8145060)
        if 727 == lotto:
            await ctx.send("음... 와타시. >//<")
        else:
            await ctx.send(f"음... {FOOD[result]}.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Menu(bot))
