## custom modules
from modules.fileEnsurer import fileEnsurer
from modules.toolkit import toolkit

class localHandler:

    """
    
    Handles all interactions with local storage for the bot.\n
    
    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_file_ensurer:fileEnsurer, inc_toolkit:toolkit) -> None:

        """

        Constructor for the localHandler class.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        self.file_ensurer = inc_file_ensurer
        self.toolkit = inc_toolkit