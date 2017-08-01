'''
Created on 10Feb.,2017

@author: Alex Palmer | SuperFrosty
'''
from discord.ext import commands

import config


class Reload:
    """Blitzcrank's reloading module,"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True, hidden=True, description="Test")
    @commands.is_owner()
    async def reload(self, ctx, *, module: str):
        """Reloads the specified module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send("There was an error reloading module {}:".format(module))
            await ctx.send("```fix\n{}: {}\n```".format(type(e).__name__, e))
        else:
            await ctx.send("{} successfully reloaded.".format(module))


def setup(bot):
    bot.add_cog(Reload(bot))
