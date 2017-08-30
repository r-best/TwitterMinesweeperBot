from datetime import datetime
import re
import json
from json import JSONEncoder
from MinesweeperGame import MinesweeperGame


class GameEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MinesweeperGame):
            return {
                "height": str(obj.height),
                "width": str(obj.width),
                "board": obj.mines_to_string()
            }
        else:
            return JSONEncoder.default(self, obj)


def load_saved_games():
    with open("saved_games.json", "r+") as file:
        data = json.load(file)
    games = dict()
    for user, value in data.items():
        games[user] = MinesweeperGame()
        games[user].__init__(board_height=int(value["height"]), board_width=int(value["width"]), num_mines=-1)
        games[user].load_board(value['board'])
    return games


def save_game_data(saved_games):
    with open("saved_games.json", "w+") as file:
        json.dump(saved_games, file, cls=GameEncoder, indent=4)


def get_last_update_time():
    date_file = open('lastupdate.txt', 'r+')
    temp = re.split(' |-|:|\\.', date_file.readline())
    temp = [int(x) for x in temp]
    return datetime(temp[0], temp[1], temp[2], temp[3] + 4, temp[4], temp[5])


def update_last_update_time(new_update_time):
    date_file = open('lastupdate.txt', 'r+')
    date_file.seek(0)
    date_file.write(str(new_update_time))
    date_file.truncate()
    date_file.close()
