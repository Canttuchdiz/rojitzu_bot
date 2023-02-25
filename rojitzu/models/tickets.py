from __future__ import annotations
from discord import TextChannel, Embed, Color
from discord import User, Member, Message
from discord.ext import commands
from rojitzu.utils.config import Config
from dataclasses import dataclass
from typing import Union, Optional
from enum import Enum


class TicketTypes(Enum):

    TICKET = "ticket"
    APPEAL = "appeal"


@dataclass
class Ticket:
    ticket_type: TicketTypes
    user: Union[User, Member]
    logger: Union[User, Member]
    info: str


@dataclass
class AppealTicket(Ticket):
    status: str


class TicketLogger:

    def __init__(self, bot: commands.Bot) -> None:
        self.client = bot

    @staticmethod
    async def log(ticket: Union[Ticket, AppealTicket], channel: TextChannel, embed: Embed) -> Message:
        TicketLogger.log_embed(ticket, embed)
        message = await channel.send(embed=embed)
        return message

    @staticmethod
    def log_embed(ticket: Union[Ticket, AppealTicket], embed: Embed) -> None:
        embed.add_field(name="Ticket Data", value=f"``Ticket Creator``: "
                                                  f"**{ticket.user}**\n``User ID``: *{ticket.user.id}*\n"
                                                  f"``Ticket Staff``: **{ticket.logger}**\n"
                                                  f"``Staff ID``: *{ticket.logger.id}*")
