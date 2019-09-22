from tweepy import OAuthHandler, StreamListener, Stream, API
import time


class TweetStream(StreamListener):
    def __init__(self, filename):
        super().__init__()
        self.filname = filename

    def on_data(self, raw_data):
        with open(self.filename,'a') as f:
            f.write(raw_data)
        print("exit")



    def on_error(self, status_code):
        print(status_code)

    def on_timeout(self):
        print("Max. timed out.")

words = []

class Twitter:
    def __init__(self, con_key, con_secret, key, secret, filename):
        auth = OAuthHandler(con_key, con_secret)
        auth.set_access_token(key,
                              secret)
        self.my_streamer = TweetStream()
        self.api = API(auth)
        self.streamer = Stream(auth,self.my_streamer)

    def start(self, track, show=False):
        global words
        words = track
        self.streamer.filter(track=track)

    def stop(self):
        self.streamer.disconnect()







