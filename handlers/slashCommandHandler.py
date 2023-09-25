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

        ##self.goose_exam = gooseExam(kanrisha_client)

        self.admin_command_handler = adminCommandHandler(kanrisha_client)
    
        ##-------------------start-of-check_if_registered()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def check_if_registered(interaction:discord.Interaction, register_check:bool = False):

            """

            Checks if the user is registered.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n
            register_check (bool) : whether or not the check is for the register command.\n

            Returns:\n
            None.\n

            """

            registered_member_ids = [member.member_id for member in kanrisha_client.remote_handler.member_handler.members]

            if(interaction.user.id not in registered_member_ids):

                if(register_check == False):
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

            if(await check_if_registered(interaction) == False):
                return

            spin_result, spin_index = await kanrisha_client.remote_handler.gacha_handler.spin_wheel(interaction.user.id)

            target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_syndicate_member(interaction)

            await kanrisha_client.remote_handler.member_handler.update_spin_value(target_member.member_id, 1, spin_index) ## type: ignore (we know it's not None)

            await kanrisha_client.interaction_handler.send_response_filter_channel(interaction, spin_result, embed=None, view=None)

        ##-------------------start-of-multispin()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="multispin", description="Spins a wheel 10 times")
        async def multi_spin(interaction: discord.Interaction):

            """

            Spins a wheel 10 times.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(await check_if_registered(interaction) == False):
                return

            target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_syndicate_member(interaction)

            multi_spin = ""
            
            for i in range(0, 10):
                spin_result, spin_index = await kanrisha_client.remote_handler.gacha_handler.spin_wheel(interaction.user.id)

                multi_spin += f"{spin_result}"

                await kanrisha_client.remote_handler.member_handler.update_spin_value(target_member.member_id, 1, spin_index) ## type: ignore (we know it's not None)

            await kanrisha_client.interaction_handler.send_response_filter_channel(interaction, multi_spin)

        ##-------------------start-of-gacha_spin()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="gacha-spin", description="Spins the wheel to obtain a card.")
        async def gacha_spin(interaction: discord.Interaction):

            """

            Spins the gacha wheel.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(await check_if_registered(interaction) == False):
                return

            ## admin check
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You do not have permission to use this command.", delete_after=3.0, is_ephemeral=True)
                return

            card = await kanrisha_client.remote_handler.gacha_handler.spin_gacha(interaction.user.id)

            embed = card.get_display_embed()

            ## get the syndicateMember object for the target member, and add the card id to the member's owned_card_ids list if not already owned
            target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_syndicate_member(interaction)

            if(card.id not in target_member.owned_card_ids): ## type: ignore (we know it's not None)
                target_member.owned_card_ids.append(card.id) ## type: ignore (we know it's not None)

            ## add credits to the member's balance based on the card's rarity if the card is already owned
            else:
                credits_to_add = kanrisha_client.remote_handler.gacha_handler.rarity_to_credits.get(card.rarity.name, 0) 
                target_member.credits += credits_to_add ## type: ignore (we know it's not None)
                embed.set_footer(text=f"You already own this card. You have been awarded {credits_to_add} credits.")
    
            await kanrisha_client.interaction_handler.send_response_filter_channel(interaction, embed=embed)

        ##-------------------start-of-register()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="register", description="Signs you up for the Syndicates System.")
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

            if(await check_if_registered(interaction, register_check=True) == True):
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

        @kanrisha_client.tree.command(name="snipe", description="Fetches the last deleted message in a channel.")
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

                    if(message.embeds and message.embeds[0].fields[1].value == str(interaction.channel_id)):
                        deleted_message = message
                        break

                if(not deleted_message):
                    error_message = "No recent deleted messages in this channel."
                    raise Exception(error_message)
                
                embed = discord.Embed(title=deleted_message.embeds[0].title, description=f"Deleted Message : {deleted_message.embeds[0].description}\nDeleted At : {deleted_message.embeds[0].fields[0].value}.", color=0xC0C0C0)
                embed.set_thumbnail(url=deleted_message.embeds[0].thumbnail.url)
                embed.set_footer(text=deleted_message.embeds[0].footer.text)

                await kanrisha_client.file_ensurer.logger.log_action("INFO", "Kanrisha", f"{interaction.user.name} sniped a message in {interaction.channel.name}. The message was: {deleted_message.embeds[0].description}") ## type: ignore (we know it's not None)

                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed)
                
            except:

                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, error_message, delete_after=3.0, is_ephemeral=True) ## type: ignore (we know it's not unbound)

        ##-------------------start-of-profile()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="profile", description="Sends a members Syndicate profile.")
        async def profile(interaction: discord.Interaction, member:typing.Union[discord.Member , None]):

            """
            
            Sends the user's profile.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(await check_if_registered(interaction) == False):
                return
            
            is_ephemeral = True

            target_member, _, image_url, self_request = await kanrisha_client.remote_handler.member_handler.get_syndicate_member(interaction, member)

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

            is_admin = False

            ## Check if the user is registered
            if(await check_if_registered(interaction) == False):
                return
            
            ## Check if the user is an admin
            if(interaction.user.id in kanrisha_client.interaction_handler.admin_user_ids):
                is_admin = True

            ## get the syndicateMember objects for the sender and the transfer target     
            sender_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_syndicate_member(interaction, interaction.user)
            transfer_target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_syndicate_member(interaction, member)

            if(transfer_target_member == None):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "That user is not registered.", delete_after=5.0, is_ephemeral=True)
                return
            
            ## Check if target and sender are the same
            if(sender_member.member_id == transfer_target_member.member_id and not is_admin): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You can't transfer credits to yourself.", delete_after=5.0, is_ephemeral=True)
                return

            if(amount < 0 and not is_admin):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You can't transfer negative credits.", delete_after=5.0, is_ephemeral=True)
                return

            if(amount > sender_member.credits and not is_admin): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You don't have enough credits.", delete_after=5.0, is_ephemeral=True)
                return
            
            if(not is_admin):
                sender_member.credits -= amount ## type: ignore (we know it's not None)
                
            transfer_target_member.credits += amount

            embed = discord.Embed(title="Credit Transfer", description= f"{interaction.user.mention} successfully transferred {amount} credits to {member.mention}.", color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)

            await kanrisha_client.file_ensurer.logger.log_action("INFO", "Kanrisha", f"{interaction.user.name} transferred {amount} credits to {member.name}.") ## type: ignore (we know it's not None)
        
            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed)

##-------------------start-of-get_card()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="card", description="Displays a card.")
        async def get_card(interaction:discord.Interaction, member:discord.Member | None, card_name:str) -> None:

            """
            
            Gets a card.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n
            member (object - discord.Member | None) : the member object.\n

            Returns:\n
            None.\n

            """

            ## Check if the user is registered
            if(await check_if_registered(interaction) == False):
                return
            
            ## get the syndicateMember object for the target member
            target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_syndicate_member(interaction, member)

            ## make sure the target member is registered
            if(target_member == None):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "That user is not registered.", delete_after=5.0, is_ephemeral=True)
                return

            owned_card_names = [card.name.lower() for card in kanrisha_client.remote_handler.gacha_handler.cards if card.id in target_member.owned_card_ids] ## type: ignore (we know it's not None)
            all_card_names = [card.name.lower() for card in kanrisha_client.remote_handler.gacha_handler.cards]

            ## if member has the card, get the card object
            if(card_name.lower() in owned_card_names): ## type: ignore (we know it's not None)
                card = [card for card in kanrisha_client.remote_handler.gacha_handler.cards if card.name.lower() == card_name.lower()][0] ## type: ignore (we know it's not None)

            elif(card_name.lower() in all_card_names):
                card = [card for card in kanrisha_client.remote_handler.gacha_handler.cards if card.name.lower() == card_name.lower()][0]
            
            else:

                card_name = await kanrisha_client.toolkit.get_intended_card(card_name, all_card_names)

                card = [card for card in kanrisha_client.remote_handler.gacha_handler.cards if card.name.lower() == card_name.lower()][0]

            embed = card.get_display_embed()

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed)

##-------------------start-of-get_deck()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="deck", description="Displays the user's deck.")
        async def get_deck(interaction:discord.Interaction, member:discord.Member | None) -> None:

            """

            Displays the user's deck.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n
            member (object - discord.Member | None) : the member object.\n
            
            Returns:\n
            None.\n

            """

            ## Check if the user is registered
            if(not await check_if_registered(interaction)):
                return
            
            ## get the syndicateMember object for the target member
            target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_syndicate_member(interaction, member)

            if(target_member.owned_card_ids == []): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "That deck doesn't have any cards.", delete_after=5.0, is_ephemeral=True)
                return
            
            ## get the card objects for the target member's owned cards
            owned_cards = [card for card in kanrisha_client.remote_handler.gacha_handler.cards if card.id in target_member.owned_card_ids] ## type: ignore (we know it's not None)

            ## sort the cards by rarity
            owned_cards.sort(key=lambda x: x.rarity.identifier, reverse=True)

            embed = discord.Embed(title="Deck", description=f"{owned_cards[0].rarity.name} {owned_cards[0].name}", color=0xC0C0C0)
            embed.set_image(url=owned_cards[0].picture_url)
            embed.set_footer(text=f"1/{len(owned_cards)}")

            ## custom id structure
            ##  id of command caller | id of member whose deck is being viewed
            ## _{interaction.user.id}.{member.id}
            custom_id = f"_{interaction.user.id}.{target_member.member_id}" ## type: ignore (we know it's not None)

            left_button = discord.ui.Button(style=discord.ButtonStyle.gray, custom_id=f"deck_left{custom_id}", emoji="◀️")
            right_button = discord.ui.Button(style=discord.ButtonStyle.gray, custom_id=f"deck_right{custom_id}", emoji="▶️")

            view = discord.ui.View(timeout=300)

            view.add_item(left_button)
            view.add_item(right_button)

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed, view=view)

##-------------------start-of-catalog()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="catalog", description="Shows all cards.")
        async def catalog(interaction:discord.Interaction) -> None:

            """

            Shows all cards.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            ## Check if the user is registered
            if(not await check_if_registered(interaction)):
                return

            kanrisha_member = await kanrisha_client.fetch_user(kanrisha_client.interaction_handler.admin_user_ids[-1])

            kanrisha_syndicate_object, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_syndicate_member(interaction, kanrisha_member) ## type: ignore (we know it's not None)

            ## get the card objects for the target member's owned cards
            owned_cards = [card for card in kanrisha_client.remote_handler.gacha_handler.cards if card.id in kanrisha_syndicate_object.owned_card_ids] ## type: ignore (we know it's not None)

            ## sort the cards by rarity
            owned_cards.sort(key=lambda x: x.rarity.identifier, reverse=True)

            embed = discord.Embed(title="Catalog", description=f"{owned_cards[0].rarity.name} {owned_cards[0].name}", color=0xC0C0C0)
            embed.set_image(url=owned_cards[0].picture_url)
            embed.set_footer(text=f"1/{len(owned_cards)}")

            ## custom id structure
            ##  id of command caller | id of member whose deck is being viewed
            ## _{interaction.user.id}.{member.id}
            custom_id = f"_{interaction.user.id}.{kanrisha_syndicate_object.member_id}" ## type: ignore (we know it's not None)

            left_button = discord.ui.Button(style=discord.ButtonStyle.gray, custom_id=f"deck_left{custom_id}", emoji="◀️")
            right_button = discord.ui.Button(style=discord.ButtonStyle.gray, custom_id=f"deck_right{custom_id}", emoji="▶️")

            view = discord.ui.View(timeout=300)

            view.add_item(left_button)
            view.add_item(right_button)

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed, view=view)
            
##-------------------start-of-leaderboard()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="leaderboard", description="Sends the leaderboards.")
        async def leaderboard(interaction: discord.Interaction):

            """
            
            Sends the leaderboards.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            ## Check if the user is registered
            if(not await check_if_registered(interaction)):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not registered.", delete_after=5.0, is_ephemeral=True)
                return

            luck_leaderboard = await get_luck_leaderboard(interaction)

            balance_leaderboard = await get_balance_leaderboard(interaction)

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=luck_leaderboard)

            await interaction.followup.send(embed=balance_leaderboard)

##-------------------start-of-get_luck_leaderboard()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def get_luck_leaderboard(interaction: discord.Interaction) -> discord.Embed:

            """

            Gets the luck leaderboard.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            luck_leaderboard (object - discord.Embed) : the embed object.\n

            """

            ## Calculate scores for each member who has spun at least once and store them in a list with the member's name
            scores_with_members = []
            for member in kanrisha_client.remote_handler.member_handler.members:
                ## Skip admins
                if(member.member_id in kanrisha_client.interaction_handler.admin_user_ids):
                    continue

                total_spins = sum(member.spin_scores)
                if(total_spins > 0):
                    score = round((member.spin_scores[0] * 20 + member.spin_scores[1] * 8.33 + member.spin_scores[2] * 1.20) / total_spins, 3)
                    scores_with_members.append((score, member.member_name))

            ## Sort the list based on the scores in descending order and then take only the top 10
            scores_with_members.sort(key=lambda x: x[0], reverse=True)
            top_10_scores_with_members = scores_with_members[:10]

            ## Find the rank of the user calling the command if the user is not an admin
            user_rank = None
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
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

            luck_leaderboard = discord.Embed(title="Luck Leaderboard", description=leaderboard_message, color=0xC0C0C0)
            luck_leaderboard.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)

            annotation = "At the end of each month, top 5 users will receive a credit bonus based on their rank.\n"
            
            if(user_rank is not None):
                luck_leaderboard.set_footer(text=f"Your rank is #{user_rank}. {annotation}")
            elif(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):  # Check if the user is not an admin
                luck_leaderboard.set_footer(text=f"Your rank is #{no_spin_rank} (haven't spun yet). {annotation}")

            return luck_leaderboard
        
##-------------------start-of-get_balance_leaderboard()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def get_balance_leaderboard(interaction: discord.Interaction) -> discord.Embed:

            """
            
            Gets the balance leaderboard.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            balance_leaderboard (object - discord.Embed) : the embed object.\n

            """

            ## Sort the list based on the scores in descending order and then take only the non-admin members
            non_admin_members = [
                member for member in kanrisha_client.remote_handler.member_handler.members 
                if member.member_id not in kanrisha_client.interaction_handler.admin_user_ids
            ]
            
            ## Sort the non-admin members based on credits in descending order
            sorted_non_admin_members = sorted(non_admin_members, key=lambda x: x.credits, reverse=True)
            
            ## Take the top 10 members for the leaderboard
            top_10_members = sorted_non_admin_members[:10]
            
            ## Find the rank of the user calling the command if they are not an admin
            user_rank = None
            if interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids:
                for rank, member in enumerate(sorted_non_admin_members, 1):
                    if member.member_id == interaction.user.id:
                        user_rank = rank
                        break
            
            ## Construct the leaderboard message
            leaderboard_message = ""
            for member in top_10_members:
                leaderboard_message += f"**{member.member_name}** - {member.credits}\n"
            
            balance_leaderboard = discord.Embed(
                title="Balance Leaderboard",
                description=leaderboard_message,
                color=0xC0C0C0
            )
            balance_leaderboard.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)
            
            ## Only set the footer with rank if the user is not an admin
            if user_rank is not None:
                balance_leaderboard.set_footer(text=f"Your rank is #{user_rank}.")
            
            return balance_leaderboard
        
##-------------------start-of-help_commands()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        @kanrisha_client.tree.command(name="help-commands", description="Shows all commands.")
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
                "**/spin** - Spins a wheel.\n\n"
                "**/multispin** - Spins a wheel 10 times.\n\n"
                "**/gacha-spin** - Spins the gacha wheel.\n\n"
                "**/register** - Signs you up for the Syndicates System.\n\n"
                "**/snipe** - Fetches the last deleted message in a channel.\n\n"
                "**/profile** - Sends a members Syndicate profile.\n\n"
                "**/transfer** - Transfers credits from one user to another.\n\n"
                "**/card** - Displays a card.\n\n"
                "**/deck** - Displays the user's deck.\n\n"
                "**/catalog** - Shows all cards.\n\n"
                "**/leaderboard** - Sends the leaderboards.\n\n"
                "**/help-commands** - Sends this message.\n\n"
            )

            embed = discord.Embed(title="Help", description=help_message, color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed)
