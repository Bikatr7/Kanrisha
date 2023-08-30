## built-in modules
import os
import shutil

## custom modules
from handlers.fileHandler import fileHandler

from modules.logger import logger

class fileEnsurer:

   """
   
   The fileEnsurer class is used to ensure that the files needed to run the program are present and ready to be used.\n

   """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def __init__(self) -> None:

      """
      
      Initializes the fileEnsurer class.\n

      Parameters:\n
      None.\n

      Returns:\n
      None.\n

      """
   

      ##----------------------------------------------------------------dirs----------------------------------------------------------------

      self.script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

      if(os.name == 'nt'):  # Windows
         self.config_dir = os.path.join(os.environ['USERPROFILE'],"KanrishaConfig")
      else:  # Linux
         self.config_dir = os.path.join(os.path.expanduser("~"), "KanrishaConfig")

      self.bot_details_dir = os.path.join(self.config_dir, "bot details")
      self.members_dir = os.path.join(self.config_dir, "members")
      self.images_dir = os.path.join(self.config_dir, "images")

      self.bot_images_dir = os.path.join(self.images_dir, "bot images")

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## log file
      self.log_path = os.path.join(self.bot_details_dir, "debug log.txt")

      self.token_path = os.path.join(self.bot_details_dir, "token.txt")

      self.bot_thumbnail_path = os.path.join(self.bot_images_dir, "kanrisha thumbnail.png")
      self.bot_thumbnail_url = "https://cdn.discordapp.com/app-icons/1144166968979628072/7f4e6d14a104149d59624d5cc2897b94.png?size=256"

      ##----------------------------------------------------------------functions----------------------------------------------------------------

      ## makes config dir where log sits, if not already there

      try:
         os.mkdir(self.config_dir)
      except:
         pass

      ##----------------------------------------------------------------objects----------------------------------------------------------------

      ## logger for all actions taken by Seisen.\n
      self.logger = logger(self.log_path)

      self.logger.log_action("Initialization")
      self.logger.log_action("--------------------------------------------------------------")

      self.file_handler = fileHandler(self.logger)

##--------------------start-of-ensure_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   async def ensure_files(self) -> None:

      """

      This function ensures that the files needed to run the program are present and ready to be used.\n
      
      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object.\n

      Returns:\n
      None.\n
      
      """

      await self.create_needed_base_directories()
      await self.ensure_member_files()

##--------------------start-of-create_needed_base_directories()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   async def create_needed_base_directories(self) -> None:

      """
      
      Creates the needed base directories.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object.\n

      Returns:\n
      None.\n
      
      """

      await self.file_handler.standard_create_directory(self.bot_details_dir)
      await self.file_handler.standard_create_directory(self.members_dir)
      await self.file_handler.standard_create_directory(self.images_dir)

      await self.file_handler.standard_create_directory(self.bot_images_dir)


##--------------------start-of-ensure_bot_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   async def ensure_member_files(self) -> None:
       
      """
      
      Ensures that the member files are present and ready to be used.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object.\n

      Returns:\n
      None.\n
      
      """

      self.member_path = os.path.join(self.members_dir, "members.txt")

      await self.file_handler.standard_create_file(self.member_path)
       

               
##-------------------start-of-get_elapsed_time()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def get_token(self) -> str:

      """

      Gets the token from the token.txt file for Kanrisha.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object.\n

      Returns:\n
      token (str) : the token for Kanrisha.\n

      """
      
      token = ""

      try:
         with open(self.token_path, 'r', encoding='utf-8') as file: 
               token = file.read()

         assert token != "" and token != "token"

      except Exception as e: ## else try to get api key manually

         token = input("DO NOT DELETE YOUR COPY OF THE TOKEN\n\nPlease enter the token of 'The Gamemaster' : ")

         with open(self.token_path, 'w+', encoding='utf-8') as file: 
               file.write(token)
               
      finally:
            return token