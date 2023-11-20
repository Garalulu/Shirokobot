import discord
from discord.ext import commands
import random


class Listener(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.llast_msg = {}
        self.last_msg = {}

    async def copypasta(self, message: discord.Message) -> None:
        # repeat same messages when different people send the same message
        repl = False
        cid = message.channel.id
        if (
            cid in self.last_msg
            and self.last_msg[cid].content == message.content
            and not (
                cid in self.llast_msg and self.llast_msg[cid].content == message.content
            )
            and not self.last_msg[cid].author.id == message.author.id
            and not self.last_msg[cid].author.bot
        ):
            repl = True

        if cid in self.last_msg:
            self.llast_msg[cid] = self.last_msg[cid]
        self.last_msg[cid] = message

        if repl and len(message.content) > 0:
            await message.channel.send(content=message.content)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await self.copypasta(message)

        if "흰둥이" in message.content or "흰둥아" in message.content:
            result = random.randint(0, 1)
            reaction_list = [
                "<:shiroko:923136803463114802>",
                "<:koharu:923137473842929684>",
            ]
            await message.add_reaction(reaction_list[result])


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Listener(bot))
