## built-in modules
import os

## custom modules
from modules.toolkit import toolkit
from modules.fileEnsurer import fileEnsurer
from handlers.connectionHandler import connectionHandler

from handlers.gachaHandler import gachaHandler
from handlers.memberHandler import memberHandler

class remoteHandler():

    """
    
    The handler that handles all interactions with the remote storage.\n

    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, file_ensurer:fileEnsurer, toolkit:toolkit) -> None:

        """
        
        Initializes the remoteHandler class.\n

        Parameters:\n
        file_ensurer (object - fileEnsurer) : The fileEnsurer object.\n
        toolkit (object - toolkit) : The toolkit object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        self.file_ensurer = file_ensurer

        self.toolkit = toolkit

        self.connection_handler = connectionHandler(self.file_ensurer, self.toolkit)

        self.member_handler = memberHandler(self.file_ensurer, self.toolkit, self.connection_handler)

        self.gacha_handler = gachaHandler(self.file_ensurer, self.toolkit, self.connection_handler)


        ##----------------------------------------------------------------dir----------------------------------------------------------------


        ##----------------------------------------------------------------paths----------------------------------------------------------------


        ##----------------------------------------------------------------variables----------------------------------------------------------------
        

        ##----------------------------------------------------------------functions---------------------------------------------------------------- 

##--------------------start-of-load_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def load_remote_storage(self) -> None:

        """
        
        Loads the need data from remote storage.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        await self.member_handler.load_members_from_remote()
        await self.gacha_handler.load_cards_from_remote()

##--------------------start-of-load_local_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def load_local_storage(self) -> None:

        """
        
        Loads the needed data from local storage.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """
        
        await self.member_handler.load_members_from_local()
        await self.gacha_handler.load_cards_from_local()

##--------------------start-of-reset_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def reset_remote_storage(self, is_forced:bool, forced_by:str | None = None) -> None:

        """
        
        Resets the remote storage with the local storage.\n
        Note that this will reset all the words remotely stored on the connected database.\n
        Use Carefully!\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        await self.delete_remote_storage()
        await self.create_remote_storage()
        await self.fill_remote_storage()

        if(is_forced):
            await self.file_ensurer.logger.log_action("INFO", "remoteHandler", f"Remote storage has been forcibly reset by {forced_by}.")

        else:
            await self.file_ensurer.logger.log_action("INFO", "remoteHandler", "Remote storage has been reset.")

##--------------------start-of-delete_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def delete_remote_storage(self) -> None:

        """
        
        Deletes the remote storage.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------members----------------------------------------------------------------

        delete_members_query = """
        drop table if exists members
        """

        delete_cards_query = """
        drop table if exists cards
        """

        ##----------------------------------------------------------------calls----------------------------------------------------------------

        await self.connection_handler.execute_query(delete_members_query)
        await self.connection_handler.execute_query(delete_cards_query)

##--------------------start-of-create_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def create_remote_storage(self) -> None:

        """
        
        Creates the tables for the remote storage.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------members----------------------------------------------------------------

        create_members_query = """
        create table if not exists members (
            member_id bigint primary key,
            member_name varchar(32) not null,
            spin_scores varchar(32) not null,
            owned_card_ids varchar(32) not null,
            credits int not null
        )
        """

        create_cards_query = """
        create table if not exists cards (
            card_id bigint primary key,
            card_name varchar(32) not null,
            card_rarity int not null,
            card_picture_path varchar(32) not null,
            card_picture_url varchar(32) not null
        )
        """

        ##----------------------------------------------------------------calls----------------------------------------------------------------

        await self.connection_handler.execute_query(create_members_query)
        await self.connection_handler.execute_query(create_cards_query)

##--------------------start-of-fill_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def fill_remote_storage(self) -> None:

        """
        
        Fills the remote storage with the local storage.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------clears----------------------------------------------------------------
        
        async def clear_members():
    
            with open(self.file_ensurer.member_path, "w+") as member_file:
                member_file.truncate(0)

        async def clear_cards():

            with open(self.file_ensurer.card_path, "w+") as card_file:
                card_file.truncate(0)

        ##----------------------------------------------------------------members----------------------------------------------------------------

        async def fill_members():

            table_name = "members"

            for member in self.member_handler.members:

                ## member_id, member_name, spin_scores, owned care_ids, credits
                new_id = member.member_id
                new_name = member.member_name
                new_spin_scores = member.spin_scores
                owned_card_ids = member.owned_card_ids
                new_credits = member.credits

                score_string = ""
                card_string = ""

                score_string = f'"{new_spin_scores[0]}.{new_spin_scores[1]}.{new_spin_scores[2]}"'

                for card_id in owned_card_ids:
                    card_string += f'"{card_id}."'

                card_string = card_string[:-1]

                member_details = [str(new_id), new_name, score_string, card_string, str(new_credits)]

                table_name = "members"
                insert_dict = {
                    "member_id" : new_id,
                    "member_name" : new_name,
                    "spin_scores" : new_spin_scores,
                    "owned_card_ids" : owned_card_ids,
                    "credits" : new_credits
                }

                await self.connection_handler.insert_into_table(table_name, insert_dict)

                await self.file_ensurer.file_handler.write_sei_line(self.file_ensurer.member_path, member_details)

        ##----------------------------------------------------------------cards----------------------------------------------------------------

        async def fill_cards():

            table_name = "cards"

            for card in self.gacha_handler.cards:

                ## card_id, card_name, card_rarity, card_picture_path, card_picture_url
                new_id = card.id
                new_name = card.name
                new_rarity = card.rarity.identifier
                new_picture_path = os.path.basename(card.picture_path)
                new_picture_url = card.picture_url

                card_details = [str(new_id), new_name, str(new_rarity), new_picture_path, new_picture_url]

                insert_dict = {
                    "card_id" : new_id,
                    "card_name" : new_name,
                    "card_rarity" : new_rarity,
                    "card_picture_path" : new_picture_path,
                    "card_picture_url" : new_picture_url
                }

                await self.connection_handler.insert_into_table(table_name, insert_dict)

                await self.file_ensurer.file_handler.write_sei_line(self.file_ensurer.card_path, card_details)

        ##----------------------------------------------------------------calls----------------------------------------------------------------

        await clear_members()
        await clear_cards()

        await fill_members()
        await fill_cards()