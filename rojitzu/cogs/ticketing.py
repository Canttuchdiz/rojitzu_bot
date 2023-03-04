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

    group = app_commands.Group(name="ticket", description="Ticket related commands")

    def __init__(self, bot: commands.Bot) -> None:
        self.client = bot
        self.log_channel_id = Config.log_channel_id
        self.prisma = PrismaExt()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.prisma.connect_client())
        self.ticket_manager = TicketManager(self.client)

    @group.command(name="create", description="Sets ticket category")
    async def create(self, interaction: Interaction, category: CategoryChannel) -> None:
        modal = EmbedDescriptor(self.client, category)
        await interaction.response.send_modal(modal)

    @group.command(name="log", description="Logs ticket")
    async def log(self, interaction: Interaction) -> None:
        try:
            log_channel = self.client.get_channel(self.log_channel_id)
            ticket = await self.ticket_manager.get_ticket(interaction.channel)
            await ticket.log_ticket(interaction.user, log_channel)
            await interaction.response.send_message("Successfully logged!", ephemeral=True)
        except AttributeError as e:
            await interaction.response.send_message("Invalid ticket", ephemeral=True)

    @group.command(name="close", description="Closes ticket")
    async def close(self, interaction: Interaction) -> None:
        ticket = await self.ticket_manager.get_ticket(interaction.channel)
        await interaction.response.send_message("Closing...", ephemeral=True)
        await ticket.delete_ticket(self.prisma)


    @group.command(name="add", description="Adds user to ticket")
    async def add(self, interaction: Interaction, user: Union[User, Member]) -> None:
        ticket = await self.ticket_manager.get_ticket(interaction.channel)
        await ticket.user_add(user)
        await interaction.response.send_message(f"{user.name} was added", ephemeral=True)

    @group.command(name="remove", description="removes user from ticket")
    async def remove(self, interaction: Interaction, user: Union[User, Member]) -> None:
        ticket = await self.ticket_manager.get_ticket(interaction.channel)
        await ticket.user_remove(user)
        await interaction.response.send_message(f"{user.name} was removed", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Ticketing(bot))
