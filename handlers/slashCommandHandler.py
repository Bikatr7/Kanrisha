## built-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing
import random

## third-party libraries
import discord

## custom libraries
if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from bot.Kanrisha import Kanrisha

from handlers.gachaHandler import spin_wheel

class slashCommandHandler:

    """
    
    Handles slash commands.\n

    """


##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_kanrisha_client:Kanrisha) -> None:

        """
        
        Initializes the slash command handler.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        kanrisha_client = inc_kanrisha_client


        ##-------------------start-of-translate_menu()--------------------------------------------------------------

        @kanrisha_client.tree.command(name="translate", description="Translates a message from Japanese to English")
        async def translate(interaction: discord.Interaction, message: str):
            await interaction.response.send_message(str(message) + " was altered", ephemeral=True)

        ##-------------------start-of-translate_menu()--------------------------------------------------------------

        @kanrisha_client.tree.context_menu(name = "translate")
        async def translate_menu(interaction: discord.Interaction, message: discord.Message):
            await interaction.response.send_message(str(message.content) + " was altered", ephemeral=True) 

        ##-------------------start-of-spin()------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="spin", description="Spins a wheel")
        async def spin(interaction: discord.Interaction):


            await interaction.response.send_message(spin_wheel())


        @kanrisha_client.tree.command(name="multispin", description="Spins a wheel 10 times")
        async def multi_spin(interaction: discord.Interaction):

            multi_spin = ""
            for i in range(0, 10):
                multi_spin += spin_wheel()

            await interaction.response.send_message(multi_spin)