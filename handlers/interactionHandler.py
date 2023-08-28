## third-party libraries
import discord


class interactionHandler:

    """
    
    Handles interactions, mostly responses to slash commands.\n
    
    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self) -> None:

        """

        Initializes the interaction handler.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        self.bot_channel_id = 1144136660691460126

        self.bot_channel_name = "#general-bot"

##-------------------start-of-send_response_filter_channel()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def send_response_filter_channel(self, interaction:discord.Interaction, response:str) -> None:

        """

        Sends a response to a channel.\n

        Parameters:\n
        interaction (object - discord.Interaction) : the interaction object.\n
        response (str) : the response to send.\n

        Returns:\n
        None.\n

        """

        if(interaction.channel_id == self.bot_channel_id):
            await interaction.response.send_message(response)

        else:
            await interaction.response.send_message(f"Please use {self.bot_channel_name} for this command.", delete_after=3.0)

##-------------------start-of-send_response_no_filter_channel()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def send_response_no_filter_channel(self, interaction:discord.Interaction, response:str) -> None:

        """

        Sends a response to a channel.\n

        Parameters:\n
        interaction (object - discord.Interaction) : the interaction object.\n
        response (str) : the response to send.\n

        Returns:\n
        None.\n

        """

        await interaction.response.send_message(response)
    