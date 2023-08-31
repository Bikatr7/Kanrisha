## build-in libraries
import typing

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

        self.members: typing.List[syndicateMember] = [] 

##-------------------start-of-load_members()---------------------------------------------------------------------------------------------------------------------------------------------------------------

    def load_members(self) -> None:

        """

        Loads the members from the members folder.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        with open(self.file_ensurer.member_path, "r", encoding="utf-8") as file:

            for line in file:

                values = line.strip().split(',')

                spin_scores = tuple([int(score) for score in values[2].strip('"').split(',')[:3]])

                self.members.append(syndicateMember(int(values[0]), values[1], spin_scores))

                self.file_ensurer.logger.log_action(f"Loaded member {values[0]}, {values[1]}, {spin_scores}.")

##-------------------start-of-add_new_member()---------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def add_new_member(self, inc_member_id:int, inc_member_name:str, inc_spin_scores:typing.Tuple[int,int,int]) -> None:

        """
        
        Adds a new member to the members list.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        ## member id, member_name

        score_string = f'"{inc_spin_scores[0]},{inc_spin_scores[1]},{inc_spin_scores[2]}"'

        member_details = [str(inc_member_id), inc_member_name, score_string]

        await self.file_ensurer.file_handler.write_sei_line(self.file_ensurer.member_path, member_details)

        ## adds new member to current instance of bot
        new_member = syndicateMember(inc_member_id, inc_member_name, inc_spin_scores)

        self.members.append(new_member)

        