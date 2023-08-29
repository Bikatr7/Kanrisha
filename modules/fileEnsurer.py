## built-in modules
import os
import shutil

## custom modules
from modules.fileHandler import fileHandler

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


      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## log file
      self.log_path = os.path.join(self.bot_details_dir, "debug log.txt")

      self.token_path = os.path.join(self.bot_details_dir, "token.txt")

      ##----------------------------------------------------------------functions----------------------------------------------------------------

      ## makes config dir where log sits, if not already there

      try:
         os.mkdir(self.config_dir)
      except:
         pass

      ##----------------------------------------------------------------objects----------------------------------------------------------------

      ## logger for all actions taken by Seisen.\n
      self.logger = logger(self.log_path)

      self.logger.clear_log_file()

      self.logger.log_action("Initialization")
      self.logger.log_action("--------------------------------------------------------------")

      self.file_handler = fileHandler(self.logger)

##--------------------start-of-ensure_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_files(self) -> None:

      """

      This function ensures that the files needed to run the program are present and ready to be used.\n
      
      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object.\n

      Returns:\n
      None.\n
      
      """

      self.create_needed_base_directories()

##--------------------start-of-create_needed_base_directories()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def create_needed_base_directories(self) -> None:

      """
      
      Creates the needed base directories.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object.\n

      Returns:\n
      None.\n
      
      """

      self.file_handler.standard_create_directory(self.bot_details_dir)
      self.file_handler.standard_create_directory(self.members_dir)
               
