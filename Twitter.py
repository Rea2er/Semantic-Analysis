from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
import json
import csv

consumer_key = "Kse4B6UBA1crWPOP1xMh9qhp2"
consumer_secret = "JeTTKvOffKo94SGmVnCAGJGvBHOZGu033pc4KIMoFfyF6i3nd7"
token_key = "840229860098342913-YwhrqW0L8H35DJCAm9XVLbi1oN8oemr"
token_secret = "IPAgBPlkkudfKVvDlAoAgqxNAYFx4hcesIIxSWvjjvlt8"


class TwitterStreamer():
    """
    class for streaming and processing live tweets
    """
    def stream_tweets(self, filename, tag_list):
        # this handles Twitter authentication and the connection to the Twitter Streaming API
        listener = MyStreamListener(filename)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(token_key, token_secret)
        stream = Stream(auth, listener)
        stream.filter(track=tag_list)


class MyStreamListener(StreamListener):
    """
    this a basic listener class that just prints received tweets to stdout
    """
    def __init__(self, filename):
        self.filename = filename

    def on_data(self, raw_data):
        data = json.loads(raw_data)
        with open(self.filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # remove URL and/or any special characters.
            row = [self.clean_tweet(data['text'])]
            print(row)
            writer.writerow(row)

    def clean_tweet(self, tweet):
        #  remove any @user as well as any special character, white space
        return ' '.join(re.sub("(\w+://\S+)|([^0-9A-Za-z \t])|(@[A-Za-z0-9]+)", " ", tweet).split())


if __name__ == "__main__":

    tag_list = ["Canada", "University", "Dalhousie University", "Halifax", "Canada Education"]
    filename = "tweets.csv"

    twitter_stream = TwitterStreamer()
    tweets = twitter_stream.stream_tweets(filename, tag_list)
