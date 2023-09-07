## built-in imports
from datetime import datetime

class logger:

    '''

    The logger class is used to log actions taken by Kudasai.\n
        
    '''

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, incoming_log_file_path:str):

        """
        
        Initializes a new logger object.\n

        Parameters:\n
        incoming_log_file_path (str) : The path to the log file.\n

        Returns:\n
        None.\n

        """

        self.log_file_path = incoming_log_file_path

        self.batch = ""

##--------------------start-of-log_barrier()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def log_barrier(self):

        """
        
        Logs a barrier.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        self.batch += "--------------------------------------------------------------\n"

##--------------------start-of-log_action()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def log_action(self, type, module, action:str):

        """
        
        Logs an action.\n

        Parameters:\n
        self (object - logger) : the logger object.\n
        action (str) : the action being logged.\n

        Returns:\n
        None.\n
 
        """

        entry = "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f"] [{type} - {module}] {action}"

        if(module != "connectionHandler"):
            print(entry)

        self.batch += entry + "\n"

##--------------------start-of-push_batch()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def push_batch(self):

        """
        
        Pushes all stored actions to the file.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n
        
        """

        with open(self.log_file_path, 'a+', encoding="utf-8") as file:
            file.write(self.batch)

        self.batch = ""

##--------------------start-of-clear_log_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def clear_log_file(self):

        """
        
        Clears the log file.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n
        
        """

        with open(self.log_file_path, 'w+', encoding="utf-8") as file:
            file.truncate(0)