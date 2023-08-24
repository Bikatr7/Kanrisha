## built-in modules
import os

## third-party modules
from discord.ext import commands 
from discord import app_commands

import discord

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

        self.synced = False

        activity = discord.Activity(name='/translate', type=discord.ActivityType.watching)

        self.activity = activity

        self.tree = discord.app_commands.CommandTree(self)

    
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

##-------------------start-of-main()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

client = Kanrisha()

#-------------------start-of-on_message()--------------------------------------------------------------

@client.event
async def on_message(message):
    
    if(message.content == "hi"):
        await message.channel.send('Hello, world!')

@client.tree.command(name="translate", description="Translates a message from Japanese to English")
async def translate(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(str(message) + " was altered", ephemeral=True)

#-------------------start-of-translate_menu()--------------------------------------------------------------

@client.tree.context_menu(name = "translate")
async def translate_menu(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(str(message.content) + " was altered", ephemeral=True) 

##-------------------start-of-run()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

token = ""

client.run(token=token)