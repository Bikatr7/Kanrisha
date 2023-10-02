## built-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing
import asyncio
import os
import shutil
import tempfile

## third-party libraries
import discord

## custom libraries
if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from bot.Kanrisha import Kanrisha

class adminCommandHandler:

    """
    
    Handles admin slash commands.\n

    """


##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_kanrisha_client:Kanrisha) -> None:

        """
        
        Initializes the admin command handler.\n

        Parameters:\n
        inc_kanrisha_client (Kanrisha): The client object.\n

        Returns:\n
        None.\n

        """

        kanrisha_client = inc_kanrisha_client


##-------------------start-of-trigger_early-shutdown()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def trigger_early_shutdown_logic(interaction:discord.Interaction) -> None:

            """
            
            Triggers an early shutdown.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(not await kanrisha_client.interaction_handler.admin_check(interaction)):
                return

            await kanrisha_client.interaction_handler.defer_interaction(interaction, is_ephemeral=True, is_thinking=True)

            await force_remote_reset_logic(interaction, is_shutdown_protocol=True) 

            await force_log_push_logic(interaction, is_shutdown_protocol=True)

            await kanrisha_client.file_ensurer.logger.log_action("WARNING", "adminCommandHandler", f"Early shutdown triggered by {interaction.user.name}.")

            await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, "Shutting Down.", is_ephemeral=True)

            try:
                ## cancel all tasks
                kanrisha_client.send_log_file_to_log_channel.cancel()
                kanrisha_client.refresh_remote_storage.cancel()
                kanrisha_client.sync_role_persistence_database.cancel()
                kanrisha_client.check_for_freebie_reset.cancel()

                ## try to close gracefully
                await kanrisha_client.close()

                exit()

            ## if we can't close gracefully, just exit
            except:
                exit()

        ##-------------------start-of-force-log-push()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def force_log_push_logic(interaction:discord.Interaction, is_shutdown_protocol:bool | None = False) -> None:

            """
            
            Forces a log push.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n
            is_shutdown_protocol (bool | None) : whether or not this is part of a shutdown protocol.\n

            Returns:\n
            None.\n

            """

            if(not await kanrisha_client.interaction_handler.admin_check(interaction)):
                return
            
            if(not is_shutdown_protocol):
                await kanrisha_client.interaction_handler.defer_interaction(interaction, is_ephemeral=True, is_thinking=True)

            await kanrisha_client.interaction_handler.send_log_file(kanrisha_client.get_channel(kanrisha_client.log_channel_id), is_forced=True,  forced_by=interaction.user.name) ## type: ignore

            if(not is_shutdown_protocol):
                await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, "Log pushed.", is_ephemeral=True)

        ##-------------------start-of-force-remote-reset()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def force_remote_reset_logic(interaction:discord.Interaction, is_shutdown_protocol:bool | None = False) -> None:

            """
            
            Resets the remote storage with the current instance's data.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n
            is_shutdown_protocol (bool | None) : whether or not this is part of a shutdown protocol.\n

            Returns:\n
            None.\n

            """

            if(not await kanrisha_client.interaction_handler.admin_check(interaction)):
                return
            
            if(not is_shutdown_protocol):
                await kanrisha_client.interaction_handler.defer_interaction(interaction, is_ephemeral=True, is_thinking=True)

            await kanrisha_client.remote_handler.reset_remote_storage(is_forced=True, forced_by=interaction.user.name)

            if(not is_shutdown_protocol):
                await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, "Remote reset.", is_ephemeral=True)
            
        ##-------------------start-of-execute_order_66()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="execute-order-66", description="It is time. (ADMIN)")
        async def execute_order_66(interaction:discord.Interaction, ban_reason:str, ban_message:str) -> None:

            """
            
            Executes order 66.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n
            ban_reason (str) : the reason for the ban.\n
            ban_message (str) : the message to send to the banned users.\n

            Returns:\n
            None.\n

            """

            if(not await kanrisha_client.interaction_handler.admin_check(interaction)):
                return

            ## marked ids
            marked_for_death_role_id = 1146651136363855982
            mark_of_silence_role_id = 1147336187888021524

            ## order 66 spectator role
            role_to_ping = kanrisha_client.get_guild(interaction.guild_id).get_role(1147346384178131034) ## type: ignore (we know it's not None)
            role_ping = role_to_ping.mention ## type: ignore (we know it's not None)

            mark_of_silence_role = kanrisha_client.get_guild(interaction.guild_id).get_role(mark_of_silence_role_id) ## type: ignore (we know it's not None)

            marked_for_death: typing.List[discord.Member] = []

            execution_message = "The following users have been marked for death and will be banned:\n"

            ## get all members with the marked for death role
            for guild in kanrisha_client.guilds:
                
                for member in guild.members:

                    member_role_ids = [role.id for role in member.roles]

                    if(marked_for_death_role_id in member_role_ids):
                        marked_for_death.append(member)
                        execution_message += f"{member.mention}\n"

            ## if no one to ban 
            if(len(marked_for_death) == 0):
                execution_message = "No users have been marked for death."
                await kanrisha_client.file_ensurer.logger.log_action("WARNING", "adminCommandHandler", execution_message)
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
                
                ## countdown for ban (last 10 seconds)
                if(20 <= i < 30):
                    await interaction.followup.send(f"Banning in {30 - i} seconds...")

            ## ban loop
            for member in marked_for_death:
                
                try:
                    await member.send(f"You have been banned from Pig Game for the following reason:\n{ban_reason}\n\nNote: {ban_message}")
                
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

##-------------------start-of-sync-roles()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="sync-roles", description="Syncs the roles of all users in the server with the role persistence database. (ADMIN)")
        async def sync_roles(interaction:discord.Interaction) -> None:

            """
            
            Syncs the roles of all users in the server with the role persistence database.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """
            
            if(not await kanrisha_client.interaction_handler.admin_check(interaction)):
                return
            
            members = [member for member in interaction.guild.members] ## type: ignore (we know it's not None)

            await kanrisha_client.interaction_handler.sync_roles_logic(members, is_forced=True, forced_by=interaction.user.name)

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "Roles synced.", delete_after=3.0, is_ephemeral=True)

##-------------------start-of-get-running-config-directory()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="get-running-config-directory", description="Gets the running config directory. (ADMIN)")
        async def get_running_config_directory(interaction:discord.Interaction) -> None:

            """
            
            Gets the running config directory.\n

            Parameters:\n
            self (object - adminCommandHandler) : the adminCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(not await kanrisha_client.interaction_handler.admin_check(interaction)):
                return
            
            await kanrisha_client.interaction_handler.defer_interaction(interaction, is_ephemeral=True, is_thinking=True)
                    
            member_requesting = interaction.user
            
            src = kanrisha_client.file_ensurer.config_dir

            ## config dir name
            outer_dir_name = os.path.basename(src)

            ## destination
            if(os.name == 'nt'):  ## Windows
                dest = os.path.join(os.environ['USERPROFILE'],"KanrishaConfig-Copy")
            else:  ## Linux
                dest = os.path.join(os.path.expanduser("~"), "KanrishaConfig-Copy")

            excluded_files = [kanrisha_client.file_ensurer.credentials_path, kanrisha_client.file_ensurer.user_name_path, kanrisha_client.file_ensurer.token_path]

            with tempfile.TemporaryDirectory() as tmpdirname:
                ## Prepare the temp directory path with the outer directory name
                tmp_dest = os.path.join(tmpdirname, outer_dir_name)

                ## Copy the config to the temporary directory
                for dirpath, dirnames, filenames in os.walk(src):
                    for dirname in dirnames:
                        dest_dir_path = os.path.join(tmp_dest, os.path.relpath(dirpath, src), dirname)
                        if(not os.path.exists(dest_dir_path)):
                            os.makedirs(dest_dir_path)

                    for filename in filenames:
                        if(os.path.join(dirpath, filename) not in excluded_files):
                            shutil.copy2(os.path.join(dirpath, filename), os.path.join(tmp_dest, os.path.relpath(dirpath, src), filename))

                ## Create the ZIP from the temporary directory
                await asyncio.to_thread(shutil.make_archive, dest, 'zip', tmpdirname)

            ## send the zip file
            await member_requesting.send(file=discord.File(f"{dest}.zip"))

            await member_requesting.send("Please place this under your /user folder and rename it to KanrishaConfig.")

            ## delete the ZIP, temporary directory, and the copied config directory. Or at least try to.
            try:
                await asyncio.to_thread(os.remove, f"{dest}.zip")
            except:
                pass

            try:
                await asyncio.to_thread(shutil.rmtree, tmpdirname)
            except:
                pass

            try:
                await asyncio.to_thread(shutil.rmtree, dest)

            except:
                pass

            await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, "Config sent. Check your DMs.", is_ephemeral=True)

##-------------------start-of-load-members-from-local()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="load-local-storage", description="(DO NOT USE THIS WITH A LOADED INSTANCE) Loads from the local file. (ADMIN))")
        async def load_local_storage(interaction:discord.Interaction) -> None:

            """
            
            Loads members from the local file.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(not await kanrisha_client.interaction_handler.admin_check(interaction)):
                return
            
            await kanrisha_client.interaction_handler.defer_interaction(interaction, is_ephemeral=True, is_thinking=True)

            await kanrisha_client.remote_handler.load_local_storage()

            await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, "Loaded from local.", is_ephemeral=True)

##-------------------start-of-send-query()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="send-query", description="Sends an sql query to the local database. (ADMIN)")
        async def send_query(interaction:discord.Interaction, query:str) -> None:

            """
            
            Sends an sql query to the Nusevei database.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n
            query (str) : the query to send.\n

            Returns:\n
            None.\n

            """
            
            if(not await kanrisha_client.interaction_handler.admin_check(interaction)):
                return
            
            await kanrisha_client.interaction_handler.defer_interaction(interaction, is_ephemeral=True, is_thinking=True)
            
            if("drop" in query.lower()):
                await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, "You can't drop tables.", is_ephemeral=True)
                return
            
            ## get remote up to date
            await kanrisha_client.remote_handler.reset_remote_storage(is_forced=False)

            description = f"Query : {query}"

            try:

                ## if requesting data
                if(query.lower().startswith("select")):

                    result = await kanrisha_client.remote_handler.connection_handler.read_multi_column_query(query)
                
                    description += f"\n\nResult : \n{result}"

                else:
                
                    ## change remote via query
                    await kanrisha_client.remote_handler.connection_handler.execute_query(query)

            except Exception as e:
                await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, f"Error : {e}", is_ephemeral=True)
                return

            ## pull remote back into instance
            await kanrisha_client.remote_handler.load_remote_storage()

            embed = discord.Embed(title="Query Sent.", description=description, color=0xC0C0C0)

            await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, embed=embed, is_ephemeral=True)

        ##-------------------start-of-transfer()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="transfer", description="Transfers credits from one user to another.")
        async def transfer_credits(interaction: discord.Interaction, member:discord.Member, amount:int):

            """

            Transfers credits from one user to another.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n
            member (object - discord.Member) : the member object.\n
            amount (int) : the amount of credits to transfer.\n

            Returns:\n
            None.\n

            """

            is_admin = True

            ## Check if the user is registered
            if(not await kanrisha_client.check_if_registered(interaction)):
                return
            
            ## admin check
            if(not await kanrisha_client.interaction_handler.admin_check(interaction)):
                return 

            ## get the syndicateMember objects for the sender and the transfer target     
            sender_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_aibg_member_object(interaction, interaction.user)
            transfer_target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_aibg_member_object(interaction, member)

            if(transfer_target_member == None):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "That user is not registered.", delete_after=5.0, is_ephemeral=True)
                return
            
            ## Check if target and sender are the same
            if(sender_member.member_id == transfer_target_member.member_id and not is_admin): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You can't transfer credits to yourself.", delete_after=5.0, is_ephemeral=True)
                return

            ## Check if the amount is negative, allows admins to transfer negative credits
            if(amount < 0 and not is_admin):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You can't transfer negative credits.", delete_after=5.0, is_ephemeral=True)
                return

            ## Check if the sender has enough credits, allows admins to transfer more credits than they have
            if(amount > sender_member.credits and not is_admin): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You don't have enough credits.", delete_after=5.0, is_ephemeral=True)
                return
            
            ## deduct credits from sender and add to transfer target, admins are not deducted credits
            if(not is_admin):
                sender_member.credits -= amount ## type: ignore (we know it's not None)
                
            transfer_target_member.credits += amount

            embed = discord.Embed(title="Credit Transfer", description= f'{interaction.user.mention} successfully transferred {amount:,} credits to {member.mention}.', color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)

            await kanrisha_client.file_ensurer.logger.log_action("INFO", "Kanrisha", f"{interaction.user.name} transferred {amount} credits to {member.name}.") ## type: ignore (we know it's not None)
        
            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed)

##-------------------start-of-help_admin()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        @kanrisha_client.tree.command(name="help-admin", description="Lists admin commands. (ADMIN)")
        async def help_admin(interaction: discord.Interaction) -> None:

            """

            Sends the admin help message.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(not await kanrisha_client.interaction_handler.admin_check(interaction)):
                return

            help_message = (
                "**/trigger-early-shutdown** - Shuts down the bot. (ADMIN)\n\n"
                "**/force-log-push** - Forces a Kanrisha log push. (ADMIN)\n\n"
                "**/transfer** - Transfers credits from one user to another.\n\n"
                "**/force-remote-reset** - Overrides the local database with the current instance's data. (ADMIN)\n\n"
                "**/execute-order-66** - It is time. (ADMIN)\n\n"
                "**/sync-roles** - Syncs the roles of all users in the server with the role persistence database. (ADMIN)\n\n"
                "**/get-running-config-directory** - Gets the running config directory. (ADMIN)\n\n"
                "**/load-local-storage** - (DO NOT USE THIS WITH A LOADED INSTANCE) Loads from the local file. (ADMIN))\n\n"
                "**/send-query** - Sends an sql query to the local database. (ADMIN)\n\n"
                "**/help-admin** - Sends this message (ADMIN).\n\n"
            )

            embed = discord.Embed(title="Help", description=help_message, color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed)

        ##-------------------start-of-banners--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        ## banners for logic functions, so that they can be accessed internally
        ## cause functions with decorations cannot be accessed internally

        trigger_early_shutdown = kanrisha_client.tree.command(name="trigger-early-shutdown", description="Shuts down the bot. (ADMIN)")(trigger_early_shutdown_logic)
        force_log_push = kanrisha_client.tree.command(name="force-log-push", description="Forces a Kanrisha log push. (ADMIN)")(force_log_push_logic)
        force_remote_reset = kanrisha_client.tree.command(name="force-remote-reset", description="Overrides the local database with the current instance's data. (ADMIN)")(force_remote_reset_logic)