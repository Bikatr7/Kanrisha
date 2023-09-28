## built-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing

## third-party libraries
import discord
import json

## custom libraries
if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from bot.Kanrisha import Kanrisha

from entities.card import card

from handlers.pilHandler import pilHandler

class eventHandler:

    """
    
    Handles events.\n
    
    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_kanrisha_client:Kanrisha, inc_pil_handler:pilHandler) -> None:

        """
        
        Initializes the slash command handler.\n

        Parameters:\n
        kanrisha_client (object - Kanrisha) : the Kanrisha object.\n

        Returns:\n
        None.\n

        """

        kanrisha_client = inc_kanrisha_client

        self.file_ensurer = kanrisha_client.file_ensurer

        archive_channel_id = 1146979933416067163

        self.syndicate_role_id = 1146901009248026734 

        self.banned_messages = []

        self.pil_handler = inc_pil_handler

        ##-------------------start-of-on_member_remove()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.event
        async def on_member_remove(member:discord.Member) -> None:

            """

            Handles members leaving.\n

            Parameters:\n
            member (object - discord.Member | discord.User) : the member object.\n

            Returns:\n
            None.\n

            """

            roles = [role.id for role in member.roles] 

            ## loads the data from the file, adds the roles to the json object.
            with open(self.file_ensurer.role_persistence_path, 'r') as file:
                data = json.load(file)
                data[str(member.id)] = roles

            ## saves the data back to the file
            with open(self.file_ensurer.role_persistence_path, 'w') as file:
                json.dump(data, file)

        ##-------------------start-of-on_member_join()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.event
        async def on_member_join(member:discord.Member) -> None:

            """

            Handles members joining.\n

            Parameters:\n
            member (object - discord.Member | discord.User) : the member object.\n

            Returns:\n
            None.\n

            """

            ## loads the data from the file.
            with open(self.file_ensurer.role_persistence_path, 'r') as file:
                try:
                    data = json.load(file)

                except json.JSONDecodeError:
                    data = {}
                    
                ## checks if the member is in the json object, if they are, adds the roles to the member.
                roles = data.get(str(member.id))

                if(roles):
                    role_objects = [discord.utils.get(member.guild.roles, id=role_id) for role_id in roles if discord.utils.get(member.guild.roles, id=role_id) is not None]

                    if(role_objects):
                        try:
                            await member.add_roles(*[role for role in role_objects if role is not None])
                        except:
                            pass

                    del data[str(member.id)]
                    
            with open(self.file_ensurer.role_persistence_path, 'w') as file:
                json.dump(data, file)
    
        ##-------------------start-of-on_message()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.event
        async def on_message(message: discord.Message) -> None:

            """

            Handles messages.\n

            Parameters:\n
            self (object) : the eventHandler object.\n
            message (object) : the message object.\n

            Returns:\n
            None.\n

            """

            await check_banned_messages(message)

        ##-------------------start-of-check_banned_messages()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def check_banned_messages(message:discord.Message) -> None:

            """

            Checks for banned messages and deletes them.\n

            Parameters:\n
            self (object) : the eventHandler object.\n
            message (object) : the message object.\n

            Returns:\n
            None.\n

            """

            member = message.author

            guild = await kanrisha_client.fetch_guild(kanrisha_client.pg)

            try:
                member = await guild.fetch_member(member.id)
            except:
                pass

            channel = kanrisha_client.get_channel(message.channel.id) 

            seinu = await kanrisha_client.fetch_user(kanrisha_client.interaction_handler.owner_id)

            for banned_message in self.banned_messages:
                if(banned_message in message.content):

                    try:
                        await message.delete()

                        await kanrisha_client.file_ensurer.logger.log_action("ALERT", "eventHandler", f"Deleted banned message from {member.name} in {channel.name}.") ## type: ignore (we know it's not None)

                        await member.send(f"Your banned message has been deleted in {channel.name}. You may face penalties depending on severity.") ## type: ignore (we know it's not None)
                        await seinu.send(f"{member.name} sent a banned message in {channel.name}. See {banned_message} for details.") ## type: ignore (we know it's not None)  

                        await kanrisha_client.file_ensurer.logger.log_action("ALERT", "eventHandler", f"{member.name} sent a banned message in {channel.name}. See {banned_message} for details.") ## type: ignore (we know it's not None)

                    except:
                        pass

        ##-------------------start-of-on_raw_message_delete()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.event
        async def on_raw_message_delete(payload: discord.RawMessageDeleteEvent) -> None:

            """

            Stores deleted messages in a channel for later.\n

            Parameters:\n
            self (object) : the eventHandler object.\n
            payload (object) : the payload object.\n

            Returns:\n
            None.\n

            """

            ## check if the message was cached and if it was not sent by a bot or the owner cause we don't want to store those
            if(payload.cached_message and not payload.cached_message.author.bot and payload.cached_message.author.id != kanrisha_client.interaction_handler.owner_id):
                store_channel = kanrisha_client.get_channel(archive_channel_id)

                message_cache = payload.cached_message
                message_content = message_cache.content

                for banned_message in self.banned_messages:
                    if(banned_message in message_content):
                        return

                if(len(message_cache.attachments) > 0):
                    for attachment in message_cache.attachments:
                        message_content += "\n" + str(attachment)

                embed = discord.Embed(title=message_cache.author.name, description=message_content, color=0xC0C0C0)

                if(message_cache.author.avatar):
                    embed.set_thumbnail(url=message_cache.author.avatar.url)

                timestamp = int(message_cache.created_at.now().timestamp())

                embed.set_footer(text=f'Deleted in #{message_cache.channel.name}') ## type: ignore (we know it's not None)
                embed.add_field(name="Deleted at", value=f"<t:{timestamp}:F>") ## type: ignore (we know it's not None)
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

            ##----------------------------------------------/

            async def check_register_button(interaction: discord.Interaction, custom_id) -> None:

                ## if register button was pressed by the correct user
                if(custom_id == f"register_{interaction.user.id}"):

                    syndicate_role = kanrisha_client.get_guild(interaction.guild_id).get_role(self.syndicate_role_id) ## type: ignore (we know it's not None)

                    ## acknowledge the interaction immediately
                    await kanrisha_client.interaction_handler.defer_interaction(interaction, is_ephemeral=True, is_thinking=True) 

                    ## delete the register message
                    await interaction.message.delete() ## type: ignore (we know it's not None)

                    await kanrisha_client.remote_handler.member_handler.add_new_member(interaction.user.id, interaction.user.name, tuple([0,0,0,0,0]), 50000) # type: ignore

                    await interaction.followup.send("You have been registered.", ephemeral=True)

                    await kanrisha_client.file_ensurer.logger.log_action("INFO", "slashCommandHandler", f"{interaction.user.name} has been registered.") ## type: ignore (we know it's not None)

                    await interaction.user.add_roles(syndicate_role) ## type: ignore (we know it's not None)

                ## if register button was pressed by the wrong user
                elif(custom_id and custom_id.startswith("register_")):

                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not authorized to use this button.", delete_after=5.0, is_ephemeral=True)

            ##----------------------------------------------/

            async def get_owned_cards(deck_owner:discord.User) -> typing.Tuple[typing.List[card], typing.List[str], int]:

                ## get the current card index
                current_index = int(interaction.message.embeds[0].footer.text.split("/")[0]) - 1 ## type: ignore (we know it's not None)

                ## get the target member's syndicateMember object
                target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_syndicate_member(interaction, deck_owner) 

                ## get first 4 digits of card id for all member owned cards
                owned_card_ids = [card_id[0:4] for card_id in target_member.owned_card_ids] ## type: ignore (we know it's not None)

                ## get the card objects for the target member's owned cards, as well as the sequence ids
                owned_cards = [card for card in kanrisha_client.remote_handler.gacha_handler.cards if card.actual_id in owned_card_ids] ## type: ignore (we know it's not None)
                sequence_ids = [target_member.owned_card_ids[owned_card_ids.index(card.actual_id)] for card in owned_cards] ## type: ignore (we know it's not None)

                ## Create pairs of (owned_card, sequence_id)
                paired_list = list(zip(owned_cards, sequence_ids))

                ## Sort the pairs based on the rarity of the owned_card
                paired_list.sort(key=lambda x: x[0].rarity.identifier, reverse=True)

                ## Separate the sorted pairs back into two lists
                owned_cards, sequence_ids = zip(*paired_list)

                return owned_cards, sequence_ids, current_index ## type: ignore (we know it's not empty)

            ##----------------------------------------------/

            async def check_left_deck_button(interaction: discord.Interaction, custom_id:str) -> None:

                target_id_portion = f"deck_left_{interaction.user.id}."

                ## if left deck button was pressed by the correct user
                if(target_id_portion in custom_id):

                    ## get deck owner member object
                    member_id = int(custom_id.replace(target_id_portion, ""))
                    deck_owner = await kanrisha_client.fetch_user(member_id)

                    ## get the current cards and index
                    owned_cards, sequence_ids, current_index = await get_owned_cards(deck_owner)

                    ## calculate the new index to display
                    new_index = current_index - 1 if current_index > 0 else len(owned_cards) - 1

                    ## get the card to display, and create a safe copy of it
                    card_to_display = owned_cards[new_index]
                    safe_card_to_display = card_to_display

                    ## alter card to match user's sequence id
                    card_to_display.replica.identifier = int(sequence_ids[new_index][4]) ## type: ignore (we know it's not going to be empty)
                    card_to_display.rarity.current_xp = int(sequence_ids[new_index][5]) ## type: ignore (we know it's not going to be empty)

                    new_embed, file = await self.pil_handler.assemble_embed(card_to_display)

                    new_embed.set_footer(text=f"{new_index + 1}/{len(owned_cards)}")

                    new_embed, file = await self.pil_handler.assemble_embed(card_to_display)

                    new_embed.set_footer(text=f"{new_index + 1}/{len(owned_cards)}")

                    ## set card to display back to the safe copy
                    card_to_display = safe_card_to_display

                    new_embed.set_image(url=f"attachment://{file.filename}")

                    await interaction.response.edit_message(embed=new_embed,attachments=[file])

                ## if left deck button was pressed by the wrong user
                elif(custom_id and custom_id.startswith("deck_left_")):

                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not authorized to use this button.", delete_after=5.0, is_ephemeral=True)

            ##----------------------------------------------/

            async def check_right_deck_button(interaction: discord.Interaction, custom_id:str) -> None:

                target_id_portion = f"deck_right_{interaction.user.id}."

                ## if right deck button was pressed by the correct user

                if(target_id_portion in custom_id):

                    ## get deck owner member object
                    member_id = int(custom_id.replace(target_id_portion, ""))
                    deck_owner = await kanrisha_client.fetch_user(member_id)

                    ## get the current cards and index
                    owned_cards, sequence_ids, current_index = await get_owned_cards(deck_owner)

                    ## calculate the new index to display
                    new_index = current_index + 1 if current_index < len(owned_cards) - 1 else 0

                    ## get the card to display, and create a safe copy of it
                    card_to_display = owned_cards[new_index]
                    safe_card_to_display = card_to_display

                    ## alter card to match user's sequence id
                    card_to_display.replica.identifier = int(sequence_ids[new_index][4]) ## type: ignore (we know it's not going to be empty)
                    card_to_display.rarity.current_xp = int(sequence_ids[new_index][5]) ## type: ignore (we know it's not going to be empty)

                    new_embed, file = await self.pil_handler.assemble_embed(card_to_display)

                    new_embed.set_footer(text=f"{new_index + 1}/{len(owned_cards)}")

                    ## set card to display back to the safe copy
                    card_to_display = safe_card_to_display

                    new_embed.set_image(url=f"attachment://{file.filename}")

                    await interaction.response.edit_message(embed=new_embed, attachments=[file])

                ## if right deck button was pressed by the wrong user
                elif(custom_id and custom_id.startswith("deck_right_")):

                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not authorized to use this button.", delete_after=5.0, is_ephemeral=True)

            ##----------------------------------------------/
                
            ## check if it's a button press
            if(interaction.type == discord.InteractionType.component):

                ## get the custom id of the button
                custom_id = str(interaction.data.get("custom_id")) if interaction.data else ""

                ## check if the button is the register button
                await check_register_button(interaction, custom_id)

                ## check deck/catalog buttons
                await check_left_deck_button(interaction, custom_id)
                await check_right_deck_button(interaction, custom_id)


##-------------------start-of-setup_moderation()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def setup_moderation(self) -> None:

        """

        Reads the banned links file.\n

        Parameters:\n
        self (object) : the eventHandler object.\n

        Returns:\n
        None.\n

        """

        with open(self.file_ensurer.banned_links_path, "r") as file:
            self.banned_messages = file.read().splitlines()

        await self.file_ensurer.logger.log_action("INFO", "eventHandler", "Banned messages have been loaded.") ## type: ignore (we know it's not None)