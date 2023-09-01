## built-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing
import asyncio

## third-party libraries
import discord

## custom libraries
from handlers.eventHandler import eventHandler
if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from bot.Kanrisha import Kanrisha

from handlers.adminCommandHandler import adminCommandHandler

from entities.syndicateMember import syndicateMember

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


        ##-------------------event-handler--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        kanrisha_client.event_handler = eventHandler(kanrisha_client)

        self.admin_command_handler = adminCommandHandler(kanrisha_client)
    
        ##-------------------start-of-check_if_registered()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def check_if_registered(self, interaction:discord.Interaction, register_check:bool = False):

            registered_member_ids = [member.member_id for member in kanrisha_client.member_handler.members]

            if(interaction.user.id not in registered_member_ids):

                if(register_check == False):
                    error_message = "You are not registered. Please use the /register command to register."

                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, response=error_message, delete_after=5.0, is_ephemeral=True)

                return False
            
            else:
                return True
            
        ##-------------------start-of-get_member_id()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def get_member_id(interaction:discord.Interaction, member:discord.Member | None = None) -> typing.Tuple[syndicateMember | None, int, str, bool]:

            """
            
            Gets the member id of the member.\n
            
            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n
            member (object - discord.Member) : the member object.\n

            Returns:\n
            target_member_id (int) : the member id of the member.\n
            target_member_id (int) : the member id of the member.\n
            image_url (str) : the url of the member's avatar.\n
            is_self_request (bool) : whether or not the request is for the user's own profile.\n

            """

            target_member = None

            is_self_request = False

            if(member):

                target_member_id = member.id
                image_url = member.display_avatar.url
                
            else:
                is_self_request = True
                target_member_id = interaction.user.id
                image_url = interaction.user.display_avatar.url

            for syndicate_member in kanrisha_client.member_handler.members:
                    
                    if(target_member_id == syndicate_member.member_id):
                        target_member = syndicate_member

            return target_member, target_member_id, image_url, is_self_request

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

            spin_result, spin_index = kanrisha_client.gacha_handler.spin_wheel()

            target_member, _, _, _ = await get_member_id(interaction) 

            await kanrisha_client.member_handler.update_spin_value(target_member.member_id, 1, spin_index) ## type: ignore (we know it's not None)

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

            target_member, _, _, _ = await get_member_id(interaction) 

            multi_spin = ""
            
            for i in range(0, 10):
                spin_result, spin_index = kanrisha_client.gacha_handler.spin_wheel()

                multi_spin += f"{spin_result}"

                await kanrisha_client.member_handler.update_spin_value(target_member.member_id, 1, spin_index) ## type: ignore (we know it's not None)

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

            if(await check_if_registered(self, interaction, register_check=True) == True):
                error_message = "You are already registered."

                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, response=error_message, delete_after=5.0, is_ephemeral=True)

                return

            embed = discord.Embed(title="Register", description=register_message, color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)
            embed.set_footer(text="This message will be deleted in 60 seconds.")

            # Store the user's ID as a custom attribute of the button
            view = discord.ui.View().add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id=f"register_{interaction.user.id}", label="Register"))

            await kanrisha_client.interaction_handler.send_response_filter_channel(interaction, embed=embed, view=view, delete_after=60.0)

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



         ##-------------------start-of-execute_order_66()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="snipe", description="Nobody's safe.")
        async def snipe(interaction: discord.Interaction):
            store_channel = kanrisha_client.get_channel(1146979933416067163)
            messages = [message async for message in store_channel.history(limit=25)]
            deleted_message = None
            for message in messages:
                if int(message.content) == interaction.channel.id:
                    deleted_message = message
                    break
            if not deleted_message:
                await interaction.response.send_message("Message unavailable.", delete_after=3.0, ephemeral=True)
                return
            deleted_message_embed = deleted_message.embeds[0]
            await interaction.response.send_message("", embed=deleted_message_embed)

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
            
            is_ephemeral = True

            target_member, _, image_url, self_request = await get_member_id(interaction, member)

            if(target_member == None):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "That user is not registered.", delete_after=5.0, is_ephemeral=True)
                return
            
            ## if user is admin or if user is requesting their own profile
            if(self_request or interaction.user.id in kanrisha_client.interaction_handler.admin_user_ids):

                profile_message = f"""
                **Name:** {target_member.member_name}
                **Credits:** {target_member.credits}
                \n**Shining Rolls:** {target_member.spin_scores[0]}
                **Glowing Rolls:** {target_member.spin_scores[1]}
                **Common Rolls:** {target_member.spin_scores[2]}
                """
            
            else:

                is_ephemeral = False

                profile_message = f"""
                **Name:** {target_member.member_name}\n
                \n**Shining Rolls:** {target_member.spin_scores[0]}
                **Glowing Rolls:** {target_member.spin_scores[1]}
                **Common Rolls:** {target_member.spin_scores[2]}
                """

            embed = discord.Embed(title="Profile", description=profile_message, color=0xC0C0C0)
            embed.set_thumbnail(url=image_url)

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, profile_message, embed=embed, is_ephemeral=is_ephemeral)
