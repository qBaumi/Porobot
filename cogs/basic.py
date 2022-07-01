import asyncio
import random
import discord
from discord.ext import commands
from discord import app_commands

import utils
from config import guilds, allowedRoles


class basic(commands.Cog):
    def __init__(self, client):
        self.client = client

        # Check if the user exists in the loyalty table

    def check_loyalty(self, user):
        id = utils.sql_select(f"SELECT id FROM poroscore WHERE id = '{user.id}'")
        print(id)
        if id:
            return True

        print("here")
        return False

    @app_commands.command(name="poropoints", description="Give a user Poro Score Points")
    @app_commands.describe(user="User that gets Poro Score Points")
    @app_commands.describe(poroscore="PoroScore the user gets")
    async def poropoints(self, interaction: discord.Interaction, user: discord.User,
                     poroscore: int):

        if not await utils.checkPerms(interaction, allowedRoles):
            return

        # If the user has no loyalty points he gets inserted into the loyalty table
        if not self.check_loyalty(user):
            utils.sql_exec(f"INSERT INTO poroscore (id, score) VALUES ('{user.id}', {poroscore})")

            await interaction.response.send_message(f"{user.mention} got {poroscore} PoroScore, they now have {poroscore} PoroScore in total!")
            return
        # If the user already received loyalty points they get fetched and added
        data = utils.sql_select(f"SELECT score FROM poroscore WHERE id = '{user.id}'")
        prevpoints = int(data[0][0])
        print(prevpoints)
        utils.sql_exec(f"UPDATE poroscore SET score = {poroscore + prevpoints} WHERE id = '{user.id}'")
        partyemoji = "🟨"
        redsquare = "🟥"
        empty = "<:rect843:881875152630059019>"
        await interaction.response.send_message(f"{partyemoji}{redsquare}{partyemoji}{redsquare}{partyemoji}{redsquare}{partyemoji}{redsquare}{partyemoji}{redsquare}{partyemoji}{redsquare}{partyemoji}{redsquare}\n"
                                                f"{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}\n"
                                                f"{empty} {user.mention} just got `{poroscore} PoroScore` <:poroL:984203294069112912>{empty}\n"
                                                f"{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}{empty}\n"
                                                f"{partyemoji}{redsquare}{partyemoji}{redsquare}{partyemoji}{redsquare}{partyemoji}{redsquare}{partyemoji}{redsquare}{partyemoji}{redsquare}{partyemoji}{redsquare}")

    @app_commands.command(name="poroscoreboard", description="PoroScoreBored")
    async def poroscoreboard(self, interaction: discord.Interaction):
        # Get all loyal points with user id in a list
        """
        list of tuples
        user = (user.id, points)
        loyaltylist = [(user.id, points), (user.id, points), (user.id, points)...]
        """
        emotes = [":poroBuff:984206353419612210", ":poroAmongus:984208212175781939", ":poroL:984203294069112912", ":poroMad:984209642932535356", ":poroSara:984208209529159710", ":poroEZ:984204134712504361", ":poroDank:984206880295489536", ":porocope:984215491587489793", ":porohappy:983843627073691658", ":porohappy:983843627073691658"]
        data = utils.sql_select(f"SELECT * FROM poroscore ORDER BY score DESC LIMIT 10")

        em = discord.Embed(colour=discord.Color.from_str("#e2e7e3"), title="PoroScoreBoard",
                           description="Get PoroScore by being <:poroBuff:984206353419612210>")
        # loop through each user, fetch them and add to embed
        for user in data:
            member = await self.client.fetch_user(user[0])
            em.add_field(name=str(member), value=f"`PoroScore: {user[1]}` <{random.choice(emotes)}>", inline=False)
        await interaction.response.send_message(embed=em, ephemeral=True)

async def setup(client):
    await client.add_cog(basic(client), guilds=guilds)
