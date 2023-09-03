## built-in modules
import asyncio

## custom modules
from bot.Kanrisha import Kanrisha

##-------------------start-of-main()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

async def main():

    client = Kanrisha()

    await client.file_ensurer.ensure_files()

    token = client.file_ensurer.get_token()

    host, user = client.file_ensurer.get_db_credentials()

    await client.remote_handler.connection_handler.ready_connection(host,user)

    client.run(token=token)

##---------------------------------/

asyncio.run(main())