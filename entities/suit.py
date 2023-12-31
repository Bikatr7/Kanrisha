
class suit():

    """
    
    Represents card suits for the aibg game.\n

    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self,
                inc_suit_id:int,
                inc_suit_name:str,
                inc_number_of_members:int,
                inc_king_id:int,
                inc_queen_id:int,
                inc_jack_id:int) -> None:
        
        """

        Initializes the suit object.\n

        Parameters:\n
        inc_suit_id (int) : The ID of the suit.\n
        inc_suit_name (str) : The name of the suit.\n
        inc_number_of_members (int) : The number of members in the suit.\n
        inc_king_id (int) : The ID of the king of the suit.\n
        inc_queen_id (int) : The ID of the queen of the suit.\n
        inc_jack_id (int) : The ID of the jack of the suit.\n

        Returns:\n
        None.\n

        """

        ## the ID of the suit
        self.suit_id = int(inc_suit_id)

        ## the name of the suit
        self.suit_name = inc_suit_name

        ## the number of members in the suit
        self.number_of_members = int(inc_number_of_members)

        ## the ID of the king of the suit
        self.king_id = int(inc_king_id)

        ## the ID of the queen of the suit
        self.queen_id = int(inc_queen_id)

        ## the ID of the jack of the suit
        self.jack_id = int(inc_jack_id)

        ## the ID of the suit role
        self.suit_role_id = -1

        ##-------------------/

        if(self.suit_id == 1):
            self.suit_role_id = 1158281919553875978

        elif(self.suit_id == 2):
            self.suit_role_id = 1158282031181086732

        elif(self.suit_id == 3):
            self.suit_role_id = 1158282076366323802

        elif(self.suit_id == 4):
            self.suit_role_id = 1158281982405517322
