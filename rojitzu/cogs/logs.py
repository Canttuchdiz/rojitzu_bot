from __future__ import annotations
from discord import app_commands, User, Member, Interaction
from discord.app_commands import Choice
from discord.ext import commands
from rojitzu.models.modals import InfoReceiver
from rojitzu.models.tickets import TicketLogger, Ticket, AppealTicket
from typing import Union, Optional, Literal


class Logs(commands.Cog):
    log_group = app_commands.Group(name="log", description="Parent log group for appeals and tickets")

    def __init__(self, bot: commands.Bot) -> None:
        self.client = bot

    @log_group.command(name="ticket", description="Logs ticket")
    async def log_ticket(self, interaction: Interaction) -> None:
        modal = InfoReceiver(self.client, interaction.channel)
        await interaction.response.send_modal(modal)

    @log_group.command(name="appeal", description="Logs appeal ticket")
    async def log_appeal(self, interaction: Interaction, status: Literal["Accepted", "Declined"]) -> None:
        modal = InfoReceiver(self.client, interaction.channel, status)
        await interaction.response.send_modal(modal)


async def setup(bot):
    await bot.add_cog(Logs(bot))
