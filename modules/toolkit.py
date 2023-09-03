## built-in modules
import os
import time

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

##-------------------start-of-linux_getch()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def linux_getch(self):

        """

        Get a single character from the user.

        Parameters:\n
        self (object - toolkit) : the toolkit object.\n

        Returns:\n
        ch (str) : the character the user entered.\n

        """

        if(os.name != 'nt'):

            import sys, tty, termios

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

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

##--------------------start-of-clear_stream()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def clear_stream(self) -> None: 

        """
        Clears the console stream.

        Parameters:
        self (object - toolkit) : The toolkit object.

        Returns:
        None.
        """

        if(os.name == 'nt'):  # Windows

            import msvcrt
            while msvcrt.kbhit():  # while a key is waiting to be read
                msvcrt.getch()  # read the next key and ignore it

        else: ## Linux
            import termios, fcntl, sys

            fd = sys.stdin.fileno()

            ## Get the current terminal attributes
            old_term = termios.tcgetattr(fd)
            new_attr = termios.tcgetattr(fd)
            new_attr[3] = new_attr[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSANOW, new_attr)

            ## Set the terminal to non-blocking mode
            old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)

            ## Clear the input buffer
            try:
                while True:
                    sys.stdin.read(1)
            except IOError:
                pass

            ## Restore the terminal settings and mode
            termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)

        time.sleep(0.1)

##--------------------start-of-user_confirm()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def user_confirm(self, prompt:str) -> str:

        """

        Prompts the user to confirm their input.\n

        Parameters:\n
        self (object - toolkit) : The toolkit object.\n
        prompt (str) : the prompt to be displayed to the user.\n

        Returns:\n
        user_input (str) : the user's input.\n

        """

        confirmation = "Just To Confirm You Selected "
        options = " (Press 1 To Confirm, 2 To Retry, z to skip, or q to quit)\n"
        output = ""
        user_input = ""
        
        entry_confirmed = False

        while(entry_confirmed == False):

            self.clear_console()
            
            self.clear_stream()
            
            user_input = input(prompt + options)
            
            if(user_input == "q"): ## if the user wants to quit do so
                exit(0)

            if(user_input == "z"): ## z is used to skip
                raise self.UserCancelError()

            self.clear_console()

            output = confirmation + user_input + options
            
            print(output)
            
            self.clear_stream()

            if(os.name == 'nt'): ## Windows

                import msvcrt

                key =  msvcrt.getch().decode()
            
            else:

                key = self.linux_getch()
            
            if(int(self.input_check(4, key, 2 , output)) == 1):
                    entry_confirmed = True

            else:

                self.clear_console()

                print(prompt)
        
        self.clear_console()

        return user_input
    
##--------------------start-of-input_check()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def input_check(self, input_type:int, user_input:str, number_of_choices:int, input_prompt_message:str) -> str:

        """

        Checks the user's input to make sure it is valid for the given input type.\n

        Parameters:\n
        self (object - toolkit) : The toolkit object.\n
        input_type (int) : the type of input we are checking.\n
        user_input (str) : the user's input.\n
        number_of_choices (int) : the number of choices the user has.\n
        input_prompt_message (str)  : the prompt to be displayed to the user.\n

        Returns:\n
        new_user_input (str) : the user's input.\n

        """

        new_user_input = str(user_input)
        input_issue_message = ""

        self.clear_console()

        while(True):

            if(user_input == 'q'):
                exit(0)

            elif(user_input == 'v' and input_type != 1):
                return new_user_input
            
            elif(input_type == 1 and (str(user_input).isdigit() == False or user_input == "0")):
                input_issue_message = "Invalid Input, please enter a valid number choice or 'q'\n"

            elif(input_type == 4 and (str(user_input).isdigit() == False or int(user_input) > number_of_choices or user_input == "0")):
                input_issue_message = "Invalid Input, please enter a valid number choice or 'q' or 'v'\n"

            elif(input_type == 5 and (str(user_input).isdigit() == False or int(user_input) > number_of_choices or user_input == "0")):
                input_issue_message = "Invalid Input, please enter a valid number choice or 'q' or 'v'\n"

            else:
                return new_user_input

            if(input_type == 5):
                print(input_issue_message + "\n")
                user_input = input(input_prompt_message)

            elif(input_type == 4 or input_type == 1):

                if(os.name == 'nt'): ## Windows

                    import msvcrt

                    key =  msvcrt.getch().decode()
                
                else:

                    key = self.linux_getch()

                print(input_issue_message + "\n" + input_prompt_message)
                user_input = str(key)

            self.clear_console()
            self.clear_stream()

            new_user_input = str(user_input)

##--------------------start-of-UserCancelError------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    class UserCancelError(Exception):

        """
        
        Is raised when a user cancel's an action\n

        """


##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


        def __init__(self):

            """
            
            Initializes a new UserCancelError Exception.\n

            Parameters:\n
            None.\n

            Returns:\n
            None.\n

            """

            self.message = "User Canceled."