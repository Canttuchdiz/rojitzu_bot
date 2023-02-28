import asyncio
from discord import TextStyle, Interaction, User, Member, Embed, Color, TextChannel, CategoryChannel
from discord.ext import commands
from discord.ui import TextInput, Modal
from rojitzu.models.views import TicketView, TicketClose
from rojitzu.models.tickets import TicketManager, TicketType
from typing import Union, Optional


class EmbedDescriptor(Modal, title="Embed Constructor"):
    name = TextInput(label="Title", style=TextStyle.paragraph)

    description = TextInput(label="Description", style=TextStyle.paragraph)

    def __init__(self, bot: commands.Bot, category: CategoryChannel) -> None:
        super().__init__(timeout=None)
        self.client = bot
        self.category = category

    async def on_submit(self, interaction: Interaction) -> None:
        view = TicketView(self.client, self.category)
        embed = Embed(title=self.name.value, description=self.description.value, color=Color.blue())
        embed.set_footer(text=f"ID · {self.client.user.id}")
        await interaction.response.send_message(view=view, embed=embed)


class TicketDescriptor(Modal, title="Ticket"):
    info = TextInput(label="Info", style=TextStyle.paragraph)

    def __init__(self, bot: commands.Bot, category: CategoryChannel) -> None:
        super().__init__(timeout=None)
        self.client = bot
        self.category = category
        self.ticket_manager = TicketManager(self.client)

    async def on_submit(self, interaction: Interaction) -> None:

        ticket = await self.ticket_manager.create_ticket(TicketType.TICKET, interaction.user,
                                                         self.category, self.info.value)
        lembed = self.ticket_manager.link_ticket(ticket)
        fem = Embed(title="Support Ticket", description=self.info.value, color=Color.blue())
        view = TicketClose(self.client, ticket, ticket.channel)
        await ticket.channel.send(view=view, embed=fem)
        await interaction.response.send_message(embed=lembed, ephemeral=True)
