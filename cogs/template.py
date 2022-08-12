import discord
from discord.ext import commands
from discord import app_commands
import utils
from config import guilds

class template(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="name", description="description")
    async def command(self, interaction: discord.Interaction):
        await interaction.response.send_message("command")

async def setup(client):
    await client.add_cog(template(client), guilds=guilds)
