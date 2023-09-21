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
        None.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        self.file_ensurer = file_ensurer

        self.toolkit = toolkit

        self.connection_handler = connection_handler

        self.cards:typing.List[card] = []

        ##----------------------------------------------------------------ids----------------------------------------------------------------

        self.lucky_number_ids = [
            202873006773633024,
            436459842027257856,
            455888741530075154,
            349950984295809047,
            752579862560243852,
            149722929586765824,
            758665097013886996,
        ]

        self.godlike_ids = [
            957451091748986972
        ]

##-------------------start-of-load_cards_from_remote()---------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def load_cards_from_remote(self) -> None:

        """

        Loads the cards from the local db.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        self.cards.clear()

        id_list, name_list, rarity_list, picture_path_list, picture_url_list = await self.connection_handler.read_multi_column_query("select card_id, card_name, card_rarity, card_picture_path, card_picture_url from cards")

        for i in range(len(id_list)):

            new_card = card(int(id_list[i]), name_list[i], int(rarity_list[i]), picture_path_list[i], picture_url_list[i])

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

        self.cards.clear()

        with open(self.file_ensurer.card_path, "r", encoding="utf-8") as file:

            for line in file:

                values = line.strip().split(',')

                card_id = int(values[0])
                card_name = values[1]
                card_rarity = int(values[2])
                card_picture_path = os.path.join(self.file_ensurer.gacha_images_dir, values[3])
                card_picture_url = values[4]

                new_card = card(card_id, card_name, card_rarity, card_picture_path, card_picture_url)

                self.cards.append(new_card)

        await self.file_ensurer.logger.log_action("INFO", "gachaHandler", "Loaded cards from local.")

##-------------------start-of-spin_wheel()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def spin_wheel(self, user_id:int) -> typing.Tuple[str,int]:

        """

        Spins the wheel and returns the result.\n

        Parameters:\n
        self (object - gachaHandler) : the gachaHandler object.\n
        user_id (int) : the id of the user.\n

        Returns:\n
        value_to_return (str) : the result of the spin.\n
        spin_index (int) : the type of spin.\n

        """

        if(user_id in self.lucky_number_ids):
            chances = {
                "<:shining:1144089713934864444>": 0.05,
                "<:glowing:1144089680934080512>": 0.12,
                "<:common:1144089649174814730>": 0.83
            }

        elif(user_id not in self.godlike_ids):
            chances = {
                "<:shining:1144089713934864444>": 0.08,
                "<:glowing:1144089680934080512>": 0.14,
                "<:common:1144089649174814730>": 0.78
            }

        else:
            chances = {
                "<:shining:1144089713934864444>": 0.50,
                "<:glowing:1144089680934080512>": 0.30,
                "<:common:1144089649174814730>": 0.20,
            }

        value_to_return = ""
        
        random_number = random.random()

        cumulative_probability = 0

        for value, probability in chances.items():
            cumulative_probability += probability

            if(random_number <= cumulative_probability):
                value_to_return = value
                break

        if(value_to_return == "<:shining:1144089713934864444>"):
            spin_index = 0
        elif(value_to_return == "<:glowing:1144089680934080512>"):
            spin_index = 1
        else:
            spin_index = 2

        return value_to_return, spin_index


##-------------------start-of-spin_gacha()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def spin_gacha(self, user_id:int) -> card:

        """
        
        Spins the gacha and returns the result.\n

        Parameters:\n
        self (object - gachaHandler) : the gachaHandler object.\n
        user_id (int) : the id of the user.\n

        Returns:\n
        random_card (object - card) : the result of the spin.\n
        spin_index (int) : the type of spin.\n

        """

        ##----------------------------------------------------------------/

        async def get_rarity():

            chances = {
                "Standard": 0.55,
                "Notable": 0.30,
                "Distinct": 0.12,
                "Prime": 0.03,
                "Exclusive": 0.00
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

            elif(selection == "Distinct"):
                rarity = 3
            
            elif(selection == "Prime"):
                rarity = 4

            else:
                rarity = 5

            return rarity
        
        ##----------------------------------------------------------------/

        possible_options = []
        spin_index = 0

        rarity = await get_rarity()

        for card in self.cards:

            if(card.rarity.identifier == rarity):
                possible_options.append(card)

        random_card = random.choice(possible_options)

        return random_card