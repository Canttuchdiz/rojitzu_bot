from __future__ import annotations
from functools import wraps
import asyncio
from discord import TextChannel, Embed, Color, CategoryChannel, Interaction
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

    def link_ticket(self) -> Embed:
        embed = Embed(title="Support Ticket", description=f"[Press for ticket]({self.channel.jump_url})",
                      color=Color.blue())
        return embed

    async def log_ticket(self, logger: Union[User, Member], log_channel: TextChannel) -> Ticket:
        embed = Embed(title="Support Ticket", description=f"**Info**\n{self.info}", color=Color.blue())
        embed.add_field(name="Data", value=f"``User``: **{self.user}**\n``Staff``: **{logger}**")
        embed.set_footer(text=f"User · {self.user.id} | Staff · {logger.id}")
        await log_channel.send(embed=embed)
        return self

    async def delete_ticket(self, prisma: PrismaExt) -> Ticket:
        await prisma.ticket.delete(
            where={
                'channelid': self.channel.id
            }
        )
        await self.channel.delete()

    async def user_add(self, user: Union[User, Member]) -> Ticket:
        await self.channel.set_permissions(user, send_messages=True, read_messages=True,
                                      attach_files=True, external_emojis=True, read_message_history=True)
        return self

    async def user_remove(self, user: Union[User, Member]) -> Ticket:
        await self.channel.set_permissions(user, send_messages=False, read_messages=False,
                                      attach_files=False, external_emojis=False,
                                      read_message_history=False)
        return self


@dataclass
class AppealTicket(Ticket):
    status: str


class TicketManager:

    def __init__(self, bot: commands.Bot) -> None:
        self.client = bot
        self.prisma = PrismaExt()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.prisma.connect_client())

    def can_create(func) -> None:
        @wraps(func)
        async def inner(inst, *args) -> None:
            user: Union[User, Member] = args[1]
            ticket_users = [ticket.user.id for ticket in await inst.tickets]
            if user.id not in ticket_users:
                return await func(inst, *args)

        return inner

    @can_create
    async def create_ticket(self, ticket_type: TicketType, user: Union[User, Member],
                            category: CategoryChannel, info: str) -> Ticket:
        channel = await self.private_channel(user, category)
        message = await channel.send(user.mention)
        await message.delete()
        ticket = Ticket(ticket_type, user, channel, info)
        await self._append_ticket(ticket)
        return ticket

    async def managed_log(self, interaction: Interaction, log_channel: TextChannel) -> Ticket:
        ticket = await self.get_ticket(interaction.channel)
        await ticket.log_ticket(interaction.user, log_channel)
        await ticket.delete_ticket(self.prisma)
        return ticket

    async def get_ticket(self, channel: TextChannel) -> Ticket:
        table = await self.prisma.ticket.find_first(
            where={
                'channelid': channel.id
            }
        )
        return Ticket(TicketType(table.type), self.client.get_user(table.userid),
                      self.client.get_channel(table.channelid), table.info)

    async def private_channel(self, user: Union[User, Member], category: CategoryChannel) -> TextChannel:
        channel = await category.create_text_channel(name=f'ticket-{user.name}')
        await channel.set_permissions(user, send_messages=True, read_messages=True,
                                      attach_files=True, external_emojis=True, read_message_history=True)
        return channel

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
        await ticket.user_remove(ticket.user)
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
