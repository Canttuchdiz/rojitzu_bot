import asyncio
import discord
from discord import app_commands, Interaction, User, Member, Color, Embed, CategoryChannel
from discord.ext import commands
from rojitzu.utils.config import Config
from rojitzu.utils.extentsions import PrismaExt
from rojitzu.models.modals import EmbedDescriptor
from rojitzu.models.tickets import TicketManager
from typing import Union
import traceback


class Ticketing(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.client = bot
        self.log_channel_id = Config.log_channel_id
        self.prisma = PrismaExt()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.prisma.connect_client())
        self.ticket_manager = TicketManager(self.client)

    @app_commands.command(name="create", description="Sets ticket category")
    async def create(self, interaction: Interaction, category: CategoryChannel) -> None:
        modal = EmbedDescriptor(self.client, category)
        await interaction.response.send_modal(modal)

    @app_commands.command(name="log", description="Logs ticket")
    async def log(self, interaction: Interaction) -> None:
        try:
            log_channel = self.client.get_channel(self.log_channel_id)
            await self.ticket_manager.managed_log(interaction, log_channel)
            await interaction.response.send_message("Successfully logged!")
        except AttributeError as e:
            await interaction.response.send_message("Invalid ticket", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Ticketing(bot))
