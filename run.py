import random
import os
from nextcord.ext import commands

TOKEN = os.environ.get('BOT_TOKEN')
HOST = os.environ.get('HOST')

with open('.\\food.txt', 'r') as f:
    content = f.read().split(',')


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.on_message_callback = []
        
    def more_cog(self, cog):
        if "on_message" in dir(cog):
            self.on_message_callback.append(cog.on_message)
        self.bot.add_cog(cog)

    @commands.Cog.listener()
    async def on_message(self, message):
        for callback in self.on_message_callback:
            await callback(message)
            
class Basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.llast_msg = {}
        self.last_msg = {}
        self.HOST = HOST
    
    @commands.command(name='choose')
    async def choose(self, ctx, *args):
        result = random.randint(0, len(args) - 1)
        print(args)
        await ctx.reply(args[result], mention_author = False)
    
    @commands.command(name='메뉴')
    async def wutfood(self, ctx):
        result = random.randint(0, len(content) - 1)
        lotto = random.randint(1, 8145060)
        if 8145060 == lotto:
            await ctx.reply('음... 와타시. >//< {}'.format(ctx.author.mention))
            return
        
        await ctx.reply('음... ' + content[result] +'.', mention_author = False)
        
    @commands.Cog.listener()
    async def copypasta(self, message):
    # gonna do something with https://pypi.org/project/python-sql/ later
        repl = False
        cid = message.channel.id
        if (cid in self.last_msg and self.last_msg[cid].content == message.content and
            not (cid in self.llast_msg and self.llast_msg[cid].content == message.content) and
            not self.last_msg[cid].author.id == message.author.id and
            not self.last_msg[cid].author.bot):
            repl = True
        
        if cid in self.last_msg:
            self.llast_msg[cid] = self.last_msg[cid]
        self.last_msg[cid] = message
        
        if repl and len(message.content) > 0:
            await message.channel.send(message.content)

    async def on_message(self, message):
        await self.copypasta(message)
        
        if message.author.bot:
            return

        if self.bot.user.mentioned_in(message):
            if not ("@here" in message.content or "@everyone" in message.content):
                await message.reply("안녕. {} 선생님.".format(message.author.mention))
                
        if is_modding(message.content):
            await message.reply(osu_link(message.content), mention_author = False)
            
        if '2022' in message.content:
            response = 'https://cdn.discordapp.com/attachments/915261506449469531/931251104107335770/20220110_122631.jpg'
            await message.channel.send(response)
            
def is_modding(msg):
    if 2 <= msg.count(':'):
        a = msg.find(':')
        b = msg[a + 1:].find(':')
        if a == b and msg[b + 4].isnumeric():
            return True
    return False
    
def osu_link(msg):
    box = []
    box = msg.split()
    new_box = []
    result = ''
    for pos, char in enumerate(box):
        if is_modding(char): 
            new_box.append(char)
        elif pos != 0:
            if is_modding(box[pos - 1]) and char != '-':
                tmp = new_box.pop()
                new_box.append(tmp + '-' + char)
                
    for pos, char in enumerate(new_box):
        new_box[pos] = '<osu://edit/' + char + '>'
        
    if len(new_box) > 1:
        result = '\n'.join(new_box)
    else:
        result = new_box[0]
    return result

def main():

    def get_prefix(bot, message):
        prefixes = ['?']

        # Check to see if we are outside of a guild. e.g DM's etc.
        if not message.guild:
            # Only allow ? to be used in DMs
            return '?'

        # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
        return commands.when_mentioned_or(*prefixes)(bot, message)

    bot = commands.Bot(command_prefix=get_prefix, description='흰둥이', case_insensitive=True)
    
    base_cog = Base(bot)
    bot.add_cog(base_cog)
    base_cog.more_cog(Basics(bot))
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
