## built-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing
import random

## third-party libraries
import discord

## custom libraries
if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from bot.Kanrisha import Kanrisha

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

        ##-------------------start-of-spin()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="spin", description="Spins a wheel")
        async def spin(interaction: discord.Interaction):

            """
            
            Spins a wheel.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            spin_result = kanrisha_client.gacha_handler.spin_wheel()

            await kanrisha_client.interaction_handler.send_response_filter_channel(interaction, spin_result)

        ##-------------------start-of-multispin()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="multispin", description="Spins a wheel 10 times")
        async def multi_spin(interaction: discord.Interaction):

            """

            Spins a wheel 10 times.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            multi_spin = ""
            
            for i in range(0, 10):
                multi_spin += kanrisha_client.gacha_handler.spin_wheel()

            await kanrisha_client.interaction_handler.send_response_filter_channel(interaction, multi_spin)