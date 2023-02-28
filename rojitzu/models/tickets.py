from __future__ import annotations
import asyncio
from discord import TextChannel, Embed, Color, CategoryChannel
from discord import User, Member, Message
from discord.ext import commands
from discord.types.snowflake import Snowflake
from rojitzu.utils.utilities import UtilMethods
from rojitzu.utils.extentsions import PrismaExt
from rojitzu.utils.config import Config
from dataclasses import dataclass
from typing import Union, Optional, List
from enum import Enum


class TicketType(Enum):

    TICKET = "ticket"
    APPEAL = "appeal"


@dataclass
class Ticket:
    ticket_type: TicketType
    user: Union[User, Member]
    channel: TextChannel
    info: str


@dataclass
class AppealTicket(Ticket):
    status: str


class TicketManager:

    def __init__(self, bot: commands.Bot) -> None:
        self.client = bot
        self.prisma = PrismaExt()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.prisma.connect_client())

    async def create_ticket(self, ticket_type: TicketType, user: Union[User, Member],
                            category: CategoryChannel, info: str) -> Ticket:
        channel = await self.create_channel(user, category)
        message = await channel.send(user.mention)
        await message.delete()
        ticket = Ticket(ticket_type, user, channel, info)
        await self._append_ticket(ticket)
        return ticket

    async def create_channel(self, user: Union[User, Member], category: CategoryChannel) -> TextChannel:
        channel = await category.create_text_channel(name=f'ticket-{user.name}')
        await channel.set_permissions(user, send_messages=True, read_messages=True,
                                      attach_files=True, external_emojis=True, read_message_history=True)
        return channel

    def link_ticket(self, ticket: Union[Ticket, AppealTicket]) -> Embed:
        embed = Embed(title="Support Ticket", description=f"[Press for ticket]({ticket.channel.jump_url})",
                      color=Color.blue())
        return embed

    async def _append_ticket(self, ticket: Union[Ticket, AppealTicket]) -> Ticket:
        await self.prisma.ticket.create(
            data={
                'type': ticket.ticket_type.value,
                'userid': ticket.user.id,
                'channelid': ticket.channel.id,
                'info': ticket.info
            }
        )
        return ticket

    async def close_ticket(self, ticket: Union[Ticket, AppealTicket]) -> Union[Ticket, AppealTicket]:
        await self.prisma.ticket.delete(
            where={
                'channelid': ticket.channel.id
            }
        )
        await ticket.channel.delete()
        return ticket

    @property
    async def tickets(self) -> List[Union[Ticket, AppealTicket]]:
        table = await self.prisma.ticket.find_many(
            order={
                'created_at': 'asc'
            }
        )
        return [Ticket(TicketType(ticket.type), self.client.get_user(ticket.userid),
                       self.client.get_channel(ticket.channelid), ticket.info) for ticket in table]

