## build-in libraries
import io
import aiohttp

## third party libraries
from PIL import Image, ImageDraw, ImageFont

import discord

## custom modules
from bot.Kanrisha import Kanrisha

from entities.card import card

class pilHandler():

    """
    
    Handles all image processing using PIL.\n

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, kanrisha_client:Kanrisha) -> None:

        """
        
        Initializes the remoteHandler class.\n

        Parameters:\n
        file_ensurer (object - fileEnsurer) : The fileEnsurer object.\n
        toolkit (object - toolkit) : The toolkit object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        self.kanrisha_client = kanrisha_client

        self.file_ensurer = kanrisha_client.file_ensurer

        self.toolkit = kanrisha_client.toolkit

##--------------------start-of-load_images()-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def load_images(self, card:card) -> list[Image.Image]:

        """

        Loads the images for the card.\n

        Parameters:\n
        self (object - pilHandler) : The pilHandler object.\n
        card (object - card) : The card object.\n

        Returns:\n
        images (list - Image.Image) : The images for the card.\n        
        
        """

        frame_image_dict = {
            "1": self.file_ensurer.standard_frame_path,
            "2": self.file_ensurer.notable_frame_path,
            "3": self.file_ensurer.distinguished_frame_path,
            "4": self.file_ensurer.prime_frame_path,
            "5": self.file_ensurer.exclusive_frame_path,
        }

        rarity_image_dict = {
            "1": self.file_ensurer.standard_rarity_path,
            "2": self.file_ensurer.notable_rarity_path,
            "3": self.file_ensurer.distinguished_rarity_path,
            "4": self.file_ensurer.prime_rarity_path,
            "5": self.file_ensurer.exclusive_rarity_path,
        }

        replica_image_dict = {
            "0": self.file_ensurer.R0_replica_path,
            "1": self.file_ensurer.R1_replica_path,
            "2": self.file_ensurer.R2_replica_path,
            "3": self.file_ensurer.R3_replica_path,
            "4": self.file_ensurer.R4_replica_path,
            "5": self.file_ensurer.R5_replica_path,      
        }

        ## get images given card attributes
        frame_path = frame_image_dict[str(card.rarity.identifier)]
        rarity_path = rarity_image_dict[str(card.rarity.identifier)]
        replica_path = replica_image_dict[str(card.replica.identifier)]

        ## get pfp given card person identifier
        user = await self.kanrisha_client.fetch_user(int(card.person_id))
        pfp_url = user.avatar.url ## type: ignore (We know it will find a user)

        ## load images
        frame_image = Image.open(frame_path).convert("RGBA")
        rarity_image = Image.open(rarity_path).convert("RGBA")
        replica_image = Image.open(replica_path).convert("RGBA")

        async with aiohttp.ClientSession() as session:
            async with session.get(pfp_url) as resp:
                pfp_data = await resp.read()

        pfp_image = Image.open(io.BytesIO(pfp_data)).convert("RGBA")

        pfp_image = Image.open(pfp_url).convert("RGBA")

        return [frame_image, rarity_image, replica_image, pfp_image]

##--------------------start-of-get_card_embed()-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def get_card_embed(self, card:card) -> discord.Embed:

        """
        
        Generates an embed for the card.\n

        Parameters:\n
        self (object - pilHandler) : The pilHandler object.\n
        card (object - card) : The card object.\n

        Returns:\n
        embed (object - discord.Embed) : The embed for the card.\n

        """