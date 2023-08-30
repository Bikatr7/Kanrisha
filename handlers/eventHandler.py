## built-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing

## third-party libraries
import discord

## custom libraries
if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from bot.Kanrisha import Kanrisha

class eventHandler:
    """
    
    Handles events, besides the interaction event.\n
    
    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_kanrisha_client:Kanrisha) -> None:

        """
        
        Initializes the slash command handler.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        kanrisha_client = inc_kanrisha_client

        ##-------------------handling messages--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.event
        async def on_message(message):
            print(f"{message.author}: {message.content}")