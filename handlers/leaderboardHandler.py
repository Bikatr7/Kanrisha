## built-in libraries
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing

## third party libraries
import discord

if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from bot.Kanrisha import Kanrisha

class leaderboardHandler:

    """

    This class is responsible for leaderboard assembly.\n

    """

##-------------------start-of-__init__()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_kanrisha_client:Kanrisha) -> None:

        """
        
        Initializes the slash command handler.\n

        Parameters:\n
        inc_kanrisha_client (object - Kanrisha) : the Kanrisha client object.\n

        Returns:\n
        None.\n

        """

        kanrisha_client = inc_kanrisha_client

##-------------------start-of-leaderboard()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        @kanrisha_client.tree.command(name="leaderboard", description="Sends the leaderboards.")
        async def leaderboard(interaction: discord.Interaction):

            """
            
            Sends the leaderboards.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            None.\n

            """

            if(not await kanrisha_client.check_if_registered(interaction)):
                return
            
            if(not await kanrisha_client.interaction_handler.whitelist_channel_check(interaction)):
                return
            
            await kanrisha_client.interaction_handler.defer_interaction(interaction, is_thinking=True)

            luck_leaderboard = await get_luck_leaderboard(interaction)

            balance_leaderboard = await get_balance_leaderboard(interaction)

            merit_leaderboard = await get_merit_leaderboard(interaction)

            await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, embed=luck_leaderboard)

            await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, embed=balance_leaderboard)

            await kanrisha_client.interaction_handler.send_followup_to_interaction(interaction, embed=merit_leaderboard)
            
##-------------------start-of-get_luck_leaderboard()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def get_luck_leaderboard(interaction: discord.Interaction) -> discord.Embed:

            """

            Gets the luck leaderboard.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            luck_leaderboard (object - discord.Embed) : the embed object.\n

            """

            ## Calculate scores for each member who has spun at least once and store them in a list with the member's name
            scores_with_members = []
            for member in kanrisha_client.remote_handler.member_handler.members:
                ## Skip admins
                if(member.member_id in kanrisha_client.interaction_handler.admin_user_ids):
                    continue

                total_spins = sum(member.spin_scores)
                if(total_spins > 0):
                    score = round((member.spin_scores[0] * 1.818 + member.spin_scores[1] * 3.333 + member.spin_scores[2] * 9.091 + member.spin_scores[3] * 33.333 + member.spin_scores[4] * 100) / total_spins, 3)
                    scores_with_members.append((score, member.member_name))

            ## Sort the list based on the scores in descending order and then take only the top 10
            scores_with_members.sort(key=lambda x: x[0], reverse=True)
            top_10_scores_with_members = scores_with_members[:10]

            ## Find the rank of the user calling the command if the user is not an admin
            user_rank = None
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
                for rank, (score, member_name) in enumerate(scores_with_members, 1):
                    if(member_name == interaction.user.name):
                        user_rank = rank
                        break

            ## Calculate rank for users who haven't spun yet
            no_spin_rank = len(scores_with_members) + 1

            ## Construct the leaderboard message
            leaderboard_message = ""
            for score, member_name in top_10_scores_with_members:
                leaderboard_message += f"**{member_name}** - {score}\n"

            luck_leaderboard = discord.Embed(title="Luck Leaderboard", description=leaderboard_message, color=0xC0C0C0)
            luck_leaderboard.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)

            annotation = "At the end of each month, top 5 users will receive a credit bonus based on their rank.\n"
            
            if(user_rank is not None):
                luck_leaderboard.set_footer(text=f"Your rank is #{user_rank}/{len(scores_with_members)}. {annotation}")
            elif(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):  # Check if the user is not an admin
                luck_leaderboard.set_footer(text=f"Your rank is #{no_spin_rank} (haven't spun yet). {annotation}")

            return luck_leaderboard
        
##-------------------start-of-get_balance_leaderboard()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def get_balance_leaderboard(interaction: discord.Interaction) -> discord.Embed:

            """
            
            Gets the balance leaderboard.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            balance_leaderboard (object - discord.Embed) : the embed object.\n

            """

            ## Sort the list based on the scores in descending order and then take only the non-admin members
            non_admin_members = [
                member for member in kanrisha_client.remote_handler.member_handler.members 
                if member.member_id not in kanrisha_client.interaction_handler.admin_user_ids
            ]
            
            ## Sort the non-admin members based on credits in descending order
            sorted_non_admin_members = sorted(non_admin_members, key=lambda x: x.credits, reverse=True)
            
            ## Take the top 10 members for the leaderboard
            top_10_members = sorted_non_admin_members[:10]
            
            ## Find the rank of the user calling the command if they are not an admin
            user_rank = None
            if interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids:
                for rank, member in enumerate(sorted_non_admin_members, 1):
                    if member.member_id == interaction.user.id:
                        user_rank = rank
                        break
            
            ## Construct the leaderboard message
            leaderboard_message = ""
            for member in top_10_members:
                leaderboard_message += f'**{member.member_name}** - {member.credits:,}\n'
            
            balance_leaderboard = discord.Embed(
                title="Balance Leaderboard",
                description=leaderboard_message,
                color=0xC0C0C0
            )
            balance_leaderboard.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)
            
            ## Only set the footer with rank if the user is not an admin
            if(user_rank is not None):
                balance_leaderboard.set_footer(text=f"Your rank is #{user_rank}.")
            
            return balance_leaderboard
        
##-------------------start-of-get_merit_leaderboard()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        async def get_merit_leaderboard(interaction: discord.Interaction) -> discord.Embed:

            """

            Gets the merit leaderboard.\n

            Parameters:\n
            interaction (object - discord.Interaction) : the interaction object.\n

            Returns:\n
            merit_leaderboard (object - discord.Embed) : the embed object.\n

            """

            ## get members that are not admins and have at least 1 merit point
            non_admin_members = [
                member for member in kanrisha_client.remote_handler.member_handler.members 
                if member.member_id not in kanrisha_client.interaction_handler.admin_user_ids and member.merit_points > 0
            ]

            ## sort the members based on merit points in descending order
            sorted_non_admin_members = sorted(non_admin_members, key=lambda x: x.merit_points, reverse=True)

            ## take the top 10 members for the leaderboard, or less if there are less than 10 members
            top_10_members = sorted_non_admin_members[:10]

            ## find the rank of the user calling the command if they are not an admin
            user_rank = None
            if(interaction.user.id not in kanrisha_client.interaction_handler.admin_user_ids):
                for rank, member in enumerate(sorted_non_admin_members, 1):
                    if(member.member_id == interaction.user.id):
                        user_rank = rank
                        break

            ## construct the leaderboard message
            leaderboard_message = ""
            for member in top_10_members:
                leaderboard_message += f"**{member.member_name}** - {member.merit_points}\n"

            merit_leaderboard = discord.Embed(title="Merit Leaderboard", description=leaderboard_message, color=0xC0C0C0)

            merit_leaderboard.set_thumbnail(url=kanrisha_client.file_ensurer.bot_thumbnail_url)

            ## only set the footer with rank if the user is not an admin
            if(user_rank is not None):
                merit_leaderboard.set_footer(text=f"Your rank is #{user_rank}.")
            
            return merit_leaderboard