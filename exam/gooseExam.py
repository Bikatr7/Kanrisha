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

        self.has_sprint_token = False

        self.partner = None

        self.position: tuple[int, int] = (0, 5)  ## Assuming default starting position

        self.has_moved = False

        self.is_hidden = False

##-------------------start-of-set_partner()--------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def set_partner(self, partner:player) -> None:

        """

        Sets the partner of the player.\n

        Parameters:\n
        partner (object - player): The partner of the player.\n

        Returns:\n
        None.\n

        """

        self.partner = partner

##-------------------start-of-gooseExam--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class gooseExam:

    """
    
    The Goose Exam.\n

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

        self.players:typing.List[player] = []

        roles = ["Duck", "Goose"]

        self.board_display = ''

        self.admin : discord.User | discord.Member

        self.game_started = False

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

            self.admin = interaction.user

            ## admin check
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
                await interaction.response.send_message("You do not have permission to use this command.", delete_after=3.0, ephemeral=True)
                return

            self.players = []
            self.game_started = True

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "A new game has started!")

##-------------------start-of-end()----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="end", description="End the current game.")
        async def end(interaction: discord.Interaction):

            """
            
            Ends the current game.\n

            Parameters:\n
            interaction (object - discord.Interaction): The interaction object.

            Returns:\n
            None.\n

            """

            ## admin check
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
                await interaction.response.send_message("You do not have permission to use this command.", delete_after=3.0, ephemeral=True)
                return
            
            self.game_started = False

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "The game has ended!")

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

            if(not any(p.user == interaction.user for p in self.players) and len(self.players) < 4 and self.game_started == True):

                new_player = player(interaction.user, "")
                self.players.append(new_player)
                
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"{interaction.user.mention} has joined the game!")

            elif(any(p.user == interaction.user for p in self.players)):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are already in the game!", is_ephemeral=True)

            elif(len(self.players) >= 4):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "The game is full!", is_ephemeral=True)

            elif(self.game_started == False):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "There is no game to join", is_ephemeral=True)

            else:
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "Something went wrong!", is_ephemeral=True)
##-------------------start-of-assign()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="assign", description="Assign roles to the four self.players. Make sure to mention the self.players in the correct order. (Duck, Goose, Duck, Goose)") 
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

            ## game started check
            if(self.game_started == False):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "There is no game to assign roles to.", is_ephemeral=True)
                return

            ## admin check
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
                await interaction.response.send_message("You do not have permission to use this command.", delete_after=3.0, ephemeral=True)
                return


            ## check if the self.players are in the game
            if(player1 not in self.players or player2 not in self.players or player3 not in self.players or player4 not in self.players):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "One or more of the players are not in the game.")
                return
            
            ## check if the roles are valid
            if(player1_role not in roles or player2_role not in roles or player3_role not in roles or player4_role not in roles):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "One or more of the roles are invalid.")
                return
            
            ## assign the roles
            self.players[0].role = player1_role
            self.players[1].role = player2_role
            self.players[2].role = player3_role
            self.players[3].role = player4_role

            ## set the partners
            self.players[0].set_partner(self.players[1])
            self.players[1].set_partner(self.players[0])
            self.players[2].set_partner(self.players[3])
            self.players[3].set_partner(self.players[2])

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

                    player_here = next((p for p in self.players if p.position == (x, y)), None)

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
            current_player = next((p for p in self.players if p.user == author), None)
            if(not current_player):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not in the game!", is_ephemeral=True)
                return
            
            ## Get maximum allowed move distance
            if(current_player.role.lower() == "duck"):

                if(current_player.has_sprint_token):
                    max_move_distance = 3
                else:
                    max_move_distance = 1

            elif(current_player.role.lower() == "goose"):
                max_move_distance = 3
            else:
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "Invalid role! Please contact admin", is_ephemeral=True)
                return

            ## Search for the specified room name in the room_names dictionary.
            for position, name in room_names.items():
                if(name.lower() == room_name.lower()):
                    current_position = current_player.position
                    distance_x = abs(current_position[0] - position[0])
                    distance_y = abs(current_position[1] - position[1])

                    ## Check if the move is linear and within the allowed distance
                    if(distance_x == 0 and distance_y <= max_move_distance) or (distance_y == 0 and distance_x <= max_move_distance):
                        current_player.position = position
                        if(current_player.role.lower() == "duck" and current_player.has_sprint_token):
                            current_player.has_sprint_token = False

                        # Check if all players have moved, if so, reset the has_moved variable for all players
                        if(check_if_all_players_have_moved()):
                            for player in self.players:
                                player.has_moved = False

                        ## Apply room effects
                        await apply_room_effects(current_player)

                        ## After Duck's or Goose's move, call the above function
                        if(is_duck_in_check(current_player, current_player.partner)):
                            await self.admin.send("The Duck is in check!")

                    else:
                        await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"{author.mention}, you can't move that far.", is_ephemeral=True)
                        return

     
            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"{author.mention}, the room '{room_name}' does not exist or is not accessible.", is_ephemeral=True)

##-------------------start-of-is_duck_in_check()---------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def is_duck_in_check(duck: player | None, goose: player | None) -> bool:

            """

            Checks if the Duck is in check.\n

            Parameters:\n
            duck (object - player): The Duck player object.\n

            Returns:\n
            bool: True if the Duck is in check, False otherwise.\n

            """

            if(not duck or not goose):
                await self.admin.send("Critical Error.. Please restart the game.")
                raise Exception("Critical Error.. Please restart the game.")

            dx, dy = duck.position
            gx, gy = goose.position

            ## If Duck's position is adjacent or same as Goose's position
            return abs(dx - gx) <= 1 and abs(dy - gy) <= 1
        
##-------------------start-of-apply_room_effects()-------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def apply_room_effects(player: player) -> None:
            
            """

            Applies the effects of the room the player is in.\n

            Parameters:\n
            player (object - player): The player object.\n

            Returns:\n
            None.\n

            """

            room = room_names.get(player.position)

            if(room == "Gym" and player.role.lower() == "duck"):
                player.has_sprint_token = True

            if(room == "Library" and player.role.lower() == "goose"):
                player.is_hidden = True

##-------------------start-of-force_round_end()---------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="force-round-end", description="Force the round to end.")
        async def force_round_end(interaction: discord.Interaction):

            """

            Forces the round to end.\n

            Parameters:\n
            None.\n

            Returns:\n
            None.\n

            """

            ## admin check
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
                await interaction.response.send_message("You do not have permission to use this command.", delete_after=3.0, ephemeral=True)
                return

            for player in self.players:
                player.has_moved = True

##-------------------start-of-check_if_all_players_have_moved()------------------------------------------------------------------------------------------------------------------------------------------------

        async def check_if_all_players_have_moved():

            """

            Checks if all players have moved.\n

            Parameters:\n
            None.\n

            Returns:\n
            None.\n

            """

            for player in self.players:
                if(player.has_moved == False):
                    return False

            return True

##-------------------start-of-set-duck-initial-position()-----------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="set-duck-initial-position", description="Sets your initial position as the Duck player.")
        async def set_duck_initial_position(interaction: discord.Interaction, floor_num: int, room: str):

            """

            Set the initial position of the Duck player.\n

            Parameters:\n
            interaction (object - discord.Interaction): The interaction object.\n
            floor_num (int): Floor number [1-3].\n
            room (str): Room label [A-N].\n

            Returns:\n
            None.\n

            """

            author = interaction.user
            current_player = next((p for p in self.players if p.user == author), None)

            if(not current_player or current_player.role.lower() != "duck"):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not a Duck or not in the game!", is_ephemeral=True)
                return

            position_key = (floor_num, room)
            for pos, name in room_names.items():
                if name == position_key:
                    current_player.position = pos
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"{author.mention}, you've chosen your starting position as {name}.")
                    return

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"{author.mention}, invalid starting position.", is_ephemeral=True)

##-------------------start-of-set-goose-initial-position()---------------------------------------------------------------------------------------------------------------------------------------------------- 

        @kanrisha_client.tree.command(name="set-goose-initial-position", description="Sets your initial position as the Goose player.")
        async def set_goose_initial_position(interaction: discord.Interaction, room: str):

            """

            Set the initial position of the Goose player.\n

            Parameters:\n
            interaction (object - discord.Interaction): The interaction object.\n
            room (str): Room label [A or G].\n

            Returns:\n
            None.\n

            """

            author = interaction.user
            current_player = next((p for p in self.players if p.user == author), None)

            if(not current_player or current_player.role.lower() != "goose"):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not a Goose or not in the game!", is_ephemeral=True)
                return

            if(room not in ["A", "G"]):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"{author.mention}, invalid starting position.", is_ephemeral=True)
                return

            position_key = (1, room)
            for pos, name in room_names.items():
                if name == position_key:
                    current_player.position = pos
                    await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"{author.mention}, you've chosen your starting position as {name}.")
                    return

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
            current_player = next((p for p in self.players if p.user == author), None)
            if(not current_player):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not in the game!", is_ephemeral=True)
                return

            position = current_player.position
            room_name = room_names.get(position, 'Unknown room')

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, f"{author.mention}, you are currently in {room_name}.")

##-------------------start-of-ask()----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="ask", description="Goose asks a question.")
        async def ask_question(interaction: discord.Interaction, question: str):

            """

            The Goose asks a question.\n

            Parameters:\n
            interaction (object - discord.Interaction): The interaction object.\n
            question (str): The question asked by the Goose.\n

            Returns:\n
            None.\n

            """

            author = interaction.user
            current_player = next((p for p in self.players if p.user == author), None)

            if(not current_player or current_player.role.lower() != "goose"):
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not a Goose or not in the game!", is_ephemeral=True)
                return

            ## Notify the Duck about the question
            duck = next((p for p in self.players if p.role.lower() == "duck"), None)
            if(duck):
                await duck.user.send(f"Goose asked: {question}. Please answer using /answer [your answer]. (YES OR NO ONLY)")

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "Your question has been sent to the Duck.")

##-------------------start-of-answer()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="answer", description="Duck answers the question.")
        async def answer_question(interaction: discord.Interaction, answer: str):

            """

            The Duck answers the question.\n

            Parameters:\n
            interaction (object - discord.Interaction): The interaction object.\n
            answer (str): The answer given by the Duck.\n

            Returns:\n
            None.\n

            """

            author = interaction.user
            current_player = next((p for p in self.players if p.user == author), None)

            if not current_player or current_player.role.lower() != "duck":
                await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "You are not a Duck or not in the game!", is_ephemeral=True)
                return

            ## Notify the Goose about the answer
            goose = next((p for p in self.players if p.role.lower() == "goose"), None)
        
            if(goose):
                await goose.user.send(f"Duck answered: {answer}.")

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, "Your answer has been sent to the Goose.")

##-------------------start-of-help_exam()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        @kanrisha_client.tree.command(name="help-exam", description="Sends the commands for the exam.")
        async def help_exam(interaction: discord.Interaction):

            """

            Sends the help message for the exam.\n

            Parameters:\n
            self (object - slashCommandHandler) : the slashCommandHandler object.\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            ## admin check
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):

                help_message = (
                    "**/start** - Starts a new game. (ADMIN)\n"
                    "**/end** - Ends the current game. (ADMIN)\n"
                    "**/join** - Joins the game.\n"
                    "**/assign** - Assigns roles to the four players. (ADMIN)\n"
                    "**/board** - Displays the game board.\n"
                    "**/move** - Moves to a specified room.\n"
                    "**/position** - Gets the current position of the player.\n"
                    "**/force-round-end** - Force the round to end. (ADMIN)\n"
                    "**/help-exam** - Sends the commands for the exam.\n"
                    "**/set-duck-initial-position** - Sets your initial position as the Duck player.\n"
                    "**/set-goose-initial-position** - Sets your initial position as the Goose player.\n"
                    "**/ask** - Goose asks a question.\n"
                    "**/answer** - Duck answers the question.\n"
                )
                

            else:
                    help_message = (

                        "**/join** - Joins the game.\n"
                        "**/board** - Displays the game board.\n"
                        "**/move** - Moves to a specified room.\n"
                        "**/position** - Gets the current position of the player.\n"
                        "**/help-exam** - Sends the commands for the exam.\n"
                        "**/set-duck-initial-position** - Sets your initial position as the Duck player.\n"
                        "**/set-goose-initial-position** - Sets your initial position as the Goose player.\n"
                        "**/ask** - Goose asks a question.\n"
                        "**/answer** - Duck answers the question.\n"
                    )

            embed = discord.Embed(title="Exam Help", description=help_message, color=0xC0C0C0)
            embed.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)

            await kanrisha_client.interaction_handler.send_response_no_filter_channel(interaction, embed=embed)