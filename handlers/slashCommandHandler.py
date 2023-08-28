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

            chances = {"<:shining:1144089713934864444>": 0.05, "<:glowing:1144089680934080512>": 0.12, "<:common:1144089649174814730>": 0.83}
            
            # Generate a random number between 0 and 1
            random_number = random.random()
            
            # Initialize a variable to keep track of the cumulative probability
            cumulative_probability = 0
            
            # Iterate through the chances and select a value based on the probabilities
            for value, probability in chances.items():
                cumulative_probability += probability
                if(random_number < cumulative_probability):
                    await interaction.response.send_message(value)
                    break