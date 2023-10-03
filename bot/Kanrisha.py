## built-in libraries
from datetime import datetime, timedelta

import asyncio

## third-party libraries
from discord.ext import tasks

import discord

## custom modules
from modules.fileEnsurer import fileEnsurer
from modules.toolkit import toolkit

from handlers.slashCommandHandler import slashCommandHandler

from handlers.interactionHandler import interactionHandler

from handlers.remoteHandler import remoteHandler

##-------------------start-of-Kanrisha--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Kanrisha(discord.Client):

    """
    
    Client for "The Gamemaster" Discord bot. Referred to as Kanrisha internally.\n

    """


##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self) -> None:

        """

        Initializes the Kanrisha client.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        intents = discord.Intents.default()
        intents.members = True  ## to receive member related events
        intents.guild_messages = True  ## to receive guild message related events
        intents.message_content = True  ## to receive message content related events

        super().__init__(intents=intents)

        #------------------------------------------------------

        ## tree for slash commands
        self.tree = discord.app_commands.CommandTree(self)

        ## sets the activity currently "Watching you all."
        self.activity = discord.Activity(name='you all.', type=discord.ActivityType.watching)

        ## PIG GUILD ID
        self.pg = 1143635379262607441

        ## KANRISHA LOG CHANNEL ID
        self.log_channel_id = 1149433554170810459

        self.view_dict = {}

        #------------------------------------------------------

        self.file_ensurer = fileEnsurer()

        self.toolkit = toolkit(self.file_ensurer.logger)

        #------------------------------------------------------

        self.interaction_handler = interactionHandler(self.file_ensurer, self.toolkit)

        self.remote_handler = remoteHandler(self.file_ensurer, self.toolkit)

        ## Kanrisha and the slash command handler are coupled, as the slash command handler needs an instance of Kanrisha for it's function decorators to work
        self.slash_command_handler = slashCommandHandler(self)

    ##-------------------start-of-check_if_registered()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def check_if_registered(self, interaction:discord.Interaction, register_check:bool = False):

        """

        Checks if the user is registered.\n

        register_check is used to determine if the check is for the register command. In which case the function is inverted.\n

        Parameters:\n
        interaction (object - discord.Interaction) : the interaction object.\n
        register_check (bool) : whether or not the check is for the register command.\n

        Returns:\n
        None.\n

        """

        registered_member_ids = [member.member_id for member in self.remote_handler.member_handler.members]

        if(interaction.user.id not in registered_member_ids):

            if(register_check == False):
                error_message = "You are not registered. Please use the /register command to register."

                await self.interaction_handler.send_response_no_filter_channel(interaction, response=error_message, delete_after=5.0, is_ephemeral=True)

            return False
        
        else:
            return True

##-------------------start-of-run_post_init_tasks()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def run_post_init_tasks(self) -> None:

        """
        
        Runs the post initialization tasks. Tasks that need to be done after the object and it's handlers are created, but before the object can be used.\n

        Parameters:\n
        self (object - Kanrisha): The Kanrisha client.\n

        Returns:\n
        None.\n

        """

        try:

            ## loads the remote storage
            await self.remote_handler.load_remote_storage()

        ## if it breaks, reset remote but do not fill it, load backup from local, and refresh remote
        except:

            await self.file_ensurer.logger.log_action("ERROR", "Kanrisha", "Failed to load remote storage. Resetting remote storage.")

            await self.remote_handler.delete_remote_storage()
            await self.remote_handler.create_remote_storage()

            await self.remote_handler.load_local_storage()

            await self.refresh_remote_storage()

            await self.file_ensurer.logger.log_action("WARNING", "Kanrisha", "Remote storage reset with local storage.")

        ## setups moderation tasks
        await self.slash_command_handler.event_handler.setup_moderation()
    
##-------------------start-of-on_ready()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def on_ready(self) -> None:

        """

        Gets the bot ready.\n

        Parameters:\n
        self (object - Kanrisha): The Kanrisha client.\n

        Returns:\n
        None.\n

        """

        await self.run_post_init_tasks()

        ## syncs the command tree
        await self.tree.sync()

        ## starts the remote storage refresh task
        if(not self.refresh_remote_storage.is_running()):
            self.refresh_remote_storage.start()

        ## starts the log file sending task
        if(not self.send_log_file_to_log_channel.is_running()):
            self.send_log_file_to_log_channel.start()

        ## starts the freebie reset task
        if(not self.check_for_freebie_reset.is_running()):
            self.check_for_freebie_reset.start()

        ## starts the aibgMember name sync task
        if(not self.sync_aibgMember_names.is_running()):
            self.sync_aibgMember_names.start()

        await self.file_ensurer.logger.log_action("INFO", "Kanrisha", "Kanrisha is ready.")

        await self.wait_until_ready()

##-------------------start-of-refresh_remote_storage()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @tasks.loop(minutes=5)
    async def refresh_remote_storage(self):

        """

        Refreshes the remote storage.\n
        Runs every 5 minutes.\n

        Parameters:\n
        self (object - Kanrisha): The Kanrisha client.\n

        Returns:\n
        None.\n

        """

        await self.remote_handler.reset_remote_storage(is_forced = False)

##-------------------start-of-send_log_file_to_log_channel()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @tasks.loop(minutes=15)
    async def send_log_file_to_log_channel(self):

        """

        Sends the log file to the log channel.\n
        Runs every 15 minutes.\n

        Parameters:\n
        self (object - Kanrisha): The Kanrisha client.\n

        Returns:\n
        None.\n

        """

        await self.interaction_handler.send_log_file(channel=self.get_channel(self.log_channel_id), is_forced = False) ## type: ignore

##-------------------start-of-sync_aibgMember_names()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @tasks.loop(minutes=10)
    async def sync_aibgMember_names(self):

        """
        
        Syncs the names of the members in the aibgMember list.\n

        Parameters:\n
        self (object - Kanrisha): The Kanrisha client.\n

        Returns:\n
        None.\n

        """

        await self.file_ensurer.logger.log_action("INFO", "Kanrisha", "Syncing aibgMember names...")

        for member in self.remote_handler.member_handler.members:
            user = await self.fetch_user(member.member_id)
            member.member_name = user.name
            await asyncio.sleep(5)

        await self.file_ensurer.logger.log_action("INFO", "Kanrisha", "aibgMember names synced.")

##-------------------start-of-check_for_freebie_reset()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @tasks.loop(minutes=5)
    async def check_for_freebie_reset(self) -> None:

        """

        Checks if the freebie reset is due.\n

        Parameters:\n
        self (object - Kanrisha): The Kanrisha client.\n

        Returns:\n
        None.\n

        """

        with open(self.file_ensurer.last_freebie_path, 'r') as freebie_reset_file:
            time_provided_str = freebie_reset_file.read()

        time_provided = datetime.strptime(time_provided_str, '%Y-%m-%d %H:%M:%S')

        ## Get the current time in UTC
        current_time = datetime.utcnow()

        ## Calculate the time difference between the current time and the time you provided
        time_difference = current_time - time_provided

        ## Check if it's been exactly or more than 24 hours
        has_been_24_hours = time_difference >= timedelta(hours=24)

        if(has_been_24_hours):

            ## reset freebie
            for member in self.remote_handler.member_handler.members:
                member.has_freebie = True

            ## write the current time to the file
            with open(self.file_ensurer.last_freebie_path, 'w') as freebie_reset_file:
                freebie_reset_file.write(current_time.strftime('%Y-%m-%d %H:%M:%S'))

            await self.file_ensurer.logger.log_action("INFO", "Kanrisha", "Freebie reset.")
