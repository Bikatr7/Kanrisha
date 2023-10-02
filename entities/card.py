## third-party libraries
import discord

##-------------------start-of-replica--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class replica:

    """
    
    Represents a gacha replica.\n

    """

    ##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    
    def __init__(self, inc_identifier:int) -> None:

        """

        Initializes the replica object.\n

        Parameters:\n
        inc_identifier (int) : replica identifier.\n

        Returns:\n
        None.\n
        
        """        

        self.id = inc_identifier

        self.emoji = ""

        self.determine_attributes()

##-------------------start-of-determine_attributes()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def determine_attributes(self) -> None:

        """

        Determines the replica's attributes based on its identifier.\n

        Parameters:\n
        self (object - replica) : replica object.\n

        Returns:\n
        None.\n

        """

        if(self.id == 0):
            self.emoji = "<:R0:1156440244489564181>"

        elif(self.id == 1):
            self.emoji = "<:R1:1156440260100767835>"

        elif(self.id == 2):
            self.emoji = "<:R2:1156440273166008412>"

        elif(self.id == 3):
            self.emoji = "<:R3:1156440286449373285>"

        elif(self.id == 4):
            self.emoji = "<:R4:1156440297451049030>"

        elif(self.id == 5):
            self.emoji = "<:R5:1156440308268146718>"

        else:
            self.emoji = "<:R6:1156440320880414760>"

##-------------------start-of-rarity--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class rarity:

    """
    
    Represents a gacha card's rarity.\n

    """

    ##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, inc_id:int, inc_xp:int) -> None:

        """
        
        Initializes the rarity object.\n

        Parameters:\n
        inc_identifier (int) : rarity identifier.\n

        Returns:\n
        None.\n

        """

        self.id = inc_id

        self.name = ""

        self.acronym = ""

        self.emoji = ""

        self.color = 0x000000

        self.likelihood = 0

        self.current_xp = inc_xp 

        self.max_xp = 0

        self.determine_attributes()

##-------------------start-of-determine_attributes()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def determine_attributes(self):

        """
        
        Determines the rarity's attributes based on its identifier.\n

        Parameters:\n
        self (object - rarity) : rarity object.\n

        Returns:\n
        None.\n
        
        """

        if(self.id == 1):
            self.name = "Standard"
            self.acronym = "S"
            self.likelihood = .55
            self.emoji ="<:Standard:1155897909380907181>"
            self.color = 0xB5D94D
            self.max_xp = 7

        elif(self.id == 2):
            self.name = "Notable"
            self.acronym = "N"
            self.likelihood = .30
            self.emoji = "<:Notable:1155897923243098112>"
            self.color = 0xE49D32
            self.max_xp = 4

        elif(self.id == 3):
            self.name = "Distinguished"
            self.acronym = "D"
            self.likelihood = .11
            self.emoji = "<:Distinguished:1155897936274792540>"
            self.color = 0xC1291D
            self.max_xp = 1

        elif(self.id == 4):
            self.name = "Prime"
            self.acronym = "P"
            self.likelihood = .03
            self.emoji = "<:Prime:1155897948455059536>"
            self.color = 0x000000
            self.max_xp = 1

        elif(self.id == 5):
            self.name = "Exclusive"
            self.acronym = "E"
            self.likelihood = .01
            self.emoji = "<:Exclusive:1155897960014553139>"
            self.color = 0x52196B
            self.max_xp = 1

##-------------------start-of-card--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class card:

    """
    
    Represents a gacha card.\n

    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, 
                inc_card_id:str,
                inc_name:str, 
                inc_rarity_identifier:int, 
                inc_picture_url:str,
                inc_picture_name:str,
                inc_picture_subtitle:str,
                inc_picture_description:str, 
                inc_person_id:int):

        """
        
        Initializes the card object.\n

        Parameters:\n
        inc_id_sequence (int) : id of the card.\n
        inc_name (str) : name of the card.\n
        inc_rarity_identifier (int) : rarity of the card.\n
        inc_picture_url (str) : url to the card's picture.\n
        inc_picture_name (str) : name of the card's picture.\n
        inc_picture_subtitle (str) : subtitle of the card's picture.\n
        inc_picture_description (str) : description of the card's picture.\n
        inc_person_id (int) : id of the person who the card represents.\n

        Returns:\n
        None.\n

        """


        ## id of the card
        self.id = inc_card_id

        ## name of the card
        self.name = inc_name

        ## rarity of the card
        self.rarity = rarity(inc_rarity_identifier, inc_xp=0)
        
        ## replica of the card
        self.replica = replica(inc_identifier=0)

        ## url to the card's picture
        self.picture_url = inc_picture_url

        ## name of the card's picture
        self.picture_name = inc_picture_name

        ## subtitle of the card's picture
        self.picture_subtitle = inc_picture_subtitle

        ## description of the card's picture
        self.picture_description = inc_picture_description

        ## id of the person who the card represents
        self.person_id = inc_person_id

##-------------------start-of-determine_attributes()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def determine_attributes(self):

        """
        
        Determines the card's attributes based on its identifier.\n

        Parameters:\n
        self (object - card) : card object.\n

        Returns:\n
        None.\n

        """

        self.rarity.determine_attributes()
        self.replica.determine_attributes()

##-------------------start-of-reset_card_identifiers()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def reset_card_identifiers(self):

        """
        
        Resets the card's attributes to default.\n

        Parameters:\n
        self (object - card) : card object.\n

        Returns:\n
        None.\n

        """

        self.replica.id = 0
        self.rarity.current_xp = 0

        await self.determine_attributes()

##-------------------start-of-reset_card_customization()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def reset_card_customization(self):

        """
        
        Resets the card's customization attributes to default.\n

        Parameters:\n
        self (object - card) : card object.\n

        Returns:\n
        None.\n

        """

        self.picture_name = "None"
        self.picture_subtitle = "None"
        self.picture_description = "None"

        self.picture_url = "None"