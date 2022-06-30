import asyncio
import random

import discord
from discord.ext import commands
import utils
from config import token
from discord import app_commands
from config import guilds, guild

client = commands.Bot(case_insensitive=True, command_prefix="joemama ", intents=discord.Intents.all())
client.remove_command("help")


@client.event
async def on_ready():
    print('starting...')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="to you malding"))
    for g in guilds:
        await client.tree.sync(guild=g)
    print("started")

@client.event
async def setup_hook():
    await client.load_extension("cogs.basic")



client.run(token)
