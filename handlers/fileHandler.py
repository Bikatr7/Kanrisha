## built-in libaries
import os
import traceback
import typing

## custom modules
from modules.logger import logger

class fileHandler():

    """
    
    The handler that handles interactions with files.\n

    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, inc_logger:logger) -> None:

        """
        
        Initializes the fileHandler class.\n

        Parameters:\n
        logger (object - logger) : the logger object.\n

        Returns:\n
        None.\n

        """

        ##---------------------------------------------------------------------------------

        self.logger = inc_logger

##--------------------start-of-standard_create_directory()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def standard_create_directory(self, directory_path:str) -> None:

        """

        Creates a directory if it doesn't exist, as well as logs what was created.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        directory_path (str) : path to the directory to be created.\n

        Returns:\n
        None.\n

        """

        if(os.path.isdir(directory_path) == False):
            os.mkdir(directory_path)
            await self.logger.log_action(directory_path + " created due to lack of the folder")

##--------------------start-of-standard_create_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def standard_create_file(self, file_path:str) -> None:

        """

        Creates a file if it doesn't exist, truncates it,  as well as logs what was created.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        file_path (str) : path to the file to be created.\n

        Returns:\n
        None.\n

        """

        if(os.path.exists(file_path) == False):
            await self.logger.log_action(file_path + " was created due to lack of the file")
            with open(file_path, "w+", encoding="utf-8") as file:
                file.truncate()

##--------------------start-of-modified_create_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def modified_create_file(self, file_path:str, content_to_write:str) -> None:

        """

        Creates a path if it doesn't exist or if it is blank or empty, writes to it,  as well as logs what was created.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        file_path (str) : path to the file to be created.\n
        content to write (str) : content to be written to the file.\n

        Returns:\n
        None.\n

        """

        if(os.path.exists(file_path) == False or os.path.getsize(file_path) == 0):
            await self.logger.log_action(file_path + " was created due to lack of the file or because it is blank")
            with open(file_path, "w+", encoding="utf-8") as file:
                file.write(content_to_write)

##--------------------start-of-write_sei_line()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def write_sei_line(self, sei_file_path:str, items_to_write:typing.List[str]) -> None:

        """
        
        Writes the given items to the given sei file.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        sei_file_path (str) : the path to the sei file.\n
        items_to_write (list - str) : the items to be written to the sei file.\n

        Returns:\n
        None.\n

        """

        line = ",".join(str(item) for item in items_to_write)
        
        with open(sei_file_path, "a+", encoding="utf-8") as file:
            file.write(line + ",\n")

##-------------------start-of-read_sei_file()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def edit_sei_line(self, file_path:str, target_line:int, column_number:int, value_to_replace_to:str) -> None:
        
        """

        Edits the given line in the given file.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        file_path (str) : The file being edited.\n
        target_line (int) : The line number of the file we are editing.\n
        column_number (int) : The column number we are editing.\n
        value_to_replace_to (str) : The value to replace the edit value with.\n

        Returns:\n
        None.\n

        """

        with open(file_path, "r+", encoding="utf8") as f:
            lines = f.readlines()

        line = lines[target_line - 1]
        items = line.split(",")

        items[column_number - 1] = value_to_replace_to

        new_line = ",".join(items)

        lines[target_line - 1] = new_line

        with open(file_path, "w", encoding="utf8") as file:
            file.writelines(lines)

##-------------------start-of-read_sei_file()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def read_sei_file(self, sei_file_path:str, target_line:int, column:int) -> str:

        """

        Reads the given sei file and returns the value of the given column.\n
        
        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        sei_file_path (str) : the path to the sei file.\n
        target_line (int) : the line number of the sei file.\n
        column (int) : the column we are reading.\n

        Returns:\n
        file_details[column-1] : the value of the given column.\n

        """

        i,ii = 0,0
        build_string = ""
        file_details = []

        with open(sei_file_path, "r", encoding="utf-8") as file:
            sei_file = file.readlines()

        sei_line = sei_file[target_line - 1]

        count = sei_line.count(',')

        while(i < count):
            if(sei_line[ii] != ","):
                build_string += sei_line[ii]
            else:
                file_details.append(build_string)
                build_string = ""
                i+=1
            ii+=1
            
        return file_details[column-1]

##-------------------start-of-delete_sei_line()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def delete_sei_line(self, sei_file_path:str, target_line:int) -> None:

        """

        Deletes the specified line from the given sei file.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        sei_file_path (str) : the path to the sei file.\n
        target_line (int) : the line number to be deleted.\n

        Returns:\n
        None.\n

        """

        with open(sei_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(sei_file_path, "w", encoding="utf-8") as file:
            for i, line in enumerate(lines, 1):
                if i != target_line:
                    file.write(line)

##--------------------start-of-delete_all_occurrences_of_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def delete_all_occurrences_of_id(self, file_path:str, id_index:int, id_value:int) -> None:

        """
        
        Delete all lines that match a given id.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        file_path (str) : the path to the file to search.\n
        id_index (int) : the index of where the id should be.\n
        id_value (str) : the id to look for.\n

        Returns:\n
        None.\n

        """

        i = 0

        with open(file_path, 'r') as file:
            lines = file.readlines()

        line_count = len(lines)

        while(i < line_count):

            id = int(await self.read_sei_file(file_path, i + 1, id_index))

            if(id == id_value):
                await self.delete_sei_line(file_path, i + 1)
                line_count -= 1
                
            else:
                i += 1

            if(i >= line_count):
                break

##--------------------start-of-find_target_line()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def find_target_line(self, target_path:str, target_value:str, target_column:int) -> typing.Union[int , None]:

        """

        Finds the line number of the given value in the given column.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        target_path (str) : the path to the file to search.\n
        target_value (int) : the value to look for.\n
        target_column (int) : the column to look in.\n

        Returns:\n
        i + 1 (int) : the line number of the given value in the given column or None if value was not found.\n

        """

        i = 0

        with open(target_path, 'r') as file:
            lines = file.readlines()

        line_count = len(lines)

        while(i < line_count):
            result = await self.read_sei_file(target_path, i + 1, target_column)
            
            if(result == target_value):
                return i + 1
            else:
                i += 1

            if(i >= line_count):
                break

        return None

##--------------------start-of-get_new_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def get_new_id(self, id_list:typing.List[int]) -> int:

        """

        Generates a new id.\n 

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        id_list (list - ints) : a list of already active ids.\n

        Returns:\n
        new_id (int) : a new id.\n

        """

        id_list = [id for id in id_list]

        id_list.sort()

        new_id = 1

        for num in id_list:
            if(num < new_id):
                continue
            elif(num == new_id):
                new_id += 1
            else:
                return new_id
            
        return new_id
    
##-------------------start-of-handle_critical_exception()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def handle_critical_exception(self, critical_exception:Exception) -> None:

        """

        Handles a critical exception.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        critical_exception (Exception) : the exception that is critical.\n

        Returns:\n
        None.\n

        """

        ## if crash, catch and log, then throw
        await self.logger.log_action("--------------------------------------------------------------")
        await self.logger.log_action("Kanrisha has crashed")

        traceback_str = traceback.format_exc()
        
        await self.logger.log_action(traceback_str)

        await self.logger.push_batch()

        raise critical_exception