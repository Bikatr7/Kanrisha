## built-in libraries
import random
import typing

class gachaHandler:


    """
    
    Handles all the gacha utility functions.
    

    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self):

        """

        Constructor for the gachaHandler class.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        pass

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

##-------------------start-of-spin_wheel()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def spin_wheel(self, user_id:int) -> typing.Tuple[str,int]:

        """

        Spins the wheel and returns the result.\n

        Parameters:\n
        self (object - gachaHandler) : the gachaHandler object.\n
        user_id (int) : the id of the user.\n

        Returns:\n
        result (str) : the result of the spin.\n

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

        if value_to_return == "<:shining:1144089713934864444>":
            spin_index = 0
        elif value_to_return == "<:glowing:1144089680934080512>":
            spin_index = 1
        else:
            spin_index = 2

        return value_to_return, spin_index

