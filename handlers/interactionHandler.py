## built-in libraries
import typing

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

        self.whitelisted_channel_names = ["#general-bot", "#bot-testing"]

        self.whitelisted_channel_ids = [1144136660691460126, 1146174110548901979]

        self.admin_user_ids = [957451091748986972]
        self.admin_usernames = ["seinu"]

##-------------------start-of-send_response_filter_channel()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def send_response_filter_channel(self, interaction:discord.Interaction, response:str, embed:typing.Optional[discord.Embed], view:typing.Optional[discord.ui.View], admin_only=False) -> None:

        """

        Sends a response to a channel.\n

        Parameters:\n
        self (object - interactionHandler) : the interactionHandler object.\n
        interaction (object - discord.Interaction) : the interaction object.\n
        response (str) : the response to send.\n
        admin_only (bool | optional) : whether or not to restrict the command to admins only.\n

        Returns:\n
        None.\n

        """

        ## admin check
        if(interaction.user.id not in self.admin_user_ids and admin_only):
            await interaction.response.send_message("You do not have permission to use this command.", delete_after=3.0)


        ## if correct channel or admin, send response
        if(interaction.channel_id in self.whitelisted_channel_ids or interaction.user.id in self.admin_user_ids):

            if(embed and view):
                await interaction.response.send_message(embed=embed, view=view)

            elif(embed):
                await interaction.response.send_message(embed=embed)
            
            else:
                await interaction.response.send_message(response)

        else:
            await interaction.response.send_message(f"Please use {self.whitelisted_channel_names[0]} for this command.", delete_after=3.0)

##-------------------start-of-send_response_no_filter_channel()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def send_response_no_filter_channel(self, interaction:discord.Interaction, response:str, admin_only=False) -> None:

        """

        Sends a response to a channel.\n

        Parameters:\n
        self (object - interactionHandler) : the interactionHandler object.\n
        interaction (object - discord.Interaction) : the interaction object.\n
        response (str) : the response to send.\n
        admin_only (bool | optional) : whether or not to restrict the command to admins only.\n

        Returns:\n
        None.\n

        """

        ## admin check
        if(interaction.user.id not in self.admin_user_ids and admin_only):
            await interaction.response.send_message("You do not have permission to use this command.", delete_after=3.0)

        await interaction.response.send_message(response)
    