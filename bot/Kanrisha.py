## third-party libraries
from discord.ext import tasks

import discord

## custom modules
from modules.fileEnsurer import fileEnsurer
from modules.toolkit import toolkit

from handlers.slashCommandHandler import slashCommandHandler

from handlers.interactionHandler import interactionHandler
from handlers.gachaHandler import gachaHandler

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

        #------------------------------------------------------

        self.file_ensurer = fileEnsurer()

        self.toolkit = toolkit(self.file_ensurer.logger)

        #------------------------------------------------------

        self.interaction_handler = interactionHandler(self.file_ensurer, self.toolkit)
        self.gacha_handler = gachaHandler()

        self.remote_handler = remoteHandler(self.file_ensurer, self.toolkit)

        ## Kanrisha and the slash command handler are coupled, as the slash command handler needs an instance of Kanrisha for it's function decorators to work
        self.slash_command_handler = slashCommandHandler(self)

##-------------------start-of-run_post_init_tasks()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def run_post_init_tasks(self) -> None:

        """
        
        Runs the post initialization tasks. Tasks that need to be done after the object and it's handlers are created, but before the object can be used.\n

        Parameters:\n
        self (object - Kanrisha): The Kanrisha client.\n

        Returns:\n
        None.\n

        """

        ## loads the members from the remote storage
        await self.remote_handler.member_handler.load_members_from_remote()

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

        ## starts the role persistence database sync task
        if(not self.sync_role_persistence_database.is_running()):
            self.sync_role_persistence_database.start()

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

##-------------------start-of-sync_role_persistence_database()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @tasks.loop(minutes=5)
    async def sync_role_persistence_database(self):

        """

        Syncs the role persistence database.\n
        Runs every 5 minutes.\n

        Parameters:\n
        self (object - Kanrisha): The Kanrisha client.\n

        Returns:\n
        None.\n

        """

        members = [member for member in self.get_all_members()]

        await self.interaction_handler.sync_roles_logic(members, is_forced = False)

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