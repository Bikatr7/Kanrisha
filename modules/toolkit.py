## built-in modules
import os
import typing

## custom modules
from modules.logger import logger

class toolkit():

    """
    
    The class for a bunch of utility functions used throughout Kanrisha.\n

    """

##-------------------start-of-__init__()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_logger:logger) -> None:

        """
        
        Constructor for the toolkit class.\n

        Parameters:\n
        inc_logger (object - logger) : the logger object.\n

        Returns:\n
        None.\n

        """

        self.logger = inc_logger

##-------------------start-of-clear_console()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def clear_console(self) -> None:

        """

        clears the console\n

        Parameters:\n
        self (object - toolkit) : the toolkit object.\n

        Returns:\n
        None\n

        """

        os.system('cls' if os.name == 'nt' else 'clear')
        
##-------------------start-of-pause_console()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def pause_console(self, message:str="Press any key to continue...") -> None:

        """

        Pauses the console.\n

        Parameters:\n
        self (object - toolkit) : the toolkit object.\n
        message (str | optional) : the message that will be displayed when the console is paused.\n

        Returns:\n
        None\n

        """

        print(message)  ## Print the custom message
        
        if(os.name == 'nt'):  ## Windows

            import msvcrt
            
            msvcrt.getch() 

        else:  ## Linux

            import termios

            ## Save terminal settings
            old_settings = termios.tcgetattr(0)

            try:
                new_settings = termios.tcgetattr(0)
                new_settings[3] = new_settings[3] & ~termios.ICANON
                termios.tcsetattr(0, termios.TCSANOW, new_settings)
                os.read(0, 1)  ## Wait for any key press

            finally:

                termios.tcsetattr(0, termios.TCSANOW, old_settings)

##--------------------start-of-levenshtein()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def levenshtein(self, string_one:str, string_two:str) -> int:

        """

        Compares two strings for similarity.\n

        Parameters:\n
        self (object - scoreRate): The scoreRate class object.\n
        string_one (str) : the first string to compare.\n
        string_two (str) : the second string to compare.\n

        Returns:\n
        distance[sLength1][sLength2] (int) : the minimum number of single-character edits required to transform string_one into string_two.\n

        """

        sLength1, sLength2 = len(string_one), len(string_two)
        distance = [[0] * (sLength2 + 1) for _ in range(sLength1 + 1)]
        
        for i in range(sLength1 + 1):
            distance[i][0] = i

        for ii in range(sLength2 + 1):
            distance[0][ii] = ii

        for i in range(1, sLength1 + 1):
            for ii in range(1, sLength2 + 1):

                if(string_one[i - 1] == string_two[ii - 1]):
                    cost = 0
                else:
                    cost = 1

                distance[i][ii] = min(distance[i - 1][ii] + 1, distance[i][ii- 1] + 1, distance[i - 1][ii - 1] + cost)

                if(i > 1 and ii > 1 and string_one[i-1] == string_two[ii-2] and string_one[i-2] == string_two[ii-1]):
                    distance[i][ii] = min(distance[i][ii], distance[i-2][ii-2] + cost)

        return distance[sLength1][sLength2]

##--------------------start-of-get_intended_answer()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def get_intended_card(self, user_requested_string:str, card_names:typing.List[str]) -> str:

        """
        
        When a typo has been previously encountered, we need to determine what they were trying to type and return that instead.\n

        Parameters:\n
        self (object - scoreRate) : The scoreRate class object.\n
        typo (str) : the typo the user made.\n
        correct_answers (list - str) : list of correct answers the typo could match.\n

        Returns:\n
        closest_string (str) : the string the user was trying to type.\n

        """

        closest_distance = float('inf')
        closest_string = ""

        for string in card_names:
            distance = await self.levenshtein(user_requested_string, string)
            if(distance < closest_distance):
                closest_distance = distance
                closest_string = string

        return closest_string.lower()