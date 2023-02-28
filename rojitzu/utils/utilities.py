import discord
from discord import Embed, Color, Guild, User, Member, TextChannel
from typing import Union


class UtilMethods:


    @staticmethod
    async def embedify(title: str, description: str, color: Color) -> Embed:
        embed = Embed(title=title, description=description, color=color)
        return embed

