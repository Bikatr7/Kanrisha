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

        self.identifier = inc_identifier

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

        if(self.identifier == 0):
            self.emoji = "<:R0:1155908555149414443>"

        elif(self.identifier == 1):
            self.emoji = "<:R1:1155908575449845860>"

        elif(self.identifier == 2):
            self.emoji = "<:R2:1155910882086371438>"

        elif(self.identifier == 3):
            self.emoji = "<:R3:1155908594223558746>"

        elif(self.identifier == 4):
            self.emoji = "<:R4:1155908616927326229>"

        elif(self.identifier == 5):
            self.emoji = "<:R5:1155908632639180810>"

        else:
            self.emoji = "<:R6:1155908651555491950>"

##-------------------start-of-rarity--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class rarity:

    """
    
    Represents a gacha card's rarity.\n

    """

    ##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, inc_identifier:int, inc_xp:int) -> None:

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

        if(self.identifier == 1):
            self.name = "Standard"
            self.acronym = "S"
            self.likelihood = .55
            self.emoji ="<:Standard:1155897909380907181>"
            self.color = 0xB5D94D
            self.max_xp = 7

        elif(self.identifier == 2):
            self.name = "Notable"
            self.acronym = "N"
            self.likelihood = .30
            self.emoji = "<:Notable:1155897923243098112>"
            self.color = 0xE49D32
            self.max_xp = 4

        elif(self.identifier == 3):
            self.name = "Distinguished"
            self.acronym = "D"
            self.likelihood = .11
            self.emoji = "<:Distinguished:1155897936274792540>"
            self.color = 0xC1291D
            self.max_xp = 1

        elif(self.identifier == 4):
            self.name = "Prime"
            self.acronym = "P"
            self.likelihood = .03
            self.emoji = "<:Prime:1155897949807100416>"
            self.color = 0x000000
            self.max_xp = 1

        elif(self.identifier == 5):
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


    def __init__(self, inc_id_sequence:int, inc_name:str, inc_rarity_identifier:int, inc_picture_path:str, inc_picture_url:str, inc_person_id:int):

        """
        
        Initializes the card object.\n

        Parameters:\n
        inc_id_sequence (int) : id of the card.\n
        inc_name (str) : name of the card.\n
        inc_rarity_identifier (int) : rarity of the card.\n
        inc_picture_path (str) : path to the card's picture.\n
        inc_picture_url (str) : url to the card's picture.\n
        inc_person_id (int) : id of the person who the card represents.\n

        Returns:\n
        None.\n

        """

        ## id of the card, includes the actual_id, replica_identifier, and xp_identifier.
        self.id_sequence = inc_id_sequence

        ## actual id of the card. 4 digits.
        self.actual_id = int(str(inc_id_sequence)[0:4])

        ## name of the card
        self.name = inc_name

        ## rarity of the card
        self.rarity = rarity(inc_rarity_identifier, inc_xp=int(str(inc_id_sequence)[5]))
        
        ## replica of the card
        self.replica = replica(int(str(inc_id_sequence)[4]))

        ## path to the card's picture
        self.picture_path = inc_picture_path

        ## url to the card's picture
        self.picture_url = inc_picture_url

        ## id of the person who the card represents
        self.person_id = inc_person_id

##-------------------start-of-get_display_embed()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def get_display_embed(self):

        """
        
        Returns an embed to display the card.\n

        Parameters:\n
        self (object - card) : card object.\n

        Returns:\n
        embed (object - discord.Embed) : embed to display the card.\n

        """

        print(self.replica.identifier)

        await self.determine_attributes()

        print(self.replica.identifier)

        embed = discord.Embed(title= f"{self.rarity.emoji}{self.name} {self.replica.emoji} ({self.rarity.current_xp}/{self.rarity.max_xp})", description=f"{self.rarity.name}", color = self.rarity.color)
        embed.set_image(url = self.picture_url)

        return embed

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
