## custom modules
from bot.Kanrisha import Kanrisha

##-------------------start-of-main()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

client = Kanrisha()

token = client.file_ensurer.get_token()

client.run(token=token)