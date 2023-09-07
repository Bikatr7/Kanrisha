## built-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing
import asyncio

## third-party libraries
import discord

## custom libraries
if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from bot.Kanrisha import Kanrisha

class adminCommandHandler:

    """
    
    Handles slash commands.\n

    """


##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_kanrisha_client:Kanrisha) -> None:

        """
        
        Initializes the slash command handler.\n

        Parameters:\n
        inc_kanrisha_client (Kanrisha): The client object.\n

        Returns:\n
        None.\n

        """

        kanrisha_client = inc_kanrisha_client

        ##-------------------start-of-force-log-push()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="force-log-push", description="Forces a log push.")
        async def force_log_push(interaction:discord.Interaction):

            """
            
            Forces a log push.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            ## admin check
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
                await interaction.response.send_message("You do not have permission to use this command.", delete_after=3.0, ephemeral=True)
                return

            await kanrisha_client.interaction_handler.send_log_file(kanrisha_client.get_channel(kanrisha_client.log_channel_id), is_forced=True,  forced_by=interaction.user.name)  # type: ignore

        ##-------------------start-of-force-remote-reset()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="force-remote-reset", description="Resets the remote storage.")
        async def force_remote_reset(interaction:discord.Interaction):

            """
            
            Resets the remote storage.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            ## admin check
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
                await interaction.response.send_message("You do not have permission to use this command.", delete_after=3.0, ephemeral=True)
                return

            await kanrisha_client.remote_handler.reset_remote_storage(is_forced=True, forced_by=interaction.user.name)

            await interaction.response.send_message("Remote storage has been reset.", delete_after=3.0, ephemeral=True)
    
        ##-------------------start-of-execute_order_66()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="execute-order-66", description="It is time.")
        async def execute_order_66(interaction:discord.Interaction, ban_reason:str, ban_message:str):

            """
            
            Executes order 66.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n
            ban_reason (str) : the reason for the ban.\n
            ban_message (str) : the message to send to the banned users.\n

            Returns:\n
            None.\n

            """

            ## admin check
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
                await interaction.response.send_message("You do not have permission to use this command.", delete_after=3.0, ephemeral=True)
                return

            ## marked ids
            marked_for_death_role_id = 1146651136363855982
            mark_of_silence_role_id = 1147336187888021524

            ## server announcements role
            role_to_ping = kanrisha_client.get_guild(interaction.guild_id).get_role(1147346384178131034) ## type: ignore (we know it's not None)
            role_ping = role_to_ping.mention ## type: ignore (we know it's not None)

            mark_of_silence_role = kanrisha_client.get_guild(interaction.guild_id).get_role(mark_of_silence_role_id) ## type: ignore (we know it's not None)

            marked_for_death: typing.List[discord.Member] = []

            execution_message = "The following users have been marked for death and will be banned:\n"

            for guild in kanrisha_client.guilds:
                
                for member in guild.members:

                    member_role_ids = [role.id for role in member.roles]

                    if(marked_for_death_role_id in member_role_ids):
                        marked_for_death.append(member)
                        execution_message += f"{member.mention}\n"

            ## no one to ban 
            if(len(marked_for_death) == 0):
                execution_message = "No users have been marked for death."
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, execution_message, delete_after=5.0, is_ephemeral=True)
                return
            
            mention_content = f"\nPinging : {role_ping}"
            
            embed = discord.Embed(title="Order 66.", description=execution_message, color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)
            embed.set_footer(text=f"Ban Reason : {ban_reason}\n\nBanning in 30 seconds, please standby...") 

            target_channel = kanrisha_client.get_channel(interaction.channel_id) ## type: ignore (we know it's not None)

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed)
            await kanrisha_client.interaction_handler.send_message_to_channel(target_channel, mention_content) ## type: ignore (we know it's not None)

            ## ban loop
            for i in range(30):
                await asyncio.sleep(1)
                
                for member in marked_for_death:
                    
                    member_role_ids = [role.id for role in member.roles]

                    if member.typing and mark_of_silence_role_id not in member_role_ids:

                        silence_message = f"{member.mention} has been silenced..."

                        await member.add_roles(mark_of_silence_role)  # type: ignore (we know it's not None)
                        await kanrisha_client.interaction_handler.send_message_to_channel(target_channel, silence_message) ## type: ignore (we know it's not None)
                
                if(20 <= i < 30):
                    await interaction.followup.send(f"Banning in {30 - i} seconds...")


            for member in marked_for_death:
                
                try:
                    await member.send(f"You have been banned from Psychology Game for the following reason:\n{ban_reason}\n\nNote: {ban_message}")
                
                except:
                    pass

                try:
                    await member.ban(reason=ban_reason, delete_message_days=0)
                except:
                    pass

            member_string1 = "The following users have been banned:\n"

            member_string2 = [member.display_name + "\n" for member in marked_for_death]

            member_string = member_string1 + "".join(member_string2)

            embed = discord.Embed(title="Order 66 has been executed.", description=member_string, color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)
            embed.set_footer(text="Thank you for your cooperation...")

            await interaction.followup.send(embed=embed)
