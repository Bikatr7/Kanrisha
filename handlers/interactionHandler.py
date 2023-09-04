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
        
        self.whitelisted_channel_names = ["#general-bot", "#bot-testing", "#syndicate-bot"]
        self.whitelisted_channel_ids = [1144136660691460126, 1146174110548901979, 1146922710698557560]  

        self.admin_user_ids = [957451091748986972, 277933921315061761]
        self.admin_usernames = ["seinu", "tommy.3"]

        self.owner_id = 957451091748986972

##-------------------start-of-send_response_filter_channel()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def send_response_filter_channel(self, interaction:discord.Interaction, response: typing.Union[str, None] = None, embed: typing.Union[discord.Embed, None] = None, view: typing.Union[discord.ui.View , None] = None, is_admin_only:bool = False, delete_after: typing.Union[float , None] = None, is_ephemeral:bool = False) -> None:

        """

        Sends a response to a channel.\n

        Parameters:\n
        self (object - interactionHandler) : the interactionHandler object.\n
        interaction (object - discord.Interaction) : the interaction object.\n
        response (str | optional) : the response to send.\n
        is_admin_only (bool | optional) : whether or not to restrict the command to admins only.\n
        delete_after (float | optional) : how long to wait before deleting the message.\n
        is_ephemeral (bool | optional) : whether or not to make the message ephemeral.\n

        Returns:\n
        None.\n

        """

        ## admin check
        if(interaction.user.id not in self.admin_user_ids and is_admin_only):
            await interaction.response.send_message("You do not have permission to use this command.", delete_after=3.0, ephemeral=True)
            return
        
        ## if correct channel or admin, send response
        if(interaction.channel_id in self.whitelisted_channel_ids or interaction.user.id in self.admin_user_ids):

            if(embed and view):
                await interaction.response.send_message(embed=embed, view=view, delete_after=delete_after, ephemeral=is_ephemeral)

            elif(embed):
                await interaction.response.send_message(embed=embed, delete_after=delete_after, ephemeral=is_ephemeral)
            
            elif(response):
                await interaction.response.send_message(response, delete_after=delete_after, ephemeral=is_ephemeral)

            else:
                raise Exception("No response, embed, or view was provided.")

        else:

            await interaction.response.send_message(f"Please use {str(self.whitelisted_channel_names)} for this command.", delete_after=5.0, ephemeral=True)

##-------------------start-of-send_response_no_filter_channel()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def send_response_no_filter_channel(self, interaction:discord.Interaction, response: typing.Union[str , None] = None, embed: typing.Union[discord.Embed , None] = None, view: typing.Union[discord.ui.View , None] = None, is_admin_only:bool = False, delete_after: typing.Union[float , None] = None, is_ephemeral:bool = False) -> None:

        """

        Sends a response to a channel without filtering.\n

        Parameters:\n
        self (object - interactionHandler) : the interactionHandler object.\n
        interaction (object - discord.Interaction) : the interaction object.\n
        response (str | optional) : the response to send.\n
        is_admin_only (bool | optional) : whether or not to restrict the command to admins only.\n
        delete_after (float | optional) : how long to wait before deleting the message.\n
        is_ephemeral (bool | optional) : whether or not to make the message ephemeral.\n

        Returns:\n
        None.\n

        """

        ## admin check
        if(interaction.user.id not in self.admin_user_ids and is_admin_only):
            await interaction.response.send_message("You do not have permission to use this command.", delete_after=3.0, ephemeral=True)
            return

        else:

            if(embed and view):
                await interaction.response.send_message(embed=embed, view=view, delete_after=delete_after, ephemeral=is_ephemeral)

            elif(embed):
                await interaction.response.send_message(embed=embed, delete_after=delete_after, ephemeral=is_ephemeral)
            
            elif(response):
                await interaction.response.send_message(response, delete_after=delete_after, ephemeral=is_ephemeral)

            else:
                raise Exception("No response, embed, or view was provided.")
            
##-------------------start-of-send_response_no_filter_channel()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def send_message_to_channel(self, channel:typing.Union[discord.channel.GroupChannel , discord.Thread], response: typing.Union[str , None] = None, embed: typing.Union[discord.Embed , None] = None, view: typing.Union[discord.ui.View , None] = None, delete_after: typing.Union[float , None] = None) -> None:

        """

        Sends a response to a channel.\n

        Parameters:\n
        self (object - interactionHandler) : the interactionHandler object.\n
        channel (object - discord.channel.GroupChannel | discord.Thread) : the channel to send the message to.\n
        response (str | optional) : the response to send.\n
        delete_after (float | optional) : how long to wait before deleting the message.\n
    
        Returns:\n
        None.\n

        """

        ## magic dict bullshit to make this work
        send_args = {}

        if(embed):
            send_args['embed'] = embed

        if(view):
            send_args['view'] = view

        if(delete_after):
            send_args['delete_after'] = delete_after

        ## Send the message based on the provided arguments
        if(embed or view or response):
            await channel.send(response or "", **send_args)

        else:
            raise Exception("No response, embed, or view was provided.")
