## built-in libraries
import typing

## custom modules
from handlers.connectionHandler import connectionHandler

from entities.suit import suit

from modules.fileEnsurer import fileEnsurer
from modules.toolkit import toolkit

class suitHandler:

    """
    
    Handles suits using the bot.\n

    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_file_ensurer:fileEnsurer, inc_toolkit:toolkit, connection_handler:connectionHandler) -> None:

        """

        Constructor for the suitHandler class.\n

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

        self.suits: typing.List[suit] = []

##-------------------start-of-load_suits_from_remote()---------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def load_suits_from_remote(self) -> None:

        """

        Loads the suits from the local db.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        ## clear the suits list
        self.suits.clear()

        id_list, name_list, num_members_list, king_id_list, queen_id_list, jack_id_list = await self.connection_handler.read_multi_column_query("select suit_id, suit_name, number_of_members, king_id, queen_id, jack_id from suits")

        for i in range(len(id_list)):

            ## create the suit object
            new_suit = suit(int(id_list[i]), name_list[i], int(num_members_list[i]), int(king_id_list[i]), int(queen_id_list[i]), int(jack_id_list[i]))

            ## append the suit object to the suits list
            self.suits.append(new_suit)

        await self.file_ensurer.logger.log_action("INFO", "suitHandler", "Loaded suits from remote.")


##-------------------start-of-load_suits_from_local()----------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def load_suits_from_local(self) -> None:

        """
        
        Loads the suits from the members folder.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        ## clear the suits list
        self.suits.clear()

        with open(self.file_ensurer.suit_path, "r") as file:

            for line in file:

                values = line.split(",")

                new_suit_id = int(values[0])
                new_suit_name = values[1]
                new_suit_num_members = int(values[2])
                new_suit_king_id = int(values[3])
                new_suit_queen_id = int(values[4])
                new_suit_jack_id = int(values[5])

                new_suit = suit(new_suit_id, new_suit_name, new_suit_num_members, new_suit_king_id, new_suit_queen_id, new_suit_jack_id)

                self.suits.append(new_suit)

        await self.file_ensurer.logger.log_action("INFO", "suitHandler", "Loaded suits from local.")