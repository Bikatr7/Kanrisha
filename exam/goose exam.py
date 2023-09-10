## built-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing

## third-party libraries
import discord

## custom libraries
if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from bot.Kanrisha import Kanrisha

##-------------------start-of-player---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class player:

    """
    
    The player class.

    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_user:discord.User | discord.Member, inc_role:str) -> None:

        """

        The constructor for the player class.\n

        Parameters:\n
        inc_user (object - discord.User): The user object.\n
        inc_role (str): The role of the player.\n

        Returns:\n
        None.\n

        """

        self.user = inc_user
        self.role = inc_role

        self.position: tuple[int, int] = (0, 5)  ## Assuming default starting position

##-------------------start-of-gooseExam--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class gooseExam:

    """
    
    The Goose Exam

    """


##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_kanrisha_client:Kanrisha) -> None:

        """

        The constructor for the Goose Exam.\n

        Parameters:\n
        inc_kanrisha_client (object - Kanrisha): The Kanrisha client object.

        Returns:\n
        None.\n
        
        """

        kanrisha_client = inc_kanrisha_client

        players :typing.List[player] = []

        roles = ["Duck", "Goose"]

        board_display = ''

        game_started = False

        BOARD_WIDTH = 8
        BOARD_HEIGHT = 6

        room_names: dict[tuple[int, int], str] = {
            (0, 0): "3-H",
            (1, 0): "3-I",
            (2, 0): "3-J",
            (3, 0): "3-K",
            (4, 0): "Art",
            (5, 0): "3-L",
            (6, 0): "3-M",
            (7, 0): "3-N",
            (0, 1): "3-A",
            (1, 1): "3-B",
            (2, 1): "3-C",
            (3, 1): "3-D",
            (4, 1): "3-E",
            (5, 1): "3-F",
            (6, 1): "3-G",
            (7, 1): "Music",
            (0, 2): "2-H",
            (1, 2): "2-I",
            (2, 2): "2-J",
            (3, 2): "Gym",
            (4, 2): "2-K",
            (5, 2): "2-L",
            (6, 2): "2-M",
            (7, 2): "2-N",
            (0, 3): "2-A",
            (1, 3): "2-B",
            (2, 3): "2-C",
            (3, 3): "2-D",
            (4, 3): "2-E",
            (5, 3): "Library",
            (6, 3): "2-F",
            (7, 3): "2-G",
            (0, 4): "1-H",
            (1, 4): "Science",
            (2, 4): "1-I",
            (3, 4): "1-J",
            (4, 4): "1-K",
            (5, 4): "1-L",
            (6, 4): "1-M",
            (7, 4): "1-N",
            (0, 5): "1-A",
            (1, 5): "1-B",
            (2, 5): "1-C",
            (3, 5): "Staff",
            (4, 5): "1-D",
            (5, 5): "1-E",
            (6, 5): "1-F",
            (7, 5): "1-G",
            }

##-------------------start-of-start()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="start", description="Start a new game.")
        async def start(interaction: discord.Interaction):

            """
            
            Starts a new game.\n

            Parameters:\n
            interaction (object - discord.Interaction): The interaction object.

            Returns:\n
            None.\n


            """

            ## admin check
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
                await interaction.response.send_message("You do not have permission to use this command.", delete_after=3.0, ephemeral=True)
                return

            players = []
            game_started = True

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "A new game has started!")

##-------------------start-of-join()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="join", description="Join the game.")
        async def join(interaction: discord.Interaction):

            """

            Joins the game.\n

            Parameters:\n
            interaction (object - discord.Interaction): The interaction object.

            Returns:\n
            None.\n

            """

            if(not any(p.user == interaction.user for p in players) and len(players) < 4 and game_started == True):

                new_player = player(interaction.user, "")
                players.append(new_player)
                
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"{interaction.user.mention} has joined the game!")

##-------------------start-of-assign()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="assign", description="Assign roles to the four players.")
        async def assign(interaction: discord.Interaction, player1: discord.Member, player2: discord.Member, player3: discord.Member, player4: discord.Member, player1_role: str, player2_role: str, player3_role: str, player4_role: str):

            """

            Assigns roles to the four players.\n

            Parameters:\n
            interaction (object - discord.Interaction): The interaction object.\n
            player1 (object - discord.Member): The first player.\n
            player2 (object - discord.Member): The second player.\n
            player3 (object - discord.Member): The third player.\n
            player4 (object - discord.Member): The fourth player.\n
            player1_role (str): The role of the first player.\n
            player2_role (str): The role of the second player.\n
            player3_role (str): The role of the third player.\n
            player4_role (str): The role of the fourth player.\n

            Returns:\n
            None.\n

            """

            ## admin check
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
                await interaction.response.send_message("You do not have permission to use this command.", delete_after=3.0, ephemeral=True)
                return


            ## check if the players are in the game
            if(player1 not in players or player2 not in players or player3 not in players or player4 not in players):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "One or more of the players are not in the game.")
                return
            
            ## check if the roles are valid
            if(player1_role not in roles or player2_role not in roles or player3_role not in roles or player4_role not in roles):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "One or more of the roles are invalid.")
                return
            
            ## assign the roles
            players[0].role = player1_role
            players[1].role = player2_role
            players[2].role = player3_role
            players[3].role = player4_role

##-------------------start-of-board()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="board", description="Display the game board.")
        async def board(interaction: discord.Interaction):

            """
            
            Displays the game board.\n

            Parameters:\n
            interaction (object - discord.Interaction): The interaction object.

            Returns:\n
            None.\n

            """

            board_display = ''

            for y in range(BOARD_HEIGHT):
                for x in range(BOARD_WIDTH):

                    player_here = next((p for p in players if p.position == (x, y)), None)

                    if(player_here):
                        board_display += f'[{player_here.user.display_name[0]}]'
                    else:
                        board_display += '[ ]'

                board_display += '\n'

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"```{board_display}```")

##-------------------start-of-move()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="move", description="Move to a specified room.")
        async def move(interaction: discord.Interaction, room_name: str):

            """

            Moves to a specified room.\n

            Parameters:\n
            interaction (object - discord.Interaction): The interaction object.\n
            room_name (str): The name of the room to move to.\n

            Returns:\n
            None.\n

            """

            author = interaction.user

            ## Ensure the player is in the game.
            current_player = next((p for p in players if p.user == author), None)
            if(not current_player):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not in the game!", is_ephemeral=True)
                return

            ## Search for the specified room name in the room_names dictionary.
            for position, name in room_names.items():
                if(name.lower() == room_name.lower()):
                    current_position = current_player.position
                    distance_x = abs(current_position[0] - position[0])
                    distance_y = abs(current_position[1] - position[1])

                    ## Check if the move is diagonal
                    if distance_x == 1 and distance_y == 1:
                        current_player.position = position

                    ## Check if the move is linear and within 3 positions
                    elif (distance_x == 0 and distance_y <= 3) or (distance_y == 0 and distance_x <= 3):
                        current_player.position = position

                    else:
                        await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"{author.mention}, you can't move more than 1 position diagonally or 3 positions linearly.", is_ephemeral=True)
                        return

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"{author.mention}, the room '{room_name}' does not exist or is not accessible.", is_ephemeral=True)
            
##-------------------start-of-position()-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="position", description="Get the current position of the player.")
        async def position(interaction: discord.Interaction):

            """
            
            Gets the current position of the player.\n

            Parameters:\n
            interaction (object - discord.Interaction): The interaction object.\n

            Returns:\n
            None.\n

            """

            author = interaction.user

            ## Ensure the player is in the game.
            current_player = next((p for p in players if p.user == author), None)
            if(not current_player):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not in the game!", is_ephemeral=True)
                return

            position = current_player.position
            room_name = room_names.get(position, 'Unknown room')

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"{author.mention}, you are currently in {room_name}.")