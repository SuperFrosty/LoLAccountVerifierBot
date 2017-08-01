import cassiopeia as cass
import random
import string
import discord
from discord.ext import commands
import asyncio

class Verification:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx, sum_name: str, region: str):
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
            summoner = cass.Summoner(name=sum_name, region=region)
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
                    for rank in rank_solo:
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
                        await self.bot.add_roles(ctx.author, role)
                        role_given = 'Challenger'
                    if highest_rank == 6:
                        role = discord.utils.find(lambda m: m.name == 'Master', ctx.guild.roles)
                        await self.bot.add_roles(ctx.author, role)
                        role_given = 'Master'
                    if highest_rank == 5:
                        role = discord.utils.find(lambda m: m.name == 'Diamond', ctx.guild.roles)
                        await self.bot.add_roles(ctx.author, role)
                        role_given = 'Diamond'
                    if highest_rank == 4:
                        role = discord.utils.find(lambda m: m.name == 'Platinum', ctx.guild.roles)
                        await self.bot.add_roles(ctx.author, role)
                        role_given = 'Platinum'
                    if highest_rank == 3:
                        role = discord.utils.find(lambda m: m.name == 'Gold', ctx.guild.roles)
                        await self.bot.add_roles(ctx.author, role)
                        role_given = 'Gold'
                    if highest_rank == 2:
                        role = discord.utils.find(lambda m: m.name == 'Silver', ctx.guild.roles)
                        await self.bot.add_roles(ctx.author, role)
                        role_given = 'Silver'
                    if highest_rank == 1:
                        role = discord.utils.find(lambda m: m.name == 'Bronze', ctx.guild.roles)
                        await self.bot.add_roles(ctx.author, role)
                        role_given = 'Bronze'
                    await ctx.author.send("", embed=discord.Embed(colour=0x1AFFA7, title="Success!", description="You've been given the {} role.".format(role_given)))
                else:
                    await ctx.author.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="Could not verify first rune page. Please wait a bit for the name change to save."))
            else:
                await ctx.send("", embed=discord.Embed(colour=0xCA0147, title="Error!", description="Couldn't find summoner '{0}' on the {1} region".format(summoner.name, region)))
                return

def setup(bot):
    """Adds cog to bot"""
    bot.add_cog(Verification(bot))