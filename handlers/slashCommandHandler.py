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

            await kanrisha_client.interaction_handler.send_response_filter_channel(interaction, spin_result, embed=None, view=None)

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

            await kanrisha_client.interaction_handler.send_response_filter_channel(interaction, multi_spin, embed=None, view=None)

        ##-------------------start-of-register()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="register", description="Registers a user to the bot.")
        async def register(interaction: discord.Interaction):

            """
            
            Registers a user to the bot, currently only admits the user to the bot's testing phase.\n

            """

            register_message = """
            By clicking this button you acknowledge and agree to the following:\n
            - Your Discord username and ID will be stored in a database.\n
            - Your Discord username and ID will be used for bot functionality.\n
            - You will be using the bot during its testing phase, and any and all data may be wiped/lost at any time.\n
            - You will not hold the bot owner responsible for any data loss.\n
            """

            embed = discord.Embed(title="Register", description=register_message, color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)
            embed.set_footer(text="This message will be deleted in 60 seconds.")

            view = discord.ui.View().add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id="register", label="Register"))

            await kanrisha_client.interaction_handler.send_response_filter_channel(interaction, response="", embed=embed, view=view, admin_only=True)

        ##-------------------start-of-on_interaction()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        @kanrisha_client.event
        async def on_interaction(interaction: discord.Interaction):

            """

            Handles button interactions.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """


            ## check if it's a button press
            if(interaction.type == discord.InteractionType.component):  

                ## get the custom id of the button
                custom_id = interaction.data.get("custom_id") if interaction.data else None

                ## if register button was pressed
                if(custom_id == "register"):

                    ## acknowledge the interaction immediately
                    await interaction.response.defer()

                    await interaction.followup.send("You clicked the register button!")


