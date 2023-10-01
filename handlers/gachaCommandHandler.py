## built-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing

## third-party libraries
import discord

## custom modules
from handlers.pilHandler import pilHandler

from entities.card import card

if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from bot.Kanrisha import Kanrisha

class gachaCommandHandler:

    """
    
    Handles slash commands.\n

    """


##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_kanrisha_client:Kanrisha, inc_pil_handler:pilHandler) -> None:

        """
        
        Initializes the slash command handler.\n

        Parameters:\n
        inc_kanrisha_client (object - Kanrisha) : the Kanrisha client object.\n

        Returns:\n
        None.\n

        """

        kanrisha_client = inc_kanrisha_client

        pil_handler = inc_pil_handler

##-------------------start-of-starter_pack()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="starter-pack", description="Gives you a starter pack.")
        async def starter_pack(interaction:discord.Interaction) -> None:

            """

            Gives the user a starter pack.\n

            Parameters:\n
            member (object - discord.Member) : the member object.\n

            Returns:\n
            None.\n

            """

            if(not await kanrisha_client.check_if_registered(interaction)):
                return
            
            if(await kanrisha_client.interaction_handler.whitelist_channel_check(interaction) == False):
                return
            
            if(not await kanrisha_client.interaction_handler.admin_check(interaction)):
                return

            ## get the syndicateMember object for the target member
            target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_aibg_member_object(interaction)

            ## manually check if user has already claimed their starter pack
            if(target_member.owned_card_ids != []): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You have already claimed your starter pack.", delete_after=3.0, is_ephemeral=True)
                return
            
            ## keep spinning until the user has 5 cards, all cards are Standard and unique
            starter_cards = []
            while(len(starter_cards) < 5):

                ## spin the gacha
                card:card = await kanrisha_client.remote_handler.gacha_handler.spin_gacha()

                ## if the card is not common, skip it
                if(card.rarity.name != "Standard"):
                    continue

                ## if the card is already in the starter pack, skip it
                if(card in starter_cards):
                    continue

                starter_cards.append(card)

            ## give the user the cards
            for card in starter_cards:
                
                ## remember that the owned_card_ids list holds a full sequence id, so we need to get the id from the card object and add 2 0's to the end to get the full sequence id (6 digits)
                target_member.owned_card_ids.append(f"{card.id}00") ## type: ignore (we know it's not None)

            ## award the user 15000 credits
            target_member.credits += 15000 ## type: ignore (we know it's not None)

            ## build embed
            display_message = "You have been awarded 15000 credits and the following cards:\n"

            for card in starter_cards:
                display_message += f"{card.rarity.emoji} {card.name}\n"

            embed = discord.Embed(title="Starter Pack", description=display_message, color=0xC0C0C0)

            ## send response
            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed)

        ##-------------------start-of-gacha_spin()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="spin", description="Spins the wheel to obtain a card Costs 3k credits.")
        async def gacha_spin(interaction: discord.Interaction) -> None:

            """

            Spins the gacha wheel.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(not await kanrisha_client.check_if_registered(interaction)):
                return
            
            if(await kanrisha_client.interaction_handler.whitelist_channel_check(interaction) == False):
                return
            
            if(not await kanrisha_client.interaction_handler.admin_check(interaction)):
                return

            ## get the syndicateMember object for the target member
            target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_aibg_member_object(interaction)

            ## make sure user has claimed their starter pack
            if(target_member.owned_card_ids == []): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You must claim your starter pack before spinning. (/starter-pack)", delete_after=3.0, is_ephemeral=True)
                return
            
            ## if user does not have enough credits, return
            if(target_member.credits < 27000 and interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids): ## type: ignore (we know it's not None
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You do not have enough credits. (3000)", delete_after=3.0, is_ephemeral=True)
                return

            ## get card
            card = await kanrisha_client.remote_handler.gacha_handler.spin_gacha()

            ## update spin scores (id - 1 because the spin scores are stored in a list and the rarity id starts at 1)
            await kanrisha_client.remote_handler.member_handler.update_spin_value(target_member.member_id, 1, card.rarity.id - 1) ## type: ignore (we know it's not None)

            ## get first 4 digits of card id for all member owned cards, because this is what is used to determine cards
            owned_card_ids = [card_id[0:4] for card_id in target_member.owned_card_ids] ## type: ignore (we know it's not None)

            ## if the member doesn't own the card, add it to their owned_card_ids list, use a blank 0 for rarity and xp ids
            if(card.id not in owned_card_ids): ## type: ignore (we know it's not None)

                ## remember that the owned_card_ids list holds a full sequence id, so we need to get the id from the card object and add 2 0's to the end to get the full sequence id (6 digits)
                target_member.owned_card_ids.append(f"{card.id}00") ## type: ignore (we know it's not None)

                embed, file = await pil_handler.assemble_embed(card)

            else:
                
                ## the whole idea of this is that the member doesn't actually have any "card" objects, they just have the id sequence of the card
                ## gacha_handler has the "Base" card objects, and the member's owned_card_ids list is just how the card should be altered
                ## card needs to be reset after display due to objects being passed by reference

                ## if card is owned get the id sequence from the member's owned cards
                full_user_sequence = target_member.owned_card_ids[owned_card_ids.index(card.id)] ## type: ignore (we know it's not None)

                ## modify card object to match user's id sequence
                card.replica.id = int(str(full_user_sequence)[4])
                card.rarity.current_xp = int(str(full_user_sequence)[5])

                ## if the card's replica is not maxed, increase the xp and id
                if(card.replica.id != 6):
                    card.rarity.current_xp += 1

                    ## if the card's xp is maxed, reset the xp and increase the id
                    if(card.rarity.current_xp >= card.rarity.max_xp):
                        card.rarity.current_xp = 0
                        card.replica.id += 1

                    ## get new sequence id for user's card
                    new_id_sequence = card.id + f"{card.replica.id}{card.rarity.current_xp}"

                    ## replace in array 
                    target_member.owned_card_ids[owned_card_ids.index(card.id)] = new_id_sequence ## type: ignore (we know it's not None)

                    ## user card for embed
                    embed, file = await pil_handler.assemble_embed(card)

                ## add credits to the member's balance based on the card's rarity if the card's replica is maxed
                else:

                    credits_to_add = kanrisha_client.remote_handler.gacha_handler.rarity_to_credits.get(card.rarity.name, 0) 
                    target_member.credits += credits_to_add ## type: ignore (we know it's not None)

                    embed, file = await pil_handler.assemble_embed(card)

                    embed.set_footer(text=f"You have this card maxed out. You have been awarded {credits_to_add} credits.")

            ## reset card to default values if it was altered
            await card.reset_card_identifiers()

            ## decrement credits
            target_member.credits -= 3000 ## type: ignore (we know it's not None)

            await kanrisha_client.interaction_handler.send_response_filter_channel(interaction, embed=embed, file=file)

##-------------------start-of-multispin()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="multispin", description="Spins the wheel multiple times to obtain 10 cards. Costs 27k credits.")
        async def multispin(interaction:discord.Interaction) -> None:

            """
            
            Spins the gacha wheel multiple times.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(not await kanrisha_client.check_if_registered(interaction)):
                return
            
            if(await kanrisha_client.interaction_handler.whitelist_channel_check(interaction) == False):
                return
            
            ## admin check
            if(not await kanrisha_client.interaction_handler.admin_check(interaction)):
                return

            ## get the syndicateMember object for the target member
            target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_aibg_member_object(interaction)

            ## make sure user has claimed their starter pack
            if(target_member.owned_card_ids == []): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You must claim your starter pack before spinning. (/starter-pack)", delete_after=3.0, is_ephemeral=True)
                return
            
            ## if user does not have enough credits, return
            if(target_member.credits < 27000 and interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids): ## type: ignore (we know it's not None
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You do not have enough credits. (27000)", delete_after=3.0, is_ephemeral=True)
                return
            
            ## defer response
            await kanrisha_client.interaction_handler.defer_interaction(interaction)

            ## build embed message
            display_message = "You have been awarded the following cards:\n"

            footer = ""

            total_credits_added = 0

            ## get cards
            cards = []
            while(len(cards) < 10):

                ## spin the gacha
                card:card = await kanrisha_client.remote_handler.gacha_handler.spin_gacha()

                cards.append(card)

                ## update spin scores (id - 1 because the spin scores are stored in a list and the rarity id starts at 1)
                await kanrisha_client.remote_handler.member_handler.update_spin_value(target_member.member_id, 1, card.rarity.id - 1) ## type: ignore (we know it's not None)

                ## get first 4 digits of card id for all member owned cards, because this is what is used to determine cards
                owned_card_ids = [card_id[0:4] for card_id in target_member.owned_card_ids] ## type: ignore (we know it's not None)

                ## add card to display message
                display_message += f"{card.rarity.emoji} {card.name}\n"

                ## if the member doesn't own the card, add it to their owned_card_ids list, use a blank 0 for rarity and xp ids
                if(card.id not in owned_card_ids): ## type: ignore (we know it's not None)

                    ## remember that the owned_card_ids list holds a full sequence id, so we need to get the id from the card object and add 2 0's to the end to get the full sequence id (6 digits)
                    target_member.owned_card_ids.append(f"{card.id}00") ## type: ignore (we know it's not None)

                else:
                    
                    ## the whole idea of this is that the member doesn't actually have any "card" objects, they just have the id sequence of the card
                    ## gacha_handler has the "Base" card objects, and the member's owned_card_ids list is just how the card should be altered
                    ## card needs to be reset after display due to objects being passed by reference

                    ## if card is owned get the id sequence from the member's owned cards
                    full_user_sequence = target_member.owned_card_ids[owned_card_ids.index(card.id)] ## type: ignore (we know it's not None)

                    ## modify card object to match user's id sequence
                    card.replica.id = int(str(full_user_sequence)[4])
                    card.rarity.current_xp = int(str(full_user_sequence)[5])

                    ## if the card's replica is not maxed, increase the xp and id
                    if(card.replica.id != 6):
                        card.rarity.current_xp += 1

                        ## if the card's xp is maxed, reset the xp and increase the id
                        if(card.rarity.current_xp >= card.rarity.max_xp):
                            card.rarity.current_xp = 0
                            card.replica.id += 1

                        ## get new sequence id for user's card
                        new_id_sequence = card.id + f"{card.replica.id}{card.rarity.current_xp}"

                        ## replace in array 
                        target_member.owned_card_ids[owned_card_ids.index(card.id)] = new_id_sequence ## type: ignore (we know it's not None)

                    ## add credits to the member's balance based on the card's rarity if the card's replica is maxed
                    else:

                        credits_to_add = kanrisha_client.remote_handler.gacha_handler.rarity_to_credits.get(card.rarity.name, 0) 
                        target_member.credits += credits_to_add ## type: ignore (we know it's not None)

                        total_credits_added += credits_to_add

                        ## adjust footer
                        if(footer == ""):
                            footer = f"You have the following cards maxed out."
                        
                        footer += f"{card.rarity.emoji} {card.name}\n"

                        ## reset card to default values if it was altered
                        await card.reset_card_identifiers()

            ## build embed
            embed = discord.Embed(title="Multispin", description=display_message, color=0xC0C0C0)

            if(footer != ""):
                footer += f"\nYou have been awarded {total_credits_added} credits for maxed cards."

            embed.set_footer(text=footer)

            ## decrement credits
            target_member.credits -= 27000 ## type: ignore (we know it's not None)

            await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, embed=embed)

##-------------------start-of-freebie()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="freebie", description="Lets you claim your freebie.")
        async def freebie(interaction:discord.Interaction) -> None:

            """
            
            Lets you claim your freebie.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            ## check if user is registered
            if(not await kanrisha_client.check_if_registered(interaction)):
                return
            
            if(await kanrisha_client.interaction_handler.whitelist_channel_check(interaction) == False):
                return
            
            if(not await kanrisha_client.interaction_handler.admin_check(interaction)):
                return
            
            ## get the syndicateMember object for the target member
            target_member, _, _, _ = await kanrisha_client.remote_handler.member_handler.get_aibg_member_object(interaction)
            
            ## make sure user has claimed their starter pack
            if(target_member.owned_card_ids == []): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You must claim your starter pack before using your freebie (/starter-pack)", delete_after=3.0, is_ephemeral=True)
                return
            
            ## check if user has freebie
            if(target_member.has_freebie == False): ## type: ignore (we know it's not None)
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You have already claimed your freebie.", delete_after=3.0, is_ephemeral=True)
                return

            ## award freebie
            else:
                target_member.credits += 1000 ## type: ignore (we know it's not None)
                target_member.has_freebie = False ## type: ignore (we know it's not None)

            ## send response
            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"You have been awarded 1000 credits. You now have {target_member.credits} credits.", is_ephemeral=True) ## type: ignore (we know it's not None)
