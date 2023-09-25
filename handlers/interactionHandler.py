## built-in libraries
import typing
import json

## third-party libraries
import discord

## custom modules
from modules.fileEnsurer import fileEnsurer
from modules.toolkit import toolkit

class interactionHandler:

    """
    
    Handles interactions, mostly responses to slash commands.\n
    
    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_file_ensurer:fileEnsurer, inc_toolkit:toolkit) -> None:

        """

        Initializes the interaction handler.\n

        Parameters:\n
        inc_file_ensurer (object - fileEnsurer) : the fileEnsurer object.\n
        inc_toolkit (object - toolkit) : the toolkit object.\n

        Returns:\n
        None.\n

        """
        
        self.file_ensurer = inc_file_ensurer
        self.toolkit = inc_toolkit

        self.whitelisted_channel_names = ["#general-bot", "#bot-testing", "#syndicate-bot"]
        self.whitelisted_channel_ids = [1144136660691460126, 1146174110548901979, 1146922710698557560]  

        self.admin_user_ids = [957451091748986972, 277933921315061761, 125751325760684033, 1146646164838555699, 1144166968979628072]
        self.admin_usernames = ["seinu", "tommy.3", "lombardia","dairinyn", "kanrisha"]

        self.owner_id = 957451091748986972

##-------------------start-of-send_response_filter_channel()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def send_response_filter_channel(self, 
                                           interaction:discord.Interaction, 
                                           response: typing.Union[str, None] = None, 
                                           embed: typing.Union[discord.Embed, None] = None, 
                                           view: typing.Union[discord.ui.View , None] = None, 
                                           file:typing.Union[discord.File , None] = None, 
                                           delete_after: typing.Union[float , None] = None, 
                                           is_ephemeral:bool = False) -> None:

        """

        Sends a response to a channel with filtering.\n

        Parameters:\n
        self (object - interactionHandler) : the interactionHandler object.\n
        interaction (object - discord.Interaction) : the interaction object.\n
        response (str | optional) : the response to send.\n
        embed (object - discord.Embed | optional) : the embed to send.\n
        view (object - discord.ui.View | optional) : the view to send.\n
        file (object - discord.File | optional) : the file to send.\n
        delete_after (float | optional) : how long to wait before deleting the message.\n
        is_ephemeral (bool | optional) : whether or not to make the message ephemeral.\n

        Returns:\n
        None.\n

        """

        ## if not correct channel and not admin, send response
        if(interaction.channel_id not in self.whitelisted_channel_ids and interaction.user.id not in self.admin_user_ids):
            await interaction.response.send_message(f"Please use {str(self.whitelisted_channel_names)} for this command.", delete_after=5.0, ephemeral=True)
            return
        
        send_args = {}

        if(response):
            send_args['content'] = response

        if(embed):
            send_args['embed'] = embed

        if(view):
            send_args['view'] = view

        if(file):
            send_args['file'] = file

        if(delete_after):
            send_args['delete_after'] = delete_after

        if(is_ephemeral):
            send_args['ephemeral'] = is_ephemeral

        if(response or embed or view or file):
            await interaction.response.send_message(**send_args)

        else:
            raise Exception("No response, embed, view, or file was provided.")

##-------------------start-of-send_response_no_filter_channel()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def send_response_no_filter_channel(self, 
                                              interaction:discord.Interaction, 
                                              response:typing.Union[str , None] = None, 
                                              embed:typing.Union[discord.Embed , None] = None, 
                                              view:typing.Union[discord.ui.View , None] = None, 
                                              file:typing.Union[discord.File , None] = None, 
                                              delete_after:typing.Union[float , None] = None, 
                                              is_ephemeral:bool = False) -> None:

        """

        Sends a response to a channel without filtering.\n

        Parameters:\n
        self (object - interactionHandler) : the interactionHandler object.\n
        interaction (object - discord.Interaction) : the interaction object.\n
        response (str | optional) : the response to send.\n
        embed (object - discord.Embed | optional) : the embed to send.\n
        view (object - discord.ui.View | optional) : the view to send.\n
        file (object - discord.File | optional) : the file to send.\n
        delete_after (float | optional) : how long to wait before deleting the message.\n
        is_ephemeral (bool | optional) : whether or not to make the message ephemeral.\n

        Returns:\n
        None.\n

        """

        send_args = {}

        if(response):
            send_args['content'] = response

        if(embed):
            send_args['embed'] = embed
        
        if(view):
            send_args['view'] = view

        if(file):
            send_args['file'] = file
        
        if(delete_after):
            send_args['delete_after'] = delete_after

        if(is_ephemeral):
            send_args['ephemeral'] = is_ephemeral

        if(response or embed or view or file):
            await interaction.response.send_message(**send_args)

        else:
            raise Exception("No response, embed, view, or file was provided.")
            
##-------------------start-of-send_response_no_filter_channel()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def send_message_to_channel(self, 
                                      channel:typing.Union[discord.channel.GroupChannel , discord.Thread], 
                                      response:typing.Union[str , None] = None, 
                                      embed:typing.Union[discord.Embed , None] = None, 
                                      view:typing.Union[discord.ui.View , None] = None, 
                                      file:typing.Union[discord.File, None] = None, 
                                      delete_after:typing.Union[float , None] = None) -> None:

        """

        Sends a response to a channel.\n

        Parameters:\n
        self (object - interactionHandler) : the interactionHandler object.\n
        channel (object - discord.channel.GroupChannel | discord.Thread) : the channel to send the message to.\n
        response (str | optional) : the response to send.\n
        embed (object - discord.Embed | optional) : the embed to send.\n
        view (object - discord.ui.View | optional) : the view to send.\n
        file (object - discord.File | optional) : the file to send.\n
        delete_after (float | optional) : how long to wait before deleting the message.\n
    
        Returns:\n
        None.\n

        """

        ## magic dict bullshit to make this work
        send_args = {}

        if(response):
            send_args['content'] = response

        if(embed):
            send_args['embed'] = embed

        if(view):
            send_args['view'] = view

        if(file):
            send_args['file'] = file

        if(delete_after):
            send_args['delete_after'] = delete_after

        ## Send the message based on the provided arguments
        if(response or embed or view or file):
            await channel.send(**send_args)

        else:
            raise Exception("No response, embed, view, or file was provided.")

##-------------------start-of-send_followup_to_interaction()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def send_followup_to_interaction(self,
                                      interaction:discord.Interaction,
                                      response:typing.Union[str , None] = None, 
                                      embed:typing.Union[discord.Embed , None] = None, 
                                      view:typing.Union[discord.ui.View , None] = None, 
                                      file:typing.Union[discord.File, None] = None, 
                                      is_ephemeral:bool = False) -> None:

        """

        Sends a followup to an interaction.\n

        Parameters:\n
        self (object - interactionHandler) : the interactionHandler object.\n
        interaction (object - discord.Interaction) : the interaction object.\n
        response (str | optional) : the response to send.\n
        embed (object - discord.Embed | optional) : the embed to send.\n
        view (object - discord.ui.View | optional) : the view to send.\n
        file (object - discord.File | optional) : the file to send.\n
        delete_after (float | optional) : how long to wait before deleting the message.\n

        Returns:\n
        None.\n

        """

        ## magic dict bullshit to make this work
        send_args = {}

        if(response):
            send_args['content'] = response

        if(embed):
            send_args['embed'] = embed

        if(view):
            send_args['view'] = view

        if(file):
            send_args['file'] = file

        if(is_ephemeral):
            send_args['ephemeral'] = is_ephemeral

        ## Send the message based on the provided arguments
        if(response or embed or view or file):
            await interaction.followup.send(**send_args)

        else:
            raise Exception("No response, embed, view, or file was provided.")

##-------------------start-of-defer_interaction()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    async def defer_interaction(self, 
                                interaction:discord.Interaction, 
                                is_ephemeral:bool = False,
                                is_thinking:bool = False) -> None:
        
        """
        
        Defers an interaction.\n

        Parameters:\n
        self (object - interactionHandler) : the interactionHandler object.\n
        interaction (object - discord.Interaction) : the interaction object.\n
        is_ephemeral (bool | optional) : whether or not to make the message ephemeral.\n
        is_thinking (bool | optional) : whether or not to show the thinking indicator.\n

        Returns:\n
        None.\n

        """

        send_args = {}

        if(is_ephemeral):
            send_args['ephemeral'] = is_ephemeral

        if(is_thinking):
            send_args['thinking'] = is_thinking

        await interaction.response.defer(**send_args)

##-------------------start-of-send-log-file()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def send_log_file(self, channel:typing.Union[discord.channel.GroupChannel , discord.Thread], is_forced:bool, forced_by:str | None = None) -> None:

        """
        
        Sends the log file.\n

        Parameters:\n
        self (object - interactionHandler) : the interactionHandler object.\n

        Returns:\n
        None.\n

        """

        await self.file_ensurer.logger.push_batch()

        await self.send_message_to_channel(channel, file=discord.File(self.file_ensurer.log_path)) ## type: ignore (we know it's not None)

        await self.file_ensurer.logger.clear_log_file()

        if(is_forced):
            await self.file_ensurer.logger.log_action("INFO", "interactionHandler", f"Log file has been forcibly pushed by {forced_by}.")

        else:
            await self.file_ensurer.logger.log_action("INFO", "interactionHandler", "Log file has been pushed.")

##-------------------start-of-sync-roles-logic()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def sync_roles_logic(self, members:typing.List[discord.Member], is_forced:bool, forced_by:str | None = None) -> None:

        """
        
        Syncs the roles of all users in the server with the role persistence database.\n

        Parameters:\n
        self (object - interactionHandler) : the interactionHandler object.\n
        members (list - discord.Member) : the list of members to sync.\n
        is_forced (bool) : whether or not the sync was forced.\n
        forced_by (str | optional) : who forced the sync.\n

        Returns:\n
        None.\n

        """
        

        ## Load the existing data once.
        with open(self.file_ensurer.role_persistence_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}

        for member in members:  ## type: ignore (we know it's not None)
            roles = [role.id for role in member.roles if role != member.guild.default_role]
            data[str(member.id)] = roles

        ## Write the updated data.
        with open(self.file_ensurer.role_persistence_path, 'w') as file:
            json.dump(data, file)

        if(is_forced):
            await self.file_ensurer.logger.log_action("INFO", "interactionHandler", f"Role persistence database has been forcibly synced by {forced_by}.")

        else:
            await self.file_ensurer.logger.log_action("INFO", "interactionHandler", "Role persistence database has been synced.")