from datetime import datetime
import json
import tweepy
import DataManagement
from MinesweeperGame import MinesweeperGame

# Constants
BOT_NAME = 'minesweeper_bot'

# Read in the last update time from file
last_update = DataManagement.get_last_update_time()
print("LAST UPDATE: "+str(last_update))

saved_games = DataManagement.load_saved_games()

# Read in the JSON file that contains the API keys for Twitter
keys = json.loads(open('keys.json').read())

# Initialize Twitter API with keys from JSON file
auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth)


def is_int(string):
    try:
        return int(string)
    except ValueError:
        return False


def get_new_tweets():
    new_tweets = api.search(q='@minesweeper_bot', rpp=100, show_user=1, include_entities=1)
    new_tweets[:] = [x for x in new_tweets if tweet.created_at < last_update and x.user.screen_name != 'minesweeper_bot']
    return new_tweets

# Save new "last updated" time to save to file at end
new_update_time = datetime.now()

tweets = get_new_tweets()
for tweet in tweets:
    reply_mention = '@' + tweet.user.screen_name + ' '
    print(tweet.text.lower())
    if "new game" in tweet.text.lower():
        saved_games[tweet.user.id_str] = MinesweeperGame()
        saved_games[tweet.user.id_str].__init__()
        api.update_status(reply_mention + "New game started:\n" + saved_games[tweet.user.id_str].print_board(), in_reply_to_status_id=tweet.id)
    else:
        if tweet.user.id_str in saved_games:
            text = tweet.text.lower().split(' ')  # Get text of tweet and split on spaces
            # Get the first two numbers out of the tweet and use them as the matrix coordinates to click on
            coords = list()
            for i in range(0, text.__len__()):
                coord = is_int(text[i])
                if coord is not False:
                    coords.append(coord)
                if coords.__len__() == 2:
                    break
            if coords.__len__() >= 2:
                if not saved_games[tweet.user.id_str].click_tile(coords[0], coords[1]):
                    api.update_status(reply_mention + "Game over! Reply 'New game' to start a new game\n" + saved_games[tweet.user.id_str].print_board(), in_reply_to_status_id=tweet.id)
                    del saved_games[tweet.user.id_str]
                else:
                    api.update_status(reply_mention + '\n' + saved_games[tweet.user.id_str].print_board(), in_reply_to_status_id=tweet.id)
            elif coords.__len__() == 1:
                api.update_status(reply_mention + "I only found one number in your tweet. Reply with the X and Y coordinates of the tile you want to click on", in_reply_to_status_id=tweet.id)
            elif coords.__len__() == 0:
                api.update_status(reply_mention + "I didn't find any numbers in your tweet. Reply with the X and Y coordinates of the tile you want to click on", in_reply_to_status_id=tweet.id)
        else:
            api.update_status(reply_mention + "I don't have a saved game for you, say 'new game' to start a game", in_reply_to_status_id=tweet.id)
DataManagement.save_game_data(saved_games)
DataManagement.update_last_update_time(new_update_time)
