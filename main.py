#!/usr/bin/python3
import os
from trello import TrelloClient
import trello

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
KEY_PATH = "{}/keys".format(BASE_DIR)

api_key = os.getenv("TRELLO_API_KEY")
api_secret = os.getenv("TRELLO_API_SECRET")

if api_key == None or api_secret == None or api_key == "" or api_secret == "":
    print("Error: please set api_key and api_secret in environment variables, TRELLO_API_KEY and TRELLO_API_SECRET")
    exit(1)

access_token = {}

if os.path.exists(KEY_PATH):
    with open(KEY_PATH, 'r') as f:
        access_token['oauth_token'], access_token['oauth_token_secret'] = f.read().split()
else:
    access_token = trello.util.create_oauth_token(key=api_key, secret=api_secret, output=False)
    with open(KEY_PATH, 'w') as f:
        f.write("{} {}\n".format(access_token['oauth_token'], access_token['oauth_token_secret']))

client = TrelloClient(
        api_key=api_key,
        api_secret=api_secret,
        token=access_token['oauth_token'],
        token_secret=access_token['oauth_token_secret']
        )


all_boards = client.list_boards()
main_board_list = list(filter(lambda x: x.name == 'Main', all_boards))

if len(main_board_list) != 1:
    print("No or multiple boards of named 'main'.")
    exit(1)

main_board = main_board_list[0]

lists = main_board.list_lists()

donethisweek_list = list(filter(lambda x: x.name == 'DoneThisWeek', lists))

if len(donethisweek_list) != 1:
    print("No or multiple boards of named 'DoneThisWeek'.")
    exit(1)

donethisweek_list = donethisweek_list[0]

log = ""

for card in donethisweek_list.list_cards():
    log += "[{}]({})\n".format(card.name, card.url)

with open("log.txt", "a") as f:
    from datetime import date
    today = date.today()
    f.write("{}\n".format(today.strftime("%d/%m/%Y")))
    f.write(log)
