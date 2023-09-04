## built-in modules
import asyncio

## custom modules
from bot.Kanrisha import Kanrisha

##-------------------start-of-main()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():

    client = Kanrisha()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(client.file_ensurer.ensure_files())

    token = client.file_ensurer.get_token()

    host, user = client.file_ensurer.get_db_credentials()

    loop.run_until_complete(client.remote_handler.connection_handler.ready_connection(host,user))

    client.run(token=token)

##---------------------------------/

main()