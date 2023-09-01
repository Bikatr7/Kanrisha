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
    
    Handles events.\n
    
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

        archive_channel_id = 1146979933416067163

        self.syndicate_role = 1146901009248026734

        ##-------------------start-of-on_raw_message_delete()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.event
        async def on_raw_message_delete(payload: discord.RawMessageDeleteEvent):

            """

            Stores deleted messages in a channel for later.\n

            Parameters:\n
            self (object) : the eventHandler object.\n

            Returns:\n
            None.\n

            """

            ## check if the message was cached and if it was not sent by a bot
            if(payload.cached_message and not payload.cached_message.author.bot):
                store_channel = kanrisha_client.get_channel(archive_channel_id)

                message_cache = payload.cached_message
                message_content = message_cache.content

                if(len(message_cache.attachments) > 0):
                    for attachment in message_cache.attachments:
                        message_content += "\n" + str(attachment)

                embed = discord.Embed(title=message_cache.author.name, description=message_content, color=0xC0C0C0)

                if(message_cache.author.avatar):
                    embed.set_thumbnail(url=message_cache.author.avatar.url)

                embed.set_footer(text=f'Deleted in #{message_cache.channel.name} at {message_cache.created_at.now().strftime("%Y-%m-%d %H:%M:%S")}') ## type: ignore (we know it's not None)
                embed.add_field(name="Channel ID", value=message_cache.channel.id)
                embed.add_field(name="User ID", value=message_cache.author.id)


                await kanrisha_client.interaction_handler.send_message_to_channel(store_channel, embed=embed) ## type: ignore (we know it's not None)

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
                if(custom_id == f"register_{interaction.user.id}"):

                    syndicate_role = kanrisha_client.get_guild(interaction.guild_id).get_role(self.syndicate_role) ## type: ignore (we know it's not None)

                    ## acknowledge the interaction immediately
                    await interaction.response.defer()

                    await kanrisha_client.member_handler.add_new_member(interaction.user.id, interaction.user.name, tuple([0,0,0]),0)

                    await interaction.delete_original_response()

                    await interaction.followup.send("You have been registered.", ephemeral=True)

                    await interaction.user.add_roles(syndicate_role) ## type: ignore (we know it's not None)

                ## if register button was pressed by the wrong user
                elif custom_id and custom_id.startswith("register_"):

                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not authorized to use this button.", delete_after=5.0, is_ephemeral=True)


