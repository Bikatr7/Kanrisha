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

                spin_scores = tuple([int(score) for score in values[2].strip('"').split('.')[:3]])

                self.members.append(syndicateMember(int(values[0]), values[1], spin_scores, int(values[3])))

                self.file_ensurer.logger.log_action(f"Loaded member {values[0]}, {values[1]}, {spin_scores}, {values[4]}.")

##-------------------start-of-add_new_member()---------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def add_new_member(self, inc_member_id:int, inc_member_name:str, inc_spin_scores:typing.Tuple[int,int,int], inc_credits:int) -> None:

        """
        
        Adds a new member to the members list.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        ## member id, member_name

        score_string = f'"{inc_spin_scores[0]}.{inc_spin_scores[1]}.{inc_spin_scores[2]}"'

        member_details = [str(inc_member_id), inc_member_name, score_string, str(inc_credits)]

        await self.file_ensurer.file_handler.write_sei_line(self.file_ensurer.member_path, member_details)

        ## adds new member to current instance of bot
        new_member = syndicateMember(inc_member_id, inc_member_name, inc_spin_scores, inc_credits)

        self.members.append(new_member)


##-------------------start-of-update_spin_value()---------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def update_spin_value(self, target_member_id:int, spin_value_increase:int, spin_index:int) -> None:

        """

        Updates the spin value of a member.\n

        Parameters:\n
        target_member_id (int) : the id of the member to update.\n
        spin_value_increase (int) : the value to increase the spin value by.\n
        spin_index (int) : the index of the spin value to update.\n

        Returns:\n
        None.\n

        """

        ## update member in members list
        for member in self.members:

            if(member.member_id == target_member_id):

                tuple_string = f'"{member.spin_scores[0]}.{member.spin_scores[1]}.{member.spin_scores[2]}"'

                spin_scores_list = list(member.spin_scores)
                spin_scores_list[spin_index] += spin_value_increase
                member.spin_scores = tuple(spin_scores_list)
                
                break

        # Usage:
        target_line = await self.file_ensurer.file_handler.find_target_line(self.file_ensurer.member_path, str(target_member_id), 1)

        ## update member in file
        await self.file_ensurer.file_handler.edit_sei_line(self.file_ensurer.member_path, target_line, 3, tuple_string)  # type: ignore