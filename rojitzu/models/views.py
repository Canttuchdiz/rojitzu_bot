from discord import ButtonStyle, Interaction, CategoryChannel, TextChannel
from discord.ext import commands
from discord.ui import View, button, Button
from rojitzu.models.tickets import TicketManager, Ticket, AppealTicket
from typing import Union

class TicketView(View):

    def __init__(self, bot: commands.Bot, category: CategoryChannel) -> None:
        super().__init__(timeout=None)
        self.client = bot
        self.category = category

    @button(label="Create Ticket", style=ButtonStyle.primary, emoji='📩')
    async def ticket_button(self, interaction: Interaction, button_obj: Button) -> None:
        from rojitzu.models.modals import TicketDescriptor

        modal = TicketDescriptor(self.client, self.category)
        await interaction.response.send_modal(modal)


class TicketClose(View):

    def __init__(self, bot: commands.Bot, ticket: Union[Ticket, AppealTicket], channel: TextChannel) -> None:
        super().__init__(timeout=None)
        self.client = bot
        self.ticket = ticket
        self.channel = channel
        self.ticket_manager = TicketManager(self.client)

    @button(label="Close", style=ButtonStyle.danger, emoji='🔒')
    async def close_ticket(self, interaction: Interaction, button_obj: Button) -> None:
        await self.ticket_manager.close_ticket(self.ticket)
        await interaction.response.send_message("🔒 Ticket has closed")


