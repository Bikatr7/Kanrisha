## built-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing

## third-party libraries
import discord

## custom libraries
if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from bot.Kanrisha import Kanrisha

class eventHandler:
    """
    
    Handles events, besides the interaction event.\n
    
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

        ##-------------------start-of-on_message()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # does nothing yet, but can easily be configured to do so

        @kanrisha_client.event
        async def on_message(message: discord.message):
            pass

        ##-------------------start-of-on_raw_message_delete()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.event
        async def on_raw_message_delete(payload: discord.RawMessageDeleteEvent | None = None):
            if payload.cached_message and payload.cached_message.author.id != 1146086016147538051:
                store_channel = kanrisha_client.get_channel(1146969965786837023)
                message_cache = payload.cached_message
                message_content = message_cache.content
                if len(message_cache.attachments) > 0:
                    message_content += "\n" + [attachment for attachment in message_cache.attachments]
                embed = discord.Embed(title=message_cache.author.name, description=message_content, color=0xC0C0C0)
                if message_cache.author.avatar:
                    embed.set_thumbnail(url=message_cache.author.avatar.url)
                embed.set_footer(text=f'Deleted in #{message_cache.channel.name} at {message_cache.created_at.now().strftime("%Y-%m-%d %H:%M:%S")}')
                await store_channel.send(message_cache.channel.id, embed=embed)

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

                ## if register button was pressed by the correct user
                if custom_id == f"register_{interaction.user.id}":

                    ## acknowledge the interaction immediately
                    await interaction.response.defer()

                    await kanrisha_client.member_handler.add_new_member(interaction.user.id)

                    await interaction.delete_original_response()

                    await interaction.followup.send("You have been registered.", ephemeral=True)

                ## if register button was pressed by the wrong user
                elif custom_id and custom_id.startswith("register_"):

                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not authorized to use this button.", delete_after=5.0, is_ephemeral=True)


