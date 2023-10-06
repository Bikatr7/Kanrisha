## built-in libaries
import os
import typing
import asyncio

## third-party libraries
import aiofiles

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

        if(await self.async_isdir(directory_path) == False):

            await asyncio.to_thread(os.mkdir, directory_path)

            await self.logger.log_action("INFO", "fileHandler", directory_path + " was created due to lack of the directory")

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

        if(await self.async_exists(file_path) == False):

            async with aiofiles.open(file_path, "w+", encoding="utf-8") as file:
                await file.truncate()

            await self.logger.log_action("INFO", "fileHandler", file_path + " was created due to lack of the file")

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

        if(await self.async_exists(file_path) == False or await self.async_getsize(file_path) == 0):

            async with aiofiles.open(file_path, "w+", encoding="utf-8") as file:
                await file.write(content_to_write)

            await self.logger.log_action("INFO", "fileHandler", file_path + " was created due to lack of the file or the file was empty")

##--------------------start-of-write_sei_line()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def write_sei_line(self, sei_file_path:str, items_to_write:typing.List[typing.Any]) -> None:

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
        
        async with aiofiles.open(sei_file_path, mode='a+', encoding='utf-8') as file:
            await file.write(line + ",\n")

##-------------------start-of-edit_sei_file()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

        async with aiofiles.open(file_path, mode='r+', encoding='utf8') as f:
            lines = await f.readlines()

        line = lines[target_line - 1]
        items = line.split(",")

        items[column_number - 1] = value_to_replace_to

        new_line = ",".join(items)

        lines[target_line - 1] = new_line

        async with aiofiles.open(file_path, mode='w', encoding='utf8') as file:
            await file.writelines(lines)

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

        async with aiofiles.open(sei_file_path, "r", encoding="utf-8") as file:
            sei_file = await file.readlines()

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

        async with aiofiles.open(sei_file_path, "r", encoding="utf-8") as file:
            lines = await file.readlines()

        async with aiofiles.open(sei_file_path, "w", encoding="utf-8") as file:
            for i, line in enumerate(lines, 1):
                if i != target_line:
                    await file.write(line)

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

        async with aiofiles.open(file_path, 'r') as file:
            lines = await file.readlines()

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

        async with aiofiles.open(target_path, 'r') as file:
            lines = await file.readlines()

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
    
##--------------------start-of-async_isdir()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    async def async_isdir(self, path:str) -> bool:

        """

        Checks if the given path is a directory.\n

        Parameters:\n
        path (str) : the path to check.\n

        Returns:\n
        await loop.run_in_executor(None, os.path.isdir, path) (bool) : True if the given path is a directory, False if it is not.\n

        """

        loop = asyncio.get_event_loop()
        
        return await loop.run_in_executor(None, os.path.isdir, path)
    
##--------------------start-of-async_exists()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    async def async_exists(self, path:str) -> bool:

        """

        Checks if the given path exists.\n

        Parameters:\n
        path (str) : the path to check.\n

        Returns:\n
        await loop.run_in_executor(None, os.path.exists, path) (bool) : True if the given path exists, False if it does not.\n

        """

        loop = asyncio.get_event_loop()

        return await loop.run_in_executor(None, os.path.exists, path)

##--------------------start-of-async_getsize()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def async_getsize(self, path:str) -> int:

        """

        Gets the size of the given path.\n

        Parameters:\n
        path (str) : the path to check.\n

        Returns:\n
        await loop.run_in_executor(None, os.path.getsize, path) (int) : the size of the given path.\n

        """

        loop = asyncio.get_event_loop()

        return await loop.run_in_executor(None, os.path.getsize, path)