## built-in libraries
import typing

class syndicateMember:

    """
    
    Represents users of the Kanrisha bot.\n

    Name subject to change.\n

    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_member_id:int, inc_member_name:str, inc_spin_scores:typing.Tuple[int,int,int], inc_credits:int) -> None:

        """

        Initializes the syndicateMember object.\n

        Parameters:\n
        inc_member_id (int): The ID of the member.\n
        inc_member_name (str): The name of the member.\n
        inc_spin_scores (tuple): The spin scores of the member.\n
        inc_credits (int): The credits of the member.\n

        Returns:\n
        None.\n

        """

        self.member_id = inc_member_id
        self.credits = inc_credits

        self.member_name = inc_member_name

        self.spin_scores = inc_spin_scores