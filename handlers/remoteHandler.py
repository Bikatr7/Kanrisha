## built-in modules
from datetime import datetime

import os
import shutil
import time

## custom modules


from modules.toolkit import toolkit

from modules.fileEnsurer import fileEnsurer

from handlers.connectionHandler import connectionHandler

class remoteHandler():

    """
    
    The handler that handles all interactions with the remote storage.\n

    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, file_ensurer:fileEnsurer, toolkit:toolkit) -> None:

        """
        
        Initializes the remoteHandler class.\n

        Parameters:\n
        file_ensurer (object - fileEnsurer) : The fileEnsurer object.\n
        toolkit (object - toolkit) : The toolkit object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        self.fileEnsurer = file_ensurer

        self.toolkit = toolkit

        self.connection_handler = connectionHandler(self.fileEnsurer, self.toolkit)

        ##----------------------------------------------------------------dir----------------------------------------------------------------


        ##----------------------------------------------------------------paths----------------------------------------------------------------


        ##----------------------------------------------------------------variables----------------------------------------------------------------
        

        ##----------------------------------------------------------------functions----------------------------------------------------------------

        self.fileEnsurer.logger.log_action("Remote Handler has been created")
    

