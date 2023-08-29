## third-party libraries
import discord

## custom modules
from modules.fileEnsurer import fileEnsurer
from modules.toolkit import toolkit

from handlers.slashCommandHandler import slashCommandHandler
from handlers.interactionHandler import interactionHandler
from handlers.gachaHandler import gachaHandler

##-------------------start-of-Kanrisha--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Kanrisha(discord.Client):

    """
    
    Client for "The Gamemaster" Discord bot. Referred to as Kanrisha internally.\n

    """


##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self):

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

        #------------------------------------------------------

        self.file_ensurer = fileEnsurer()

        self.file_ensurer.ensure_files()

        self.toolkit = toolkit(self.file_ensurer)

        #------------------------------------------------------

        self.slash_command_handler = slashCommandHandler(self)
        self.interaction_handler = interactionHandler()
        self.gacha_handler = gachaHandler()
    
##-------------------start-of-on_ready()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def on_ready(self):

        """

        Prints a message to the console when the bot is ready.\n

        Parameters:\n
        self (object - Kanrisha): The Kanrisha client.\n

        Returns:\n
        None.\n

        """

        await self.wait_until_ready()

        if(not self.synced):
            await self.tree.sync()
            self.synced = True

        print('The Gamemaster is ready.')