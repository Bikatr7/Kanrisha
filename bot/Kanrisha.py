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

        self.synced = False

        self.pg = 1143635379262607441

        #------------------------------------------------------

        self.file_ensurer = fileEnsurer()

        self.toolkit = toolkit(self.file_ensurer.logger)

        #------------------------------------------------------

        self.interaction_handler = interactionHandler()
        self.gacha_handler = gachaHandler()

        self.remote_handler = remoteHandler(self.file_ensurer, self.toolkit)

        ## Kanrisha and the slash command handler are coupled, as the slash command handler needs an instance of Kanrisha for it's function decorators to work
        self.slash_command_handler = slashCommandHandler(self)

##-------------------start-of-run_post_init_tasks()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def run_post_init_tasks(self) -> None:

        """
        
        Runs the post initialization tasks.\n

        Parameters:\n
        self (object - Kanrisha): The Kanrisha client.\n

        Returns:\n
        None.\n

        """

        await self.remote_handler.member_handler.load_members()

        await self.slash_command_handler.event_handler.setup_moderation()
    
##-------------------start-of-on_ready()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def on_ready(self) -> None:

        """

        Prints a message to the console when the bot is ready.\n

        Parameters:\n
        self (object - Kanrisha): The Kanrisha client.\n

        Returns:\n
        None.\n

        """

        await self.run_post_init_tasks()

        await self.wait_until_ready()

        if(not self.synced):
            await self.tree.sync()
            self.synced = True

        self.refresh_remote_storage.start()

        timestamp = await self.toolkit.get_timestamp("INFO", "Kanrisha")

        print(timestamp + " Kanrisha is ready.")

##-------------------start-of-refresh_remote_storage()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @tasks.loop(seconds=300)
    async def refresh_remote_storage(self):

        """

        Refreshes the remote storage.\n
        Runs every 5 minutes.\n

        Parameters:\n
        self (object - Kanrisha): The Kanrisha client.\n

        Returns:\n
        None.\n

        """

        await self.remote_handler.reset_remote_storage()