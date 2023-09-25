## third-party libraries
import discord

##-------------------start-of-rarity--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class rarity:

    """
    
    Represents a gacha card's rarity.\n

    """

    ##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, inc_identifier:int):

        """
        
        Initializes the rarity object.\n

        Parameters:\n
        inc_identifier (int) : rarity identifier.\n

        Returns:\n
        None.\n

        """

        self.identifier = inc_identifier

        self.name = ""

        self.acronym = ""

        self.emoji = ""

        self.color = ""

        self.likelihood = 0

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

        if(self.identifier == 1):
            self.name = "Standard"
            self.acronym = "S"
            self.likelihood = .55

        elif(self.identifier == 2):
            self.name = "Notable"
            self.acronym = "N"
            self.likelihood = .30

        elif(self.identifier == 3):
            self.name = "Distinguished"
            self.acronym = "D"
            self.likelihood = .12

        elif(self.identifier == 4):
            self.name = "Prime"
            self.acronym = "P"
            self.likelihood = .03

        elif(self.identifier == 5):
            self.name = "Exclusive"
            self.acronym = "E"
            self.likelihood = .00


##-------------------start-of-card--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class card:

    """
    
    Represents a gacha card.\n

    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, inc_id:int, inc_name:str, inc_rarity_identifier:int, inc_picture_path:str, inc_picture_url:str, inc_person_id:int):

        """
        
        Initializes the card object.\n

        Parameters:\n
        inc_id (int) : id of the card.\n
        inc_name (str) : name of the card.\n
        inc_rarity_identifier (int) : rarity of the card.\n
        inc_picture_path (str) : path to the card's picture.\n
        inc_picture_url (str) : url to the card's picture.\n
        inc_person_id (int) : id of the person who the card represents.\n

        Returns:\n
        None.\n

        """

        ## id of the card
        self.id = inc_id

        ## name of the card
        self.name = inc_name

        ## rarity of the card
        self.rarity = rarity(inc_rarity_identifier)

        ## path to the card's picture
        self.picture_path = inc_picture_path

        ## url to the card's picture
        self.picture_url = inc_picture_url

        ## id of the person who the card represents
        self.person_id = inc_person_id

##-------------------start-of-get_display_embed()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_display_embed(self):

        """
        
        Returns an embed to display the card.\n

        Parameters:\n
        self (object - card) : card object.\n

        Returns:\n
        embed (object - discord.Embed) : embed to display the card.\n

        """

        embed = discord.Embed(title= f"{self.name}", description=f"{self.rarity.name}", color = 0xC0C0C0)
        embed.set_image(url = self.picture_url)

        return embed