from bot.Kanrisha import Kanrisha

##-------------------start-of-main()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

client = Kanrisha()

token = client.toolkit.get_token()

client.run(token=token)