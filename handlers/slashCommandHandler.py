## built-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing
import asyncio

## third-party libraries
import discord

## custom libraries
if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from bot.Kanrisha import Kanrisha

class slashCommandHandler:

    """
    
    Handles slash commands.\n

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

        self.pg_guild_id = 1143635379262607441

        self.syndicate_role = 1146901009248026734

        kanrisha_client = inc_kanrisha_client

        ##-------------------start-of-check_if_registered()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def check_if_registered(self, interaction:discord.Interaction):

            registered_member_ids = [member.member_id for member in kanrisha_client.member_handler.members]

            if(interaction.user.id not in registered_member_ids):
                error_message = "You are not registered. Please use the /register command to register."

                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, response=error_message, delete_after=5.0, is_ephemeral=True)

                return False
            
            else:
                return True

        ##-------------------start-of-spin()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="spin", description="Spins a wheel")
        async def spin(interaction: discord.Interaction):

            """
            
            Spins a wheel.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(await check_if_registered(self, interaction) == False):
                return

            spin_result = kanrisha_client.gacha_handler.spin_wheel()

            await kanrisha_client.interaction_handler.send_response_filter_channel(interaction, spin_result, embed=None, view=None)

        ##-------------------start-of-multispin()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="multispin", description="Spins a wheel 10 times")
        async def multi_spin(interaction: discord.Interaction):

            """

            Spins a wheel 10 times.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(await check_if_registered(self, interaction) == False):
                return

            multi_spin = ""
            
            for i in range(0, 10):
                multi_spin += kanrisha_client.gacha_handler.spin_wheel()

            await kanrisha_client.interaction_handler.send_response_filter_channel(interaction, multi_spin)

        ##-------------------start-of-register()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="register", description="Registers a user to the bot.")
        async def register(interaction: discord.Interaction):

            """

            Registers a user to the bot, currently only admits the user to the bot's testing phase.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            register_message = """
            By clicking this button you acknowledge and agree to the following:\n
            - You will be using the bot during its testing phase, and any and all data may be wiped/lost at any time.\n
            - You will not hold the bot owner responsible for any data loss.\n
            - You may have to register multiple times during the testing phase.\n
            """

            if(await check_if_registered(self, interaction) == True):
                error_message = "You are already registered."

                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, response=error_message, delete_after=5.0, is_ephemeral=True)

                return

            embed = discord.Embed(title="Register", description=register_message, color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)
            embed.set_footer(text="This message will be deleted in 60 seconds.")

            # Store the user's ID as a custom attribute of the button
            view = discord.ui.View().add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id=f"register_{interaction.user.id}", label="Register"))

            await kanrisha_client.interaction_handler.send_response_filter_channel(interaction, embed=embed, view=view, delete_after=60.0)

        ##-------------------start-of-execute_order_66()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="execute-order-66", description="It is time.")
        async def execute_order_66(interaction:discord.Interaction, ban_reason:str, ban_message:str):

            """
            
            Executes order 66.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n
            ban_reason (str) : the reason for the ban.\n

            Returns:\n
            None.\n

            """

            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
                await interaction.response.send_message("You do not have permission to use this command.", delete_after=3.0, ephemeral=True)
                return

            marked_for_death_role_id = 1146651136363855982

            ## server announcements role
            role_to_ping = kanrisha_client.get_guild(self.pg_guild_id).get_role(1144052522819010601) ## type: ignore (we know it's not None)

            role_ping = role_to_ping.mention ## type: ignore (we know it's not None)

            marked_for_death: typing.List[discord.Member] = []

            execution_message = "The following users have been marked for death and will be banned:\n"

            for guild in kanrisha_client.guilds:
                
                for member in guild.members:

                    member_role_ids = [role.id for role in member.roles]

                    if(marked_for_death_role_id in member_role_ids):
                        marked_for_death.append(member)
                        execution_message += f"{member.mention}\n"

            execution_message += f"\n\nPinging : {role_ping}"

            if(len(marked_for_death) == 0):
                execution_message = "No users have been marked for death."
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, execution_message, delete_after=5.0, is_ephemeral=True)
                return
            
            embed = discord.Embed(title="Order 66.", description=execution_message, color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)
            embed.set_footer(text=f"Ban Reason : {ban_reason}\n\nBanning in 30 seconds, please standby...") 

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed)

            await asyncio.sleep(20)

            for i in range(10):
                await asyncio.sleep(1)
                await interaction.followup.send(f"Banning in {10 - i} seconds...")

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

                    syndicate_role = kanrisha_client.get_guild(self.pg_guild_id).get_role(self.syndicate_role) ## type: ignore (we know it's not None)

                    ## acknowledge the interaction immediately
                    await interaction.response.defer()

                    await kanrisha_client.member_handler.add_new_member(interaction.user.id, interaction.user.name, tuple([0,0,0]),0)

                    await interaction.delete_original_response()

                    await interaction.followup.send("You have been registered.", ephemeral=True)

                    await interaction.user.add_roles(syndicate_role) ## type: ignore (we know it's not None)

                ## if register button was pressed by the wrong user
                elif custom_id and custom_id.startswith("register_"):

                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not authorized to use this button.", delete_after=5.0, is_ephemeral=True)


        ##-------------------start-of-profile()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="profile", description="Sends the user's profile.")
        async def profile(interaction: discord.Interaction, member:discord.Member | None):

            """
            
            Sends the user's profile.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(await check_if_registered(self, interaction) == False):
                return

            target_member = None
            target_member_id = None
            image_url = None

            self_request = False
            is_ephemeral = True

            if(member):

                target_member_id = member.id
                image_url = member.display_avatar.url
                
    
            else:
                self_request = True
                target_member_id = interaction.user.id
                image_url = interaction.user.display_avatar.url

            for syndicate_member in kanrisha_client.member_handler.members:
                    
                    if(target_member_id == syndicate_member.member_id):
                        target_member = syndicate_member

            if(target_member == None):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "That user is not registered.", delete_after=5.0, is_ephemeral=True)
                return
            
            ## if user is admin or if user is requesting their own profile
            if(self_request or interaction.user.id in kanrisha_client.interaction_handler.admin_user_ids):

                profile_message = f"""
                **Name:** {target_member.member_name}
                \n**Credits:** {target_member.credits}
                """
            
            else:

                is_ephemeral = False

                profile_message = f"""
                **Name:** {target_member.member_name}\n
                """

            embed = discord.Embed(title="Profile", description=profile_message, color=0xC0C0C0)
            embed.set_thumbnail(url=image_url)

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, profile_message, embed=embed, is_admin_only=True, is_ephemeral=is_ephemeral)