## build-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import io
import aiohttp
import os
import typing

## third party libraries
from PIL import Image, ImageDraw, ImageFont

import discord

## custom modules
if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
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

    async def load_images(self, card:card, user:discord.User) -> list[Image.Image]:

        """

        Loads the images for the card.\n

        Parameters:\n
        self (object - pilHandler) : The pilHandler object.\n
        card (object - card) : The card object.\n
        user (object - discord.User) : The user object.\n

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
        frame_path = frame_image_dict[str(card.rarity.id)]
        rarity_path = rarity_image_dict[str(card.rarity.id)]
        replica_path = replica_image_dict[str(card.replica.id)]

        ## load images
        frame_image = Image.open(frame_path).convert("RGBA")
        rarity_image = Image.open(rarity_path).convert("RGBA")
        replica_image = Image.open(replica_path).convert("RGBA")

        if(card.picture_url == "None"):

            ## get pfp given card person identifier
            pfp_url = user.avatar.url ## type: ignore (We know it will find a user)
                    
        else:
            ## load url as pfp
            pfp_url = card.picture_url

        ## async download pfp
        async with aiohttp.ClientSession() as session:
            async with session.get(pfp_url) as resp:
                if resp.status == 200:
                    pfp_data = await resp.read()
                    pfp_image = Image.open(io.BytesIO(pfp_data)).convert("RGBA")
                else:
                    raise Exception(f"Couldn't download profile image, status code: {resp.status}")

        ## resize replica and rarity icons
        replica_image = replica_image.resize((100, 100))
        rarity_image = rarity_image.resize((100, 100))

        return [frame_image, rarity_image, replica_image, pfp_image]

##--------------------start-of-get_built_frame()-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def get_built_frame(self, card:card, user:discord.User) -> Image.Image:

        """
        
        Generates an embed for the card.\n

        Parameters:\n
        self (object - pilHandler) : The pilHandler object.\n
        card (object - card) : The card object.\n
        user (object - discord.User) : The user object.\n

        Returns:\n
        frame (object - Image.Image) : The frame object.\n

        """

        frame, rarity, replica, pfp = await self.load_images(card, user=user)

        ## calculate aspect ratios
        frame_aspect_ratio = 418 / 304  ## Target area aspect ratio (Width / Height)
        photo_aspect_ratio = pfp.width / pfp.height  

        ## force pfp into frame sie
        if(frame_aspect_ratio < photo_aspect_ratio):
            ## Fit by height, width will overflow
            new_height = 304
            new_width = int(new_height * photo_aspect_ratio)
        else:
            ## Fit by width, height will overflow
            new_width = 418
            new_height = int(new_width / photo_aspect_ratio)

        pfp = pfp.resize((new_width, new_height))

        ## Crop overflow
        x_offset = (new_width - 418) // 2
        y_offset = (new_height - 304) // 2
        pfp = pfp.crop((x_offset, y_offset, x_offset + 418, y_offset + 304))

        ## Add the pfp to the card frame
        frame.paste(pfp, (14, 60), mask=pfp)

        ## Add Replica icon
        frame.paste(replica, (350, 285), mask=replica)

        ## Add rarity icon
        frame.paste(rarity, (-10, -10), mask=rarity)

        return frame
    
##--------------------start-of-add_text_to_frame()-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def add_text_to_frame(self, frame:Image.Image, card:card, user:discord.User) -> Image.Image:


        """
        
        Adds text to the frame.\n

        Parameters:\n
        self (object - pilHandler) : The pilHandler object.\n
        frame (object - Image.Image) : The frame object.\n
        card (object - card) : The card object.\n
        user (object - discord.User) : The user object.\n

        Returns:\n
        frame (object - Image.Image) : The frame object.\n

        """


        draw = ImageDraw.Draw(frame)

        name_font = ImageFont.truetype(self.file_ensurer.title_font_path, size=35)
        description_font = ImageFont.truetype(self.file_ensurer.subtitle_font_path, size=20)

        if(card.picture_name == "None"):
            title = user.name

        else:
            title = card.picture_name

        if(card.picture_subtitle == "None"):
            subtitle = ""
        else:
            subtitle = card.picture_subtitle

        if(card.picture_description == "None"):
            description = ""

        else:
            description = card.picture_description

        ## Add text
        draw.text((70, 15), title, fill="white", font=name_font)
        draw.text((13, 370), subtitle, fill="black", font=description_font)
        draw.text((13, 420), description, fill="white", font=description_font)

        return frame

##--------------------start-of-assemble_embed()-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def assemble_embed(self, card:card) -> typing.Tuple[discord.Embed,discord.File]:

        """

        Assembles an embed for the card.\n

        Parameters:\n
        self (object - pilHandler) : The pilHandler object.\n
        card (object - card) : The card object.\n

        Returns:\n
        embed (object - discord.Embed) : The embed object.\n
        file (object - discord.File) : The file object.\n
        
        """

        user = await self.kanrisha_client.fetch_user(int(card.person_id))

        frame = await self.get_built_frame(card,user)
        frame = await self.add_text_to_frame(frame, card, user)

        ## save image to byte stream
        byte_io = io.BytesIO()
        frame.save(byte_io, format='png')

        ## needs to sync attributes before displaying, because it's highly likely that the card was just modified.
        await card.determine_attributes()

        ## build embed
        embed = discord.Embed(title= f"{card.rarity.emoji}{card.name} {card.replica.emoji} ({card.rarity.current_xp}/{card.rarity.max_xp})", description=f"{card.rarity.name}", color = card.rarity.color)

        ## get image from byte stream
        byte_io.seek(0)
        file = discord.File(byte_io, filename=f"{card.id}{card.replica.id}{card.rarity.current_xp}.png")

        embed.set_image(url=f"attachment://{file.filename}")

        return embed, file