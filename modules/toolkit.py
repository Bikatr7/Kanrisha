## built-in modules
from datetime import datetime

import os

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

##-------------------start-of-get_timestamp()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def get_timestamp(self, type, module) -> str:

        """
        
        Gets a formatted timestamp.\n

        Parameters:\n
        self (object - toolkit) : the toolkit object.\n
        type (str) : the type of timestamp to get.\n
        module (str) : the module that is requesting the timestamp.\n

        Returns:\n
        timestamp (str) : the formatted timestamp.\n
        
        """

        timestamp = "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f"] [{type} - {module}]"

        return timestamp

