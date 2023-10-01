## built-in libraries
import random
import typing
import os

## custom modules
from entities.card import card

from modules.fileEnsurer import fileEnsurer
from modules.toolkit import toolkit

from handlers.connectionHandler import connectionHandler

class gachaHandler:


    """
    
    Handles all the gacha utility functions.
    

    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, file_ensurer:fileEnsurer, toolkit:toolkit, connection_handler:connectionHandler) -> None:

        """

        Constructor for the gachaHandler class.\n

        Parameters:\n
        file_ensurer (object - fileEnsurer) : the fileEnsurer object.\n
        toolkit (object - toolkit) : the toolkit object.\n
        connection_handler (object - connectionHandler) : the connectionHandler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        self.file_ensurer = file_ensurer

        self.toolkit = toolkit

        self.connection_handler = connection_handler

        ## all the base cards
        self.cards:typing.List[card] = []

        ##----------------------------------------------------------------likelihoods----------------------------------------------------------------

        self.STANDARD_LIKELIHOOD = .55
        self.NOTABLE_LIKELIHOOD = .30
        self.DISTINGUISHED_LIKELIHOOD = .11
        self.PRIME_LIKELIHOOD = .03
        self.EXCLUSIVE_LIKELIHOOD = .01

        ##----------------------------------------------------------------ids----------------------------------------------------------------

        self.rarity_to_credits = {
            'Standard': 300,
            'Notable': 600,
            'Distinguished': 1200,
            'Prime': 2500,
            'Exclusive': 5000
        }

##-------------------start-of-load_cards_from_remote()---------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def load_cards_from_remote(self) -> None:

        """

        Loads the cards from the local db.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        ## clear the cards list
        self.cards.clear()

        card_id_list, replica_id_list, xp_id_list, name_list, rarity_list, picture_url_list, picture_name_list, picture_subtitle_list, picture_description_list, person_id_list = await self.connection_handler.read_multi_column_query("select card_id, card_replica_id, card_xp_id, card_name, card_rarity, card_picture_url, card_picture_name, card_picture_subtitle, card_picture_description, person_id from cards")

        for i in range(len(card_id_list)):

            new_card = card(card_id_list[i], int(replica_id_list[i]), int(xp_id_list[i]), name_list[i], int(rarity_list[i]), picture_url_list[i], picture_name_list[i], picture_subtitle_list[i], picture_description_list[i], int(person_id_list[i]))

            self.cards.append(new_card)

        await self.file_ensurer.logger.log_action("INFO", "gachaHandler", "Loaded cards from remote.")

##-------------------start-of-load_cards_from_local()---------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def load_cards_from_local(self) -> None:

        """

        Loads the cards from the cards folder.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        ## clear the cards list
        self.cards.clear()

        with open(self.file_ensurer.card_path, "r", encoding="utf-8") as file:

            for line in file:

                values = line.strip().split(',')

                card_id = values[0]
                card_replica_id = int(values[1])
                card_xp_id = int(values[2])
                card_name = values[3]
                card_rarity = int(values[4])
                card_picture_url = values[5]
                card_picture_name = values[6]
                card_picture_subtitle = values[7]
                card_picture_description = values[8]
                card_person_id = int(values[9])

                new_card = card(card_id, card_replica_id, card_xp_id, card_name, card_rarity, card_picture_url, card_picture_name, card_picture_subtitle, card_picture_description, card_person_id)

                self.cards.append(new_card)

        await self.file_ensurer.logger.log_action("INFO", "gachaHandler", "Loaded cards from local.")

##-------------------start-of-spin_gacha()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def spin_gacha(self) -> card:

        """
        
        Spins the gacha and returns the result.\n

        Parameters:\n
        self (object - gachaHandler) : the gachaHandler object.\n

        Returns:\n
        random_card (object - card) : the result of the spin.\n
        spin_index (int) : the type of spin.\n

        """

        ##----------------------------------------------------------------/

        async def get_rarity():

            chances = {
                "Standard": self.STANDARD_LIKELIHOOD,
                "Notable": self.NOTABLE_LIKELIHOOD,
                "Distinguished": self.DISTINGUISHED_LIKELIHOOD,
                "Prime": self.PRIME_LIKELIHOOD,
                "Exclusive": self.EXCLUSIVE_LIKELIHOOD
            }
            random_number = random.random()

            selection = ""

            cumulative_probability = 0

            for value, probability in chances.items():
                cumulative_probability += probability

                if(random_number <= cumulative_probability):
                    selection = value
                    break

            if(selection == "Standard"):
                rarity = 1

            elif(selection == "Notable"):
                rarity = 2

            elif(selection == "Distinguished"):
                rarity = 3
            
            elif(selection == "Prime"):
                rarity = 4

            else:
                rarity = 5

            return rarity
        
        ##----------------------------------------------------------------/

        possible_options = []

        ## get the rarity
        rarity = await get_rarity()

        ## picks a random card from the list of cards in matching rarity
        for card in self.cards:

            if(card.rarity.id == rarity):
                possible_options.append(card)

        random_card = random.choice(possible_options)

        return random_card