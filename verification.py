import asyncio
import random
import string
import urllib.parse

import cassiopeia as cass
import discord
from cassiopeia.configuration import settings
from cassiopeia.core import RunePages
from discord.ext import commands

VALID_REGIONS = ["BR", "EUW", "EUNE", "JP", "KR", "LAN", "LAS", "NA", "OCE", "RU", "TR"]

class Verification:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx, *args):
        if args[-1].upper() in VALID_REGIONS:
            region = args[-1].upper()
            sum_name = ' '.join(args[:(len(args) - 1)])
            print(sum_name)
        else:
            await ctx.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="Invalid region {0}!".format(args[-1].upper())))
            return

        if region == 'KR':
            await ctx.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="Riot recently disallowed rune page verification of korean accounts, sorry!"))
            reason = "KR account"
            print("{0} on region {1} - failed: {2}".format(sum_name, region, reason))
            return

        random_string = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
        try:
            await ctx.author.send("", embed=discord.Embed(colour=0x1AFFA7, title="Instructions:", description="Please rename your first rune page to `{}`, wait a while, then reply with 'done'.".format(random_string)))
            initial_embed = discord.Embed(colour=0x1AFFA7)
            initial_embed.add_field(name="Instructions DM'd!", value=ctx.author.mention)
            await ctx.send("", embed=initial_embed)
            print("{0} on region {1} - code: {2}".format(sum_name, region, random_string))
        except discord.Forbidden:
            await ctx.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="Couldn't DM you, perhaps you have them disable?"))
            reason = "Couldn't DM"
            print("{0} on region {1} - failed: {2}".format(sum_name, region, reason))


        def check(m):
            return m.content == 'done' and m.author == ctx.author

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=3600)
        except asyncio.TimeoutError:
            await ctx.author.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="You didn't respond in time."))
            reason = "Timeout"
            print("{0} on region {1} - failed: {2}".format(sum_name, region, reason))
            return
        else:
            await ctx.author.trigger_typing()

            try:
                summoner = cass.Summoner(name=urllib.parse.quote(sum_name.encode('utf-8')), region=region)
                print("{0} on region {1} - Summoner call passed".format(sum_name, region))
            except ValueError:
                await ctx.author.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="{} is not a valid region.".format(region)))
                reason = "Invalid region {0}".format(region)
                print("{0} on region {1} - failed: {2}".format(sum_name, region, reason))
                return

            if summoner.exists:
                rank_solo = ''
                pages = summoner.rune_pages
                print("{0} on region {1} - Page name: {2}".format(sum_name, region, pages[0].name))
                if random_string in pages[0].name:
                    leagues = summoner.leagues
                    for league in leagues:
                        queue = league.queue.value
                        if queue == 'RANKED_SOLO_5x5':
                            rank_solo = league.tier.value
                            print("{0} on region {1} - Solo: {2}".format(sum_name, region, rank_solo))
                    if 'CHALLENGER' in rank_solo:
                        role = discord.utils.find(lambda m: m.name == 'Challenger', ctx.guild.roles)
                        await ctx.author.add_roles(role, reason="Verified account.")
                        role_given = 'Challenger'
                    elif 'MASTER' in rank_solo:
                        role = discord.utils.find(lambda m: m.name == 'Master', ctx.guild.roles)
                        await ctx.author.add_roles(role, reason="Verified account.")
                        role_given = 'Master'
                    elif "DIAMOND" in rank_solo:
                        role = discord.utils.find(lambda m: m.name == 'Diamond', ctx.guild.roles)
                        await ctx.author.add_roles(role, reason="Verified account.")
                        role_given = 'Diamond'
                    elif "PLATINUM" in rank_solo:
                        role = discord.utils.find(lambda m: m.name == 'Platinum', ctx.guild.roles)
                        await ctx.author.add_roles(role, reason="Verified account.")
                        role_given = 'Platinum'
                    elif "GOLD" in rank_solo:
                        role = discord.utils.find(lambda m: m.name == 'Gold', ctx.guild.roles)
                        await ctx.author.add_roles(role, reason="Verified account.")
                        role_given = 'Gold'
                    elif "SILVER" in rank_solo:
                        role = discord.utils.find(lambda m: m.name == 'Silver', ctx.guild.roles)
                        await ctx.author.add_roles(role, reason="Verified account.")
                        role_given = 'Silver'
                    elif "BRONZE" in rank_solo:
                        role = discord.utils.find(lambda m: m.name == 'Bronze', ctx.guild.roles)
                        await ctx.author.add_roles(role, reason="Verified account.")
                        role_given = 'Bronze'
                    else:
                        await ctx.author.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="That account's unranked!"))
                        return
                    await ctx.author.send("", embed=discord.Embed(colour=0x1AFFA7, title="Success!", description="You've been given the `{}` role.".format(role_given)))
                    print("{0} on region {1} - Success: {2}".format(sum_name, region, role_given))
                    settings.pipeline._cache._cache._data[RunePages].clear()
                    return
                else:
                    await ctx.author.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="Could not verify first rune page. Expected: `{0}`, but was: `{1}`. Please wait a bit for the name change to save.".format(pages[0].name, random_string)))
                    reason = "Rune page not verified: {0}".format(pages[0].name)
                    print("{0} on region {1} - failed: {2}".format(sum_name, region, reason))
                    settings.pipeline._cache._cache._data[RunePages].clear()
                    return
            else:
                await ctx.author.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="Couldn't find summoner '{0}' on the {1} region".format(summoner.name, region)))
                reason = "Couldn't find summoner"
                print("{0} on region {1} - failed: {2}".format(sum_name, region, reason))
                return

def setup(bot):
    """Adds cog to bot"""
    bot.add_cog(Verification(bot))
