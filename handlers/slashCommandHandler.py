## built-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing

## third-party libraries
import discord

## custom libraries
from handlers.eventHandler import eventHandler
from handlers.adminCommandHandler import adminCommandHandler

from entities.syndicateMember import syndicateMember

from exam.gooseExam import gooseExam

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

        kanrisha_client = inc_kanrisha_client

        archive_channel_id = 1146979933416067163

        self.event_handler = eventHandler(kanrisha_client)

        self.goose_exam = gooseExam(kanrisha_client)

        self.admin_command_handler = adminCommandHandler(kanrisha_client)
    
        ##-------------------start-of-check_if_registered()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def check_if_registered(self, interaction:discord.Interaction, register_check:bool = False):

            registered_member_ids = [member.member_id for member in kanrisha_client.remote_handler.member_handler.members]

            if(interaction.user.id not in registered_member_ids):

                if(register_check == False):
                    error_message = "You are not registered. Please use the /register command to register."

                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, response=error_message, delete_after=5.0, is_ephemeral=True)

                return False
            
            else:
                return True
            
        ##-------------------start-of-get_member_id()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def get_member_id(interaction:discord.Interaction, member:discord.Member | discord.User | None = None) -> typing.Tuple[syndicateMember | None, int, str, bool]:

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

            for syndicate_member in kanrisha_client.remote_handler.member_handler.members:
                    
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

            spin_result, spin_index = await kanrisha_client.gacha_handler.spin_wheel(interaction.user.id)

            target_member, _, _, _ = await get_member_id(interaction) 

            await kanrisha_client.remote_handler.member_handler.update_spin_value(target_member.member_id, 1, spin_index) ## type: ignore (we know it's not None)

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
                spin_result, spin_index = await kanrisha_client.gacha_handler.spin_wheel(interaction.user.id)

                multi_spin += f"{spin_result}"

                await kanrisha_client.remote_handler.member_handler.update_spin_value(target_member.member_id, 1, spin_index) ## type: ignore (we know it's not None)

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

         ##-------------------start-of-snipe()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="snipe", description="Nobody's safe.")
        async def snipe(interaction: discord.Interaction):

            """

            Snipes the last deleted message in the channel.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n

            Returns:\n
            None.\n

            """

            try:

                store_channel = kanrisha_client.get_channel(archive_channel_id)

                deleted_message = None

                messages = [message async for message in store_channel.history(limit=25)]  ## type: ignore

                for message in messages:

                    if(message.embeds and message.embeds[0].fields[0].value == str(interaction.channel_id)):
                        deleted_message = message
                        break

                if(not deleted_message):
                    error_message = "No recent deleted messages in this channel."
                    raise Exception(error_message)
                
                embed = discord.Embed(title=deleted_message.embeds[0].title, description=deleted_message.embeds[0].description, color=0xC0C0C0)
                embed.set_thumbnail(url=deleted_message.embeds[0].thumbnail.url)
                embed.set_footer(text=deleted_message.embeds[0].footer.text)

                await kanrisha_client.file_ensurer.logger.log_action("INFO", "Kanrisha", f"{interaction.user.name} sniped a message in {interaction.channel.name}. The message was: {deleted_message.embeds[0].description}") ## type: ignore

                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed)
                
            except:

                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, error_message, delete_after=3.0, is_ephemeral=True) ## type: ignore (we know it's not unbound)

        ##-------------------start-of-profile()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="profile", description="Sends the user's profile.")
        async def profile(interaction: discord.Interaction, member:typing.Union[discord.Member , None]):

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
                profile_message = (
                    f"**Name:** {target_member.member_name}\n"
                    f"**Credits:** {target_member.credits}\n"
                    f"**Shining Rolls:** {target_member.spin_scores[0]}\n"
                    f"**Glowing Rolls:** {target_member.spin_scores[1]}\n"
                    f"**Common Rolls:** {target_member.spin_scores[2]}"
                )
            else:
                is_ephemeral = False
                profile_message = (
                    f"**Name:** {target_member.member_name}\n"
                    f"**Shining Rolls:** {target_member.spin_scores[0]}\n"
                    f"**Glowing Rolls:** {target_member.spin_scores[1]}\n"
                    f"**Common Rolls:** {target_member.spin_scores[2]}"
                )

            embed = discord.Embed(title="Profile", description=profile_message, color=0xC0C0C0)
            embed.set_thumbnail(url=image_url)

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, profile_message, embed=embed, is_ephemeral=is_ephemeral)

        ##-------------------start-of-transfer()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

       #@kanrisha_client.tree.command(name="transfer", description="Transfers credits from one user to another.")
        async def transfer_credits(self, interaction: discord.Interaction, member:discord.Member, amount:int):

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

            is_admin = False

            ## Check if the user is registered
            if(await check_if_registered(self, interaction) == False):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not registered.", delete_after=5.0, is_ephemeral=True)
                return
            
            ## Check if the user is an admin
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
                is_admin = True

            ## get the syndicateMember objects for the sender and the transfer target     
            sender_member, _, _, _ = await get_member_id(interaction, interaction.user)
            transfer_target_member, _, _, _ = await get_member_id(interaction, member)

            if(transfer_target_member == None):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "That user is not registered.", delete_after=5.0, is_ephemeral=True)
                return
            
            ## Check if target and sender are the same
            if(sender_member.member_id == transfer_target_member.member_id): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You can't transfer credits to yourself.", delete_after=5.0, is_ephemeral=True)
                return

            if(amount < 0 and not is_admin):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You can't transfer negative credits.", delete_after=5.0, is_ephemeral=True)
                return

            if(amount > sender_member.credits and not is_admin): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You don't have enough credits.", delete_after=5.0, is_ephemeral=True)
                return
            
            sender_member.credits -= amount ## type: ignore (we know it's not None)
            transfer_target_member.credits += amount

            embed = discord.Embed(title="Credit Transfer", description= f"{interaction.user.mention} successfully transferred {amount} credits to {member.mention}.", color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)
        
            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed)

        ##-------------------start-of-leaderboard()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="leaderboard", description="Sends the leaderboard.")
        async def leaderboard(interaction: discord.Interaction):

            """

            Sends the leaderboard.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            ## Check if the user is registered
            if(not await check_if_registered(self, interaction)):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not registered.", delete_after=5.0, is_ephemeral=True)
                return

            ## Calculate scores for each member who has spun at least once and store them in a list with the member's name
            scores_with_members = []
            for member in kanrisha_client.remote_handler.member_handler.members:
                total_spins = sum(member.spin_scores)
                if(total_spins > 0):
                    score = round((member.spin_scores[0] * 20 + member.spin_scores[1] * 8.33 + member.spin_scores[2] * 1.20) / total_spins, 3)
                    scores_with_members.append((score, member.member_name))

            ## Sort the list based on the scores in descending order and then take only the top 10
            scores_with_members.sort(key=lambda x: x[0], reverse=True)
            top_10_scores_with_members = scores_with_members[:10]

            ## Find the rank of the user calling the command
            user_rank = None
            for rank, (score, member_name) in enumerate(scores_with_members, 1):
                if(member_name == interaction.user.name):
                    user_rank = rank
                    break

            ## Calculate rank for users who haven't spun yet
            no_spin_rank = len(scores_with_members) + 1

            ## Construct the leaderboard message
            leaderboard_message = ""
            for score, member_name in top_10_scores_with_members:
                leaderboard_message += f"**{member_name}** - {score}\n"

            embed = discord.Embed(title="Luck Leaderboard", description=leaderboard_message, color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)
            
            if(user_rank is not None):
                embed.set_footer(text=f"Your rank is #{user_rank}.")
            else:
                embed.set_footer(text=f"Your rank is #{no_spin_rank} (haven't spun yet).")

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "", embed=embed)

##-------------------start-of-help_commands()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        @kanrisha_client.tree.command(name="help-commands", description="Sends the help message.")
        async def help_commands(interaction: discord.Interaction):

            """

            Sends the help message.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            help_message = (
                "**/spin** - Spins a wheel.\n"
                "**/multispin** - Spins a wheel 10 times.\n"
                "**/register** - Registers a user to the bot.\n"
                "**/snipe** - Snipes the last deleted message in a channel.\n"
                "**/profile** - Sends the user's profile.\n"
                "**/leaderboard** - Sends the luck leaderboard\n"
                "**/transfer** - Transfers credits from one user to another.\n"
                "**/help-commands** - Sends this message.\n"
            )

            embed = discord.Embed(title="Help", description=help_message, color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed)
