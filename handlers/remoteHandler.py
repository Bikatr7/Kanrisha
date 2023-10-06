## third party libraries
import aiofiles

## custom modules
from modules.toolkit import toolkit
from modules.fileEnsurer import fileEnsurer
from handlers.connectionHandler import connectionHandler

from handlers.gachaHandler import gachaHandler
from handlers.memberHandler import memberHandler
from handlers.suitHandler import suitHandler

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

        self.suit_handler = suitHandler(self.file_ensurer, self.toolkit, self.connection_handler)


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
        await self.suit_handler.load_suits_from_remote()

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
        await self.suit_handler.load_suits_from_local()

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

        delete_member_cards_query = """
        drop table if exists member_cards
        """

        delete_suits_query = """
        drop table if exists suits
        """

        ##----------------------------------------------------------------calls----------------------------------------------------------------

        ## drop member_cards and suits first because of foreign key constraints
        await self.connection_handler.execute_query(delete_member_cards_query)
        await self.connection_handler.execute_query(delete_suits_query)

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
            number_of_standard_spins int not null,
            number_of_notable_spins int not null,
            number_of_distinguished_spins int not null,
            number_of_prime_spins int not null,
            number_of_exclusive_spins int not null,
            number_of_ace_cards int not null,
            credits bigint not null,
            merit_points int not null,
            has_freebie bool not null,
            suit_id int not null
        )
        """

        create_cards_query = """
        create table if not exists cards (
            card_id varchar(256) primary key,
            card_name varchar(256) not null,
            card_rarity int not null,
            card_picture_url varchar(256),
            card_picture_name varchar(256),
            card_picture_subtitle varchar(256),
            card_picture_description varchar(256),
            person_id bigint not null
        )
        """

        create_member_cards_query = """
        create table if not exists member_cards (
            member_id bigint not null,
            card_id varchar(256) not null,
            card_replica_id int not null,
            card_xp_id int not null,
            primary key (member_id, card_id),
            foreign key (member_id) references members(member_id),
            foreign key (card_id) references cards(card_id)
        )
        """

        create_suits_query = """
        create table if not exists suits (
            suit_id int primary key,
            suit_name varchar(256) not null,
            number_of_members int not null,
            king_id bigint not null,
            queen_id bigint not null,
            jack_id bigint not null,
            foreign key (king_id) references members(member_id),
            foreign key (queen_id) references members(member_id),
            foreign key (jack_id) references members(member_id)
        )
        """

        ##----------------------------------------------------------------calls----------------------------------------------------------------

        await self.connection_handler.execute_query(create_members_query)
        await self.connection_handler.execute_query(create_cards_query)
        await self.connection_handler.execute_query(create_member_cards_query)
        await self.connection_handler.execute_query(create_suits_query)

##--------------------start-of-fill_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def fill_remote_storage(self) -> None:

        """
        
        Fills the remote storage with the local storage.\n

        Note that this will reset everything remotely stored on the connected database.\n

        As well as wipe local storage.\n
        
        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------clears----------------------------------------------------------------
        
        async def clear_members() -> None:

            async with aiofiles.open(self.file_ensurer.member_path, "w+") as member_file:
                await member_file.truncate(0)

        async def clear_cards() -> None:

            async with aiofiles.open(self.file_ensurer.card_path, "w+") as card_file:
                await card_file.truncate(0)

        async def clear_member_cards() -> None:

            async with aiofiles.open(self.file_ensurer.member_card_path, "w+") as member_card_file:
                await member_card_file.truncate(0)

        async def clear_suits() -> None:

            async with aiofiles.open(self.file_ensurer.suit_path, "w+") as suit_file:
                await suit_file.truncate(0)

        ##----------------------------------------------------------------members----------------------------------------------------------------

        async def fill_members() -> None:

            table_name = "members"

            for member in self.member_handler.members:

                ## member_id, number_of_standard_spins, number_of_notable_spins, number_of_distinguished_spins, number_of_prime_spins, number_of_exclusive_spins, number_of_ace_cards, credits, merit_points, has_freebie, suit_id
                new_id = member.member_id
                new_number_of_standard_spins = member.spin_scores[0]
                new_number_of_notable_spins = member.spin_scores[1]
                new_number_of_distinguished_spins = member.spin_scores[2]
                new_number_of_prime_spins = member.spin_scores[3]
                new_number_of_exclusive_spins = member.spin_scores[4]
                new_number_of_ace_cards = member.num_ace_cards
                new_credits = member.credits
                new_merit_points = member.merit_points
                new_has_freebie = int(member.has_freebie)
                new_suit_id = member.suit_id

                ## create a list of the member details
                member_details = [new_id, 
                                new_number_of_standard_spins, 
                                new_number_of_notable_spins, 
                                new_number_of_distinguished_spins, 
                                new_number_of_prime_spins, 
                                new_number_of_exclusive_spins, 
                                new_number_of_ace_cards, 
                                new_credits, 
                                new_merit_points, 
                                new_has_freebie, new_suit_id]

                table_name = "members"
                insert_dict = {
                    "member_id": new_id,
                    "number_of_standard_spins": new_number_of_standard_spins,
                    "number_of_notable_spins": new_number_of_notable_spins,
                    "number_of_distinguished_spins": new_number_of_distinguished_spins,
                    "number_of_prime_spins": new_number_of_prime_spins,
                    "number_of_exclusive_spins": new_number_of_exclusive_spins,
                    "number_of_ace_cards": new_number_of_ace_cards,
                    "credits": new_credits,
                    "merit_points": new_merit_points,
                    "has_freebie": new_has_freebie,
                    "suit_id": new_suit_id
                }

                await self.connection_handler.insert_into_table(table_name, insert_dict)

                await self.file_ensurer.file_handler.write_sei_line(self.file_ensurer.member_path, member_details)

        ##----------------------------------------------------------------cards----------------------------------------------------------------

        async def fill_cards() -> None:

            table_name = "cards"

            for card in self.gacha_handler.cards:

                ## card_id, card_name, card_rarity, card_picture_url, card_picture_name, card_picture_subtitle, card_picture_description, person_id
                new_id = card.id
                new_name = card.name
                new_rarity = card.rarity.id
                new_picture_url = card.picture_url
                new_picture_name = card.picture_name
                new_picture_subtitle = card.picture_subtitle
                new_picture_description = card.picture_description
                new_person_id = card.person_id

                card_details = [new_id, new_name, new_rarity, new_picture_url, new_picture_name, new_picture_subtitle, new_picture_description, new_person_id]

                ## escape single and double quotes as well as backslashes
                to_escape = [new_picture_name, new_picture_subtitle, new_picture_description]

                new_picture_name, new_picture_subtitle, new_picture_description = [
                    string.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
                    for string in to_escape
                ]

                # Update the insert_dict
                insert_dict = {
                    "card_id": new_id,
                    "card_name": new_name,
                    "card_rarity": new_rarity,
                    "card_picture_url": new_picture_url,
                    "card_picture_name": new_picture_name,
                    "card_picture_subtitle": new_picture_subtitle,
                    "card_picture_description": new_picture_description,
                    "person_id": new_person_id
                }
                
                await self.connection_handler.insert_into_table(table_name, insert_dict)

                await self.file_ensurer.file_handler.write_sei_line(self.file_ensurer.card_path, card_details)


        ##----------------------------------------------------------------member_cards----------------------------------------------------------------

        async def fill_member_cards() -> None:

            table_name = "member_cards"

            for member in self.member_handler.members:

                for id in member.owned_card_ids:

                    id_sequence = id

                    ## member_id, card_id, card_replica_id, card_xp_id
                    new_member_id = member.member_id
                    new_card_id = id_sequence[0:4]
                    new_replica_id = id_sequence[4]
                    new_xp_id = id_sequence[5]

                    member_card_details = [new_member_id, new_card_id, new_replica_id, new_xp_id]

                    insert_dict = {
                        "member_id" : new_member_id,
                        "card_id" : new_card_id,
                        "card_replica_id" : new_replica_id,
                        "card_xp_id" : new_xp_id

                    }

                    await self.connection_handler.insert_into_table(table_name, insert_dict)

                    await self.file_ensurer.file_handler.write_sei_line(self.file_ensurer.member_card_path, member_card_details)

        ##----------------------------------------------------------------suits----------------------------------------------------------------

        async def fill_suits() -> None:

            table_name = "suits"

            for suit in self.suit_handler.suits:

                ## suit_id, suit_name, number_of_members, king_id, queen_id, jack_id
                new_id = suit.suit_id
                new_name = suit.suit_name
                new_number_of_members = suit.number_of_members
                new_king_id = suit.king_id
                new_queen_id = suit.queen_id
                new_jack_id = suit.jack_id

                suit_details = [new_id, new_name, new_number_of_members, new_king_id, new_queen_id, new_jack_id]

                insert_dict = {
                    "suit_id" : new_id,
                    "suit_name" : new_name,
                    "number_of_members" : new_number_of_members,
                    "king_id" : new_king_id,
                    "queen_id" : new_queen_id,
                    "jack_id" : new_jack_id
                }

                await self.connection_handler.insert_into_table(table_name, insert_dict)

                await self.file_ensurer.file_handler.write_sei_line(self.file_ensurer.suit_path, suit_details)

        ##----------------------------------------------------------------calls----------------------------------------------------------------

        await clear_members()
        await clear_cards()
        await clear_member_cards()
        await clear_suits()

        await fill_members()
        await fill_cards()
        await fill_member_cards()
        await fill_suits()