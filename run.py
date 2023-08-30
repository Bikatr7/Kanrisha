## custom modules
from bot.Kanrisha import Kanrisha

##-------------------start-of-main()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    client = Kanrisha()

    token = client.file_ensurer.get_token()

    client.run(token=token)

if __name__ == "__main__":
    main()