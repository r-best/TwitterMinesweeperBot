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


def load_done_tweets():
    # Read in the file of tweet IDs that have already been replied to
    # Used to avoid replying to the same tweet twice
    # Could probably be done in a better way but whatever
    with open('done_tweets.txt', 'r') as done_tweets_file:
        done_tweets = done_tweets_file.readlines()
    return [x.strip() for x in done_tweets]


def save_done_tweets(done_tweets):
    file_data = load_done_tweets()
    with open('done_tweets.txt', 'a+') as done_tweets_file:
        for tweet_id in done_tweets:
            if tweet_id not in file_data:
                done_tweets_file.write(str(tweet_id) + '\n')
