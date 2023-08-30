## custom modules
from entities.syndicateMember import syndicateMember

from modules.fileEnsurer import fileEnsurer
from modules.toolkit import toolkit

class memberHandler:

    """
    
    Handles the syndicate members using the bot.\n

    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_file_ensurer:fileEnsurer, inc_toolkit:toolkit) -> None:

        """

        Constructor for the memberHandler class.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        self.file_ensurer = inc_file_ensurer
        self.toolkit = inc_toolkit

        self.members = []

##-------------------start-of-add_new_member()---------------------------------------------------------------------------------------------------------------------------------------------------------------

    def add_new_member(self, inc_member_id:int):

        """
        
        Adds a new member to the members list.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        member_details = [str(inc_member_id)]

        self.file_ensurer.file_handler.write_sei_line(self.file_ensurer.member_path, member_details)

        ## adds new member to current instance of bot
        new_member = syndicateMember(inc_member_id)

        self.members.append(new_member)