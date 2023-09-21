## built-in libraries
import typing

class syndicateMember:

    """
    
    Represents users of the Kanrisha bot.\n

    Name subject to change.\n

    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_member_id:int, inc_member_name:str, inc_spin_scores:typing.Tuple[int,int,int,int,int], inc_owned_card_ids:typing.List[int], inc_credits:int) -> None:

        """

        Initializes the syndicateMember object.\n

        Parameters:\n
        inc_member_id (int): The ID of the member.\n
        inc_member_name (str): The name of the member.\n
        inc_spin_scores (tuple): The spin scores of the member.\n
        inc_owned_card_ids (list - int): The IDs of the cards owned by the member.\n
        inc_credits (int): The credits of the member.\n

        Returns:\n
        None.\n

        """

        ## the ID of the member
        self.member_id = inc_member_id

        ## the discord username of the member
        self.member_name = inc_member_name

        ## the spin scores of the member, i.e., how many times the member has spun the wheel and the results of the spins
        self.spin_scores: typing.Tuple[int,int,int,int,int] = inc_spin_scores

        ## the IDs of the cards owned by the member
        self.owned_card_ids: typing.List[int] = inc_owned_card_ids

        ## the credits of the member
        self.credits = inc_credits