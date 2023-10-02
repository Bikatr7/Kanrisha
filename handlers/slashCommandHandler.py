## built-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing
import copy

## third-party libraries
import discord

## custom libraries
from handlers.eventHandler import eventHandler
from handlers.adminCommandHandler import adminCommandHandler
from handlers.pilHandler import pilHandler
from handlers.leaderboardHandler import leaderboardHandler
from handlers.gachaCommandHandler import gachaCommandHandler

from entities.card import card

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
        inc_kanrisha_client (object - Kanrisha) : the Kanrisha client object.\n

        Returns:\n
        None.\n

        """

        kanrisha_client = inc_kanrisha_client

        archive_channel_id = 1146979933416067163

        no_card_edit_perms_role_id = 1157543775216861234

        self.pil_handler = pilHandler(kanrisha_client)

        self.event_handler = eventHandler(kanrisha_client, self.pil_handler)

        self.gachaCommandHandler = gachaCommandHandler(kanrisha_client, self.pil_handler)

        self.admin_command_handler = adminCommandHandler(kanrisha_client)

        self.leaderboard_handler = leaderboardHandler(kanrisha_client)

        ##-------------------start-of-register()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="register", description="Signs you up for the AiBG System.")
        async def register(interaction:discord.Interaction) -> None:

            """

            Registers a user to the bot, currently only admits the user to the bot's testing phase.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(await kanrisha_client.interaction_handler.whitelist_channel_check(interaction) == False):
                return

            register_message = """
            By clicking this button you acknowledge and agree to the following:\n
            - You will be using the bot during its testing phase, and any and all data may be wiped/lost at any time.\n
            - You will not hold the bot owner responsible for any data loss.\n
            - You may have to register multiple times during the testing phase.\n
            """

            if(await kanrisha_client.check_if_registered(interaction, register_check=True) == True):
                error_message = "You are already registered."

                ## get syndicate role
                aibg_role = kanrisha_client.get_guild(interaction.guild_id).get_role(self.event_handler.syndicate_role_id) ## type: ignore (we know it's not None)

                ## check if the member has the syndicate role
                if(aibg_role not in interaction.user.roles): ## type: ignore (we know it's not None)
                    error_message += "But are missing the AiBG role. You have been given the Syndicate role."

                    await interaction.user.add_roles(aibg_role) ## type: ignore (we know it's not None)

                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, response=error_message, delete_after=5.0, is_ephemeral=True)

                return

            embed = discord.Embed(title="Register", description=register_message, color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)
            embed.set_footer(text="This message will be deleted in 60 seconds.")

            ## Store the user's ID as a custom attribute of the button
            view = discord.ui.View().add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id=f"register_{interaction.user.id}", label="Register"))

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed, view=view, delete_after=60.0)

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

        @kanrisha_client.tree.command(name="profile", description="Sends a member's AiBG profile.")
        async def profile(interaction: discord.Interaction, member:typing.Union[discord.Member , None]):

            """
            
            Sends the user's profile.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(not await kanrisha_client.check_if_registered(interaction)):
                return
            
            await kanrisha_client.interaction_handler.defer_interaction(interaction)

            target_member, _, image_url, _ = await kanrisha_client.remote_handler.member_handler.get_aibg_member_object(interaction, member)

            if(target_member == None):
                await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, "That user is not registered.", is_ephemeral=True)
                return
            
            profile_message = (
                f"**Name:** {target_member.member_name}\n"
                f'**Credits:** {target_member.credits:,}\n'
                f"**Standard Spins:** {target_member.spin_scores[0]}\n"
                f"**Notable Spins:** {target_member.spin_scores[1]}\n"
                f"**Distinguished Spins:** {target_member.spin_scores[2]}\n"
                f"**Prime Spins:** {target_member.spin_scores[3]}\n"
                f"**Exclusive Spins:** {target_member.spin_scores[4]}"
            )

            embed = discord.Embed(title="Profile", description=profile_message, color=0xC0C0C0)
            embed.set_thumbnail(url=image_url)

            await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, embed=embed)

##-------------------start-of-get_card()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="card", description="Displays a card.")
        async def get_card(interaction:discord.Interaction, card_name:str) -> None:

            """
            
            Gets a card.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n
            member (object - discord.Member | None) : the member object.\n

            Returns:\n
            None.\n

            """

            ## Check if the user is registered
            if(not await kanrisha_client.check_if_registered(interaction)):
                return
            
            if(await kanrisha_client.interaction_handler.whitelist_channel_check(interaction) == False):
                return
            
            not_owned = False
            
            await kanrisha_client.interaction_handler.defer_interaction(interaction)

            ## get the syndicateMember object for the target member
            target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_aibg_member_object(interaction)
            
            ## get first 4 digits of card id for all member owned cards
            owned_card_ids = [card_id[0:4] for card_id in target_member.owned_card_ids] ## type: ignore (we know it's not None)

            ## get all names
            all_card_names = [card.name.lower() for card in kanrisha_client.remote_handler.gacha_handler.cards]

            ## run the name through the card name filter
            card_name = await kanrisha_client.toolkit.get_intended_card(card_name.lower(), all_card_names)

            ## get the card id for the given card name
            card_id = [card.id for card in kanrisha_client.remote_handler.gacha_handler.cards if card.name.lower() == card_name.lower()][0] ## type: ignore (we know it's not None)

            ## if target member owns card, get it
            if(card_id in owned_card_ids): ## type: ignore (we know it's not None)

                ## get card object from all cards
                card = [card for card in kanrisha_client.remote_handler.gacha_handler.cards if card.id == card_id][0] ## type: ignore (we know it's not None)

                ## get full sequence id from owned cards as well old id sequence
                full_user_sequence = target_member.owned_card_ids[owned_card_ids.index(card_id)] ## type: ignore (we know it's not None)

                ## modify card object to match user's id sequence
                card.replica.id = int(full_user_sequence[4])
                card.rarity.current_xp = int(full_user_sequence[5])

            ## if not, get the base card
            else:

                ## get card object from all cards
                card = [card for card in kanrisha_client.remote_handler.gacha_handler.cards if card.id == card_id][0]

                not_owned = True
    
            embed, file = await self.pil_handler.assemble_embed(card, not_owned=not_owned)

            ## reset card to default values if it was altered
            await card.reset_card_identifiers()

            await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, embed=embed, file=file)

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
            if(not await kanrisha_client.check_if_registered(interaction)):
                return
            
            if(await kanrisha_client.interaction_handler.whitelist_channel_check(interaction) == False):
                return
            
            await kanrisha_client.interaction_handler.defer_interaction(interaction)
            
            ## get the syndicateMember object for the target member
            target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_aibg_member_object(interaction, member)

            ## ensure user owns cards
            if(target_member.owned_card_ids == []): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, "That deck doesn't have any cards.", is_ephemeral=True)
                return
            
            ## get first 4 digits of card id for all member owned cards
            owned_card_ids = [card_id[0:4] for card_id in target_member.owned_card_ids] ## type: ignore (we know it's not None)

            ## get the card objects for the target member's owned cards, also grab full sequence id from owned cards
            owned_cards = [card for card in kanrisha_client.remote_handler.gacha_handler.cards if card.id in owned_card_ids] ## type: ignore (we know it's not None)
            sequence_ids = [target_member.owned_card_ids[owned_card_ids.index(card.id)] for card in owned_cards] ## type: ignore (we know it's not None)

            ## Create pairs of (owned_card, sequence_id)
            paired_list = list(zip(owned_cards, sequence_ids))

            ## Sort the pairs based on the rarity of the owned_card
            paired_list.sort(key=lambda x: x[0].rarity.id, reverse=True)

            ## Separate the sorted pairs back into two lists
            owned_cards, sequence_ids = zip(*paired_list)

            ## get the base card
            base_card = owned_cards[0]

            ## modify the base card to match the user's card
            base_card.replica.id = int(sequence_ids[0][4]) ## type: ignore (we know it's not going to be empty)
            base_card.rarity.current_xp = int(sequence_ids[0][5]) ## type: ignore (we know it's not going to be empty)

            embed, file = await self.pil_handler.assemble_embed(base_card) ## type: ignore (we know it's not None)
            
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

            kanrisha_client.view_dict[interaction.user.id] = view

            ## reset card to default values if it was altered
            await base_card.reset_card_identifiers() ## type: ignore (we know it's not None)

            await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, embed=embed, file=file, view=view)

##-------------------start-of-summary()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="summary", description="Show all cards and their ranks in a user's deck in a list format")
        async def summary(interaction:discord.Interaction, member:discord.Member | None) -> None:

            """

            Displays the user's deck in a list format.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n
            member (object - discord.Member | None) : the member object.\n
            
            Returns:\n
            None.\n

            """

            ## Check if the user is registered
            if(not await kanrisha_client.check_if_registered(interaction)):
                return
            
            if(await kanrisha_client.interaction_handler.whitelist_channel_check(interaction) == False):
                return
            
            await kanrisha_client.interaction_handler.defer_interaction(interaction)
            
            ## get the syndicateMember object for the target member
            target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_aibg_member_object(interaction, member)

            ## ensure user owns cards
            if(target_member.owned_card_ids == []): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, "That deck doesn't have any cards.", is_ephemeral=True)
                return
            
            ## get first 4 digits of card id for all member owned cards
            owned_card_ids = [card_id[0:4] for card_id in target_member.owned_card_ids] ## type: ignore (we know it's not None)

            ## get the card objects for the target member's owned cards, also grab full sequence id from owned cards
            owned_cards = [card for card in kanrisha_client.remote_handler.gacha_handler.cards if card.id in owned_card_ids]
            sequence_ids = [target_member.owned_card_ids[owned_card_ids.index(card.id)] for card in owned_cards] ## type: ignore (we know it's not None)

            ## Clone the original cards before modifying them
            owned_cards_clone = copy.deepcopy(owned_cards)

            ## Modify the cards based on sequence_ids
            for card, sequence_id in zip(owned_cards_clone, sequence_ids):
                card.replica.id = int(str(sequence_id)[4])  # Adjust index based on your actual sequence_id format
                card.rarity.current_xp = int(str(sequence_id)[5])  # Adjust index based on your actual sequence_id format

            ## Create pairs of (owned_card, sequence_id)
            paired_list = list(zip(owned_cards_clone, sequence_ids))

            ## First, sort the pairs based on the replica.id of the owned_card in descending order
            paired_list.sort(key=lambda x: x[0].replica.id, reverse=True)

            ## Then, sort the pairs based on the rarity.id of the owned_card in descending order
            paired_list.sort(key=lambda x: x[0].rarity.id, reverse=True)

            ## Separate the sorted pairs back into two lists
            owned_cards, sequence_ids = zip(*paired_list)

            card_list = ""

            for i, (card, sequence_id) in enumerate(zip(owned_cards, sequence_ids)):
                
                ## modify the card to match the user's sequence id
                card.replica.id = int(str(sequence_id)[4]) ## type: ignore (we know it's not going to be a string)
                card.rarity.current_xp = int(str(sequence_id)[5]) ## type: ignore (we know it's not going to be a string)

                ## need to force attribute update because it's usually handled by embed generation, which we're not using here
                await card.determine_attributes() ## type: ignore (we know it's not going to be a string)

                ## add card to embed
                card_list += f"{i + 1}. {card.rarity.emoji} {card.name} {card.replica.emoji} ({card.rarity.current_xp}/{card.rarity.max_xp})\n" ## type: ignore (we know it's not going to be a string)

                ## reset card to default values if it was altered
                await card.reset_card_identifiers() ## type: ignore (we know it's not going to be a string)

            embed = discord.Embed(title= f"{target_member.member_name}'s Deck", description=card_list) ## type: ignore (we know it's not None)

            await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, embed=embed)

##-------------------start-of-catalog()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="catalog", description="Shows all cards.")
        async def catalog(interaction:discord.Interaction) -> None:

            """

            Shows all cards.\n

            Is essentially a copy of the get_deck() function but with kanrisha as the target member.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(not await kanrisha_client.check_if_registered(interaction)):
                return

            if(await kanrisha_client.interaction_handler.whitelist_channel_check(interaction) == False):
                return
            
            await kanrisha_client.interaction_handler.defer_interaction(interaction)

            kanrisha_member = await kanrisha_client.fetch_user(kanrisha_client.interaction_handler.admin_user_ids[-1])

            kanrisha_syndicate_object, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_aibg_member_object(interaction, kanrisha_member) ## type: ignore (we know it's not None)

            ## get first 4 digits of card id for all member owned cards
            owned_card_ids = [card_id[0:4] for card_id in kanrisha_syndicate_object.owned_card_ids] ## type: ignore (we know it's not None)

            ## get the card objects for the target member's owned cards
            owned_cards = [card for card in kanrisha_client.remote_handler.gacha_handler.cards if card.id in owned_card_ids] ## type: ignore (we know it's not None)

            ## sort the cards by rarity
            owned_cards.sort(key=lambda x: x.rarity.id, reverse=True)

            embed, file = await self.pil_handler.assemble_embed(owned_cards[0])
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

            kanrisha_client.view_dict[interaction.user.id] = view

            await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, embed=embed, file=file, view=view)

##-------------------start-of-customize_card()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="customize-card", description="Customizes a card.")
        async def customize_card(interaction:discord.Interaction,
                                member:discord.Member | None,
                                card_picture_url:str | None,
                                card_picture_name:str | None,
                                card_picture_subtitle:str | None,
                                card_picture_description:str | None,
                                 ):

            """
            
            Customizes a card.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n
            member (object - discord.Member | None) : the member object.\n

            """

            async def has_non_ascii(text: str) -> bool:
                return any(ord(char) >= 128 for char in text)

            is_admin = True

            if(not await kanrisha_client.check_if_registered(interaction)):
                return
            
            if(not await kanrisha_client.interaction_handler.admin_check(interaction, display=False)):
                is_admin = False

            ## check if user is banned from editing cards
            no_card_edit_perms_role = kanrisha_client.get_guild(interaction.guild_id).get_role(no_card_edit_perms_role_id) ## type: ignore (we know it's not None)
            if(no_card_edit_perms_role in interaction.user.roles): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not allowed to edit cards.", delete_after=5.0, is_ephemeral=True)
                return
            
            ## ensure user is admin if using member argument
            if(member and is_admin == False and interaction.user.id != member.id): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You don't have permission to modify other user's cards.", delete_after=5.0, is_ephemeral=True)
                return

            ## get the syndicateMember object for the target member
            target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_aibg_member_object(interaction, member)

            ## check if the user is a card
            card_person_id = [card.person_id for card in kanrisha_client.remote_handler.gacha_handler.cards]
            if(target_member.member_id not in card_person_id): ## type: ignore (we know it's not None)
                if(member):
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "That user does not have a card.", delete_after=5.0, is_ephemeral=True)
                else:
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You do not have a card.", delete_after=5.0, is_ephemeral=True) 

                return
            
            ## get card object
            card = [card for card in kanrisha_client.remote_handler.gacha_handler.cards if card.person_id == target_member.member_id][0] ## type: ignore (we know it's not None)

            ## modify card object to match provided parameters
            banned_characters = ["\n", "\t", ","]

            ## if card_picture_url is provided, ensure it is a valid i.imgur url link.
            if(card_picture_url):

                required_start = "https://i.imgur.com/"

                require_ends = [".png", ".jpg", ".jpeg"]
        
                if(not card_picture_url.startswith(required_start)):
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "That is not a valid i.imgur url. Please note that only i.imgur urls are supported.", is_ephemeral=True)
                    return
                
                if(not any([card_picture_url.endswith(require_end) for require_end in require_ends])):
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "Link must end with .png, .jpg, or .jpeg.", is_ephemeral=True)
                    return
                
                if("gallery" in card_picture_url):
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You cannot use gallery links.", is_ephemeral=True)
                    return

                ## download the image to ensure validity
                if (not await self.pil_handler.test_pfp_validity(card_picture_url)):
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "That is not a valid image.", is_ephemeral=True)
                    return

                ## set card picture url
                card.picture_url = card_picture_url

            ## if card_picture_name is provided, ensure it is a valid string
            if(card_picture_name):

                if(any([banned_character in card_picture_name for banned_character in banned_characters])):
                        
                    ## get the banned character in the name
                    banned_character = [banned_character for banned_character in banned_characters if banned_character in card_picture_name][0]

                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"Card name cannot contain {banned_character}.", is_ephemeral=True)
                    return
                    
                if(len(card_picture_name) > 27):
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "That name is too long. Please limit it to 27 characters.", is_ephemeral=True)
                    return
                
                if(await has_non_ascii(card_picture_name)):
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "Card name cannot contain non-ascii characters.", is_ephemeral=True)
                    return

                ## set card picture name
                card.picture_name = card_picture_name

            ## if card_picture_subtitle is provided, ensure it is a valid string
            if(card_picture_subtitle):

                if(any([banned_character in card_picture_subtitle for banned_character in banned_characters])):

                    ## get the banned character in the subtitle
                    banned_character = [banned_character for banned_character in banned_characters if banned_character in card_picture_subtitle][0]

                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"Card subtitle cannot contain {banned_character}.", is_ephemeral=True)
            
                if(len(card_picture_subtitle) > 34):
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "That subtitle is too long. Please limit it to 34 characters.", is_ephemeral=True)
                    return
                
                if(await has_non_ascii(card_picture_subtitle)):
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "Card name cannot contain non-ascii characters.", is_ephemeral=True)
                    return

                ## set card picture subtitle
                card.picture_subtitle= card_picture_subtitle

            ## if card_picture_description is provided, ensure it is a valid string
            if(card_picture_description):

                if(any([banned_character in card_picture_description for banned_character in banned_characters])):
                            
                    ## get the banned character in the description
                    banned_character = [banned_character for banned_character in banned_characters if banned_character in card_picture_description][0]

                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"Card description cannot contain {banned_character}.", is_ephemeral=True)
                    return
                
                if(await has_non_ascii(card_picture_description)):
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "Card name cannot contain non-ascii characters.", is_ephemeral=True)
                    return
                
                if(len(card_picture_description) > 34):
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "That description is too long. Please limit it to 34 characters.", is_ephemeral=True)
                    return

                ## set card picture description
                card.picture_description = card_picture_description

            ## if all parameters are None, send error message
            if(not any([card_picture_url, card_picture_name, card_picture_subtitle, card_picture_description])):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You must provide at least one parameter to customize.", is_ephemeral=True)
                return
            
            ## if all parameters are valid, send success message
            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "Card successfully customized.", is_ephemeral=True)

##-------------------start-of-reset_card_customization()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="reset-card-customization", description="Resets a card's customization.")
        async def reset_card_customization(interaction:discord.Interaction, member:discord.Member | None) -> None:

            """
            
            Resets a card's customization.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n
            member (object - discord.Member | None) : the member object.\n

            """

            is_admin = True

            if(not await kanrisha_client.interaction_handler.admin_check(interaction, display=False)):
                is_admin = False
            
            if(not await kanrisha_client.check_if_registered(interaction)):
                return

            ## check if user is banned from editing cards
            no_card_edit_perms_role = kanrisha_client.get_guild(interaction.guild_id).get_role(no_card_edit_perms_role_id) ## type: ignore (we know it's not None)
            if(no_card_edit_perms_role in interaction.user.roles): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not allowed to edit cards.", delete_after=5.0, is_ephemeral=True)
                return
            
            ## ensure user is admin if using member argument
            if(member and not is_admin): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You don't have permission to modify other user's cards.", delete_after=5.0, is_ephemeral=True)
                return

            ## get the syndicateMember object for the target member
            target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_aibg_member_object(interaction, member)

            ## check if the user is a card
            card_person_id = [card.person_id for card in kanrisha_client.remote_handler.gacha_handler.cards]
            if(target_member.member_id not in card_person_id): ## type: ignore (we know it's not None)
                if(member):
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "That user does not have a card.", delete_after=5.0, is_ephemeral=True)
                else:
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You do not have a card.", delete_after=5.0, is_ephemeral=True)

                return
            
            ## get card object
            card = [card for card in kanrisha_client.remote_handler.gacha_handler.cards if card.person_id == target_member.member_id][0] ## type: ignore (we know it's not None)

            ## reset card to default values
            await card.reset_card_customization()

            ## send success message
            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "Card successfully reset.", is_ephemeral=True)

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

            if(not await kanrisha_client.check_if_registered(interaction)):
                return

            if(await kanrisha_client.interaction_handler.whitelist_channel_check(interaction) == False):
                return

            help_message = (
                "**/register** - Signs you up for AiBG.\n\n"
                "**/profile** - Sends a member's AiBG profile.\n\n"
                "**/starter-pack** - Lets you claim your starter pack.\n\n"
                "**/freebie** - Lets you claim your freebie.\n\n"
                "**/spin** - Spins the wheel to obtain a card. Costs 3k credits.\n\n"
                "**/multi-spin** - Spins the wheel multiple times to obtain 10 cards. Costs 27k credits.\n\n"
                "**/card** - Displays a card.\n\n"
                "**/deck** - Displays the user's deck.\n\n"
                "**/summary** - Show all cards in a user's deck in a list format.\n\n"
                "**/catalog** - Shows all cards in existence.\n\n"
                "**/customize-card** - Customizes a card.\n\n"
                "**/reset-card-customization** - Resets a card's customization.\n\n"
                "**/leaderboard** - Sends the leaderboards.\n\n"
                "**/snipe** - Fetches the last deleted message in a channel.\n\n"
                "**/help-commands** - Sends this message.\n\n"
            )

            embed = discord.Embed(title="Help", description=help_message, color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed)