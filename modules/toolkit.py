## built-in modules
import os
import msvcrt

## custom modules
from modules.fileEnsurer import fileEnsurer

class toolkit():

    """
    
    The class for a bunch of utility functions used throughout Kanrisha.\n

    """

##-------------------start-of-__init__()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_file_ensurer:fileEnsurer) -> None:

        """
        
        Constructor for the toolkit class.\n

        Parameters:\n
        inc_file_ensurer (object - fileEnsurer) : the fileEnsurer object.\n

        Returns:\n
        None.\n

        """

        self.file_handler = inc_file_ensurer

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
            
            msvcrt.getch() 

        else:  ## Linux, No idea if any of this works lmao

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

##-------------------start-of-get_elapsed_time()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_token(self) -> str:

        """

        Gets the token from the token.txt file for Kanrisha.\n

        Parameters:\n
        self (object - toolkit) : the toolkit object.\n

        Returns:\n
        token (str) : the token for Kanrisha.\n

        """
        
        token = ""

        try:
            with open(self.file_handler.token_path, 'r', encoding='utf-8') as file: 
                token = file.read()

            assert token != "" and token != "token"

        except Exception as e: ## else try to get api key manually

            token = input("DO NOT DELETE YOUR COPY OF THE TOKEN\n\nPlease enter the token of 'The Gamemaster' : ")

            with open(self.file_handler.token_path, 'w+', encoding='utf-8') as file: 
                file.write(token)
                
        finally:
                return token