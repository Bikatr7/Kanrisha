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

##-------------------start-of-spin_wheel()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def spin_wheel(self) -> typing.Tuple[str,int]:

        """

        Spins the wheel and returns the result.\n

        Parameters:\n
        self (object - gachaHandler) : the gachaHandler object.\n

        Returns:\n
        result (str) : the result of the spin.\n

        """

        chances = {
            "<:shining:1144089713934864444>": 0.05,
            "<:glowing:1144089680934080512>": 0.12,
            "<:common:1144089649174814730>": 0.83
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

