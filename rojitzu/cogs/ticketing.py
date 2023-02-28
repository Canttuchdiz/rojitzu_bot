import asyncio
import discord
from discord import app_commands, Interaction, User, Member, Color, Embed, CategoryChannel
from discord.ext import commands
from rojitzu.models.modals import EmbedDescriptor
from typing import Union


class Ticketing(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.client = bot

    @app_commands.command(name="create", description="Sets ticket category")
    async def create(self, interaction: Interaction, category: CategoryChannel) -> None:
        modal = EmbedDescriptor(self.client, category)
        await interaction.response.send_modal(modal)


async def setup(bot):
    await bot.add_cog(Ticketing(bot))
