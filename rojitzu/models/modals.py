import asyncio
from discord import TextStyle, Interaction, User, Member, Embed, Color, TextChannel
from discord.ext import commands
from discord.ui import TextInput, Modal
from discord.types.snowflake import Snowflake
from rojitzu.models.tickets import Ticket, TicketLogger, AppealTicket, TicketTypes
from rojitzu.utils.extentsions import PrismaExt
from rojitzu.utils.utilities import UtilMethods
from rojitzu.utils.config import Config
from typing import Union, Optional


class InfoReceiver(Modal, title="Info Receiver"):

    info = TextInput(label="Ticket Info", style=TextStyle.paragraph)

    def __init__(self, bot: commands.Bot, channel: TextChannel, status: Optional[bool] = None) -> None:
        super().__init__(timeout=None)
        self.client = bot
        self.channel = channel
        self.status = status
        self.log_channel_id: Snowflake = Config.log_channel_id
        self.prisma = PrismaExt()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.prisma.connect_client())

    async def on_submit(self, interaction: Interaction) -> None:

        usertable = await self.prisma.where_first("ticketcreator", "channelid", str(self.channel.id))
        try:
            user: Union[Member, User] = self.client.get_user(usertable.userid)
        except AttributeError as e:
            error_embed = await UtilMethods.embedify("Error",
                                                     f"{self.channel.mention} is an invalid ticket", Color.red())
            await interaction.response.send_message(embed=error_embed)
            self.stop()
            return
        log_channel = self.client.get_channel(self.log_channel_id)
        emb_description = f"**Info**\n{self.info}"

        if self.status:
            embed = Embed(title="Appeal Ticket", color=Color.teal())
            embed.set_footer(text=f"Status: {self.status}")
            ticket = AppealTicket(TicketTypes.APPEAL, user, interaction.user, self.info.value, self.status)
        else:
            embed = Embed(title="Ticket", color=Color.purple())
            ticket = Ticket(TicketTypes.TICKET, user, interaction.user, self.info.value)

        embed.description = emb_description
        message = await TicketLogger.log(ticket, log_channel, embed)
        log_embed = await UtilMethods.embedify("Ticket Log", message.jump_url, Color.blue())
        await interaction.response.send_message(embed=log_embed, ephemeral=True)
        self.stop()
