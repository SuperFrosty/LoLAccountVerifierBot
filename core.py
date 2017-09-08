import config
from discord.ext import commands

DESCRIPTION = "A Discord bot that verifies a user's ownership of a summoner through rune page names. Written by Frosty."
STARTUP_EXTENSIONS = ['verification', 'reload']

class VerificationCore(commands.Bot):
    """Core"""
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("?"), description=DESCRIPTION)
        self.bot_token = config.TOKEN

        for extension in STARTUP_EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as exception:
                exc = '{}: {}'.format(type(exception).__name__, exception)
                print('Failed to load extension {}\n{}'.format(extension, exc))
    
    async def on_message(self, message):
        if message.author.id == 342956235504615424 and message.content.startswith("ily dev"):
            await message.channel.send("❤")
        await self.process_commands(message)

    def run(self):
        super().run(self.bot_token)

if __name__ == '__main__':
    VerificationCore().run()
