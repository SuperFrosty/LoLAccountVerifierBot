import asyncio
import random
import string
import urllib.parse

import cassiopeia as cass
import discord
from cassiopeia.configuration import settings
from cassiopeia.core import RunePages
from discord.ext import commands


class Verification:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx, *args):
        if len(args) == 1:
            await ctx.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="Missing required argument!"))
            return
        if len(args) == 2:
            sum_name = u'{0}'.format(args[0])
            region = args[1]
        if len(args) == 3:
            sum_name = u"{0} {1}".format(args[0], args[1])
            region = args[2]

        if region == 'KR':
            await ctx.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="Riot recently disallowed rune page verification of korean accounts, sorry!"))
            return

        random_string = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
        try:
            await ctx.author.send("", embed=discord.Embed(colour=0x1AFFA7, title="Instructions:", description="Please rename your first rune page to `{}`, wait a while, then reply with 'done'.".format(random_string)))
            initial_embed = discord.Embed(colour=0x1AFFA7)
            initial_embed.add_field(name="Instructions DM'd!", value=ctx.author.mention)
            await ctx.send("", embed=initial_embed)
        except discord.Forbidden:
            await ctx.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="Couldn't DM you, perhaps you have them disable?"))
        
        def check(m):
            return m.content == 'done' and m.author == ctx.author

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=3600)
        except asyncio.TimeoutError:
            await ctx.author.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="You didn't respond in time."))
        else:
            await ctx.author.trigger_typing()

            try:
                summoner = cass.Summoner(name=urllib.parse.quote(sum_name.encode('utf-8')), region=region)
            except ValueError:
                await ctx.author.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="{} is not a valid region.".format(region)))
                return
            
            if summoner.exists:
                rank_solo, rank_flex, rank_tt = '', '', ''
                pages = summoner.rune_pages
                if random_string in pages[0].name:
                    leagues = summoner.leagues
                    for league in leagues:
                        queue = league.queue.value
                        if queue == 'RANKED_SOLO_5x5':
                            rank_solo = league.tier.value
                        if queue == 'RANKED_FLEX_SR':
                            rank_flex = league.tier.value
                        if queue == 'RANKED_FLEX_TT':
                            rank_tt = league.tier.value
                    ranks = [rank_solo, rank_flex, rank_tt]
                    numeric_ranks = []
                    for rank in ranks:
                        if rank == 'CHALLENGER':
                            numeric_ranks.append(7)
                        elif rank == 'MASTER':
                            numeric_ranks.append(6)
                        elif rank == 'DIAMOND':
                            numeric_ranks.append(5)
                        elif rank == 'PLATINUM':
                            numeric_ranks.append(4)
                        elif rank == 'GOLD':
                            numeric_ranks.append(3)
                        elif rank == 'SILVER':
                            numeric_ranks.append(2)
                        elif rank == 'BRONZE':
                            numeric_ranks.append(1)
                        elif rank == '':
                            numeric_ranks.append(0)
                    highest_rank = max(numeric_ranks)
                    if highest_rank == 7:
                        role = discord.utils.find(lambda m: m.name == 'Challenger', ctx.guild.roles)
                        await ctx.author.add_roles(role, reason="Verified account.")
                        role_given = 'Challenger'
                    if highest_rank == 6:
                        role = discord.utils.find(lambda m: m.name == 'Master', ctx.guild.roles)
                        await ctx.author.add_roles(role, reason="Verified account.")
                        role_given = 'Master'
                    if highest_rank == 5:
                        role = discord.utils.find(lambda m: m.name == 'Diamond', ctx.guild.roles)
                        await ctx.author.add_roles(role, reason="Verified account.")
                        role_given = 'Diamond'
                    if highest_rank == 4:
                        role = discord.utils.find(lambda m: m.name == 'Platinum', ctx.guild.roles)
                        await ctx.author.add_roles(role, reason="Verified account.")
                        role_given = 'Platinum'
                    if highest_rank == 3:
                        role = discord.utils.find(lambda m: m.name == 'Gold', ctx.guild.roles)
                        await ctx.author.add_roles(role, reason="Verified account.")
                        role_given = 'Gold'
                    if highest_rank == 2:
                        role = discord.utils.find(lambda m: m.name == 'Silver', ctx.guild.roles)
                        await ctx.author.add_roles(role, reason="Verified account.")
                        role_given = 'Silver'
                    if highest_rank == 1:
                        role = discord.utils.find(lambda m: m.name == 'Bronze', ctx.guild.roles)
                        await ctx.author.add_roles(role, reason="Verified account.")
                        role_given = 'Bronze'
                    else:
                        await ctx.author.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="That account's unranked!"))
                        return
                    await ctx.author.send("", embed=discord.Embed(colour=0x1AFFA7, title="Success!", description="You've been given the `{}` role.".format(role_given)))
                    settings.pipeline._cache._cache._data[RunePages].clear()
                else:
                    await ctx.author.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="Could not verify first rune page. Please wait a bit for the name change to save."))
                    settings.pipeline._cache._cache._data[RunePages].clear()
            else:
                await ctx.author.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="Couldn't find summoner '{0}' on the {1} region".format(summoner.name, region)))
                return

def setup(bot):
    """Adds cog to bot"""
    bot.add_cog(Verification(bot))
