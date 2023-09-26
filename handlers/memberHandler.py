## build-in libraries
import typing

## third-party libraries
import discord

## custom modules
from handlers.connectionHandler import connectionHandler

from entities.syndicateMember import syndicateMember

from modules.fileEnsurer import fileEnsurer
from modules.toolkit import toolkit


class memberHandler:

    """
    
    Handles the syndicate members using the bot.\n

    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_file_ensurer:fileEnsurer, inc_toolkit:toolkit, connection_handler:connectionHandler) -> None:

        """

        Constructor for the memberHandler class.\n

        Parameters:\n
        inc_file_ensurer (object - fileEnsurer) : the fileEnsurer object.\n
        inc_toolkit (object - toolkit) : the toolkit object.\n
        connection_handler (object - connectionHandler) : the connectionHandler object.\n

        Returns:\n
        None.\n

        """

        self.file_ensurer = inc_file_ensurer
        self.toolkit = inc_toolkit
        self.connection_handler = connection_handler

        self.members: typing.List[syndicateMember] = [] 

##-------------------start-of-load_members_from_remote()---------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def load_members_from_remote(self) -> None:

        """

        Loads the members from the local db.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        self.members.clear()

        id_list, name_list, spin_scores_list, owned_card_ids, credits_list = await self.connection_handler.read_multi_column_query("select member_id, member_name, spin_scores, owned_card_ids, credits from members")

        for i in range(len(id_list)):

            spin_scores = spin_scores_list[i].strip("(").strip(")").split(",")

            spin_scores = (int(spin_scores[0]), int(spin_scores[1]), int(spin_scores[2]), int(spin_scores[3]), int(spin_scores[4]))

            owned_cards = [int(card_id) for card_id in owned_card_ids[i].strip("[").strip("]").split(",")] if owned_card_ids[i].strip("[").strip("]") != "" else []

            new_member = syndicateMember(int(id_list[i]), name_list[i], spin_scores, owned_cards, int(credits_list[i]))
            self.members.append(new_member)

        await self.file_ensurer.logger.log_action("INFO", "memberHandler", "Loaded members from remote.")

##-------------------start-of-load_members_from_local()---------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def load_members_from_local(self) -> None:

        """

        Loads the members from the members folder.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        self.members.clear()

        with open(self.file_ensurer.member_path, "r", encoding="utf-8") as file:

            for line in file:

                values = line.strip().split(',')

                spin_scores = tuple([int(score) for score in values[2].strip('"').split('.')[:5]]) 

                card_ids = [int(card_id) for card_id in values[3].strip('"').split('.')] if values[3].strip('"') != "" else []

                ## explicit type hinting to avoid pylance warning below
                spin_scores = (spin_scores[0], spin_scores[1], spin_scores[2], spin_scores[3], spin_scores[4])

                self.members.append(syndicateMember(int(values[0]), values[1], spin_scores, card_ids, int(values[4]))) 

        await self.file_ensurer.logger.log_action("INFO", "memberHandler", "Loaded members from local.") 
               
##-------------------start-of-add_new_member()---------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def add_new_member(self, inc_member_id:int, inc_member_name:str, inc_spin_scores:typing.Tuple[int,int,int,int,int],  inc_credits:int) -> None:

        """
        
        Adds a new member to the members list.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        score_string = f'"{inc_spin_scores[0]}.{inc_spin_scores[1]}.{inc_spin_scores[2]}.{inc_spin_scores[3]}.{inc_spin_scores[4]}"'

        card_id_string = ""

        member_details = [str(inc_member_id), inc_member_name, score_string, card_id_string, str(inc_credits)]

        await self.file_ensurer.file_handler.write_sei_line(self.file_ensurer.member_path, member_details)

        ## adds new member to current instance of bot
        new_member = syndicateMember(inc_member_id, inc_member_name, inc_spin_scores, [], inc_credits)

        ## logs action
        await self.file_ensurer.logger.log_action("INFO", "memberHandler", f"Added new member: {inc_member_name}.")

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

                spin_scores_list = list(member.spin_scores)
                spin_scores_list[spin_index] += spin_value_increase
                member.spin_scores = tuple(spin_scores_list) # type: ignore
                
                break

##-------------------start-of-get_syndicate_member()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def get_syndicate_member(self, interaction:discord.Interaction, member:discord.Member | discord.User | None = None) -> typing.Tuple[syndicateMember | None, int, str, bool]:

        """
        
        Gets the syndicate member object from the member id. Also returns the member id and image url. Also returns whether or not the request is for the user's own profile.\n

        Will grab syndicate object from {member} if provided, otherwise will grab from {interaction}.\n
        
        Parameters:\n
        interaction (object - discord.Interaction) : the interaction object.\n
        member (object - discord.Member | discord.User | None) : the member object.\n

        Returns:\n
        target_member (object - syndicateMember | None) : the syndicateMember object.\n
        target_member_id (int) : the member id.\n
        image_url (str) : the image url.\n
        is_self_request (bool) : whether or not the request is for the user's own profile.\n

        """

        target_member = None

        is_self_request = False

        ## if we're given a member object, use that
        if(member):

            target_member_id = member.id
            image_url = member.display_avatar.url
            
        ## otherwise, use the interaction object
        else:
            is_self_request = True
            target_member_id = interaction.user.id
            image_url = interaction.user.display_avatar.url

        for syndicate_member in self.members:
                
                if(target_member_id == syndicate_member.member_id):
                    target_member = syndicate_member

        return target_member, target_member_id, image_url, is_self_request