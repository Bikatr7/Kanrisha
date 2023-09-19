class card:

    """
    
    Represents a gacha card.\n

    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, inc_id:int, inc_name:str, inc_rarity:int, inc_picture_path:str):

        """
        
        Initializes the card object.\n

        Parameters:\n
        inc_id (int) : id of the card.\n
        inc_name (str) : name of the card.\n
        inc_rarity (int) : rarity of the card.\n
        inc_picture_path (str) : path to the card's picture.\n

        Returns:\n
        None.\n

        """

        ## id of the card
        self.id = inc_id

        ## name of the card
        self.name = inc_name

        ## rarity of the card
        self.rarity = inc_rarity

        ## path to the card's picture
        self.picture_path = inc_picture_path