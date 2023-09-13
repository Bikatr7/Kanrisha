## built-in modules
import asyncio
import os

## third-party modules
import socket

## custom modules
from bot.Kanrisha import Kanrisha

##-------------------start-of-main()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():

    client = Kanrisha()

    client.toolkit.clear_console()

    os.system("title " + "Kanrisha")

    loop = asyncio.get_event_loop()

    loop.run_until_complete(client.file_ensurer.ensure_files())

    token = client.file_ensurer.get_token()

    host, user = client.file_ensurer.get_db_credentials()

    try:

        loop.run_until_complete(client.remote_handler.connection_handler.ready_connection(host,user))

    except:

        client.toolkit.clear_console()

        print("No Connection")

        client.toolkit.pause_console()

        exit()

    client.toolkit.clear_console()

    try:
        client.run(token=token)

    except socket.gaierror:
        
        loop.run_until_complete(client.file_ensurer.logger.log_action("ERROR", "Kanrisha", "Network Error, retrying."))

##---------------------------------/

main()