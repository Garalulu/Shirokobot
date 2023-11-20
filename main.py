import discord
from discord.ext import commands
import os
import logging

from cogs.general.listener import Listener

# get token, application ID from env
TOKEN = os.environ.get("BOT_TOKEN")
ID = os.environ.get("BOT_ID")
# set logging
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix="?",
            description="흰둥이",
            intents=intents,
            application_id=ID,
        )
        self.initial_extensions = ["cogs.general.menu", "cogs.general.listener"]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        await self.tree.sync()

    async def on_command_error(self, ctx, error):
        # await ctx.reply(error, ephemeral=True)
        return


bot = MyBot()
bot.run(TOKEN, log_handler=None, log_level=logging.DEBUG)
