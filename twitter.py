from tweepy import OAuthHandler, StreamListener, Stream, API
import time


class TweetStream(StreamListener):

    def on_data(self, raw_data):
        with open("tweets2.json",'a') as f:
            f.write(raw_data)
        print("exit")



    def on_error(self, status_code):
        print(status_code)

    def on_timeout(self):
        print("Max. timed out.")



class Twitter:
    def __init__(self):
        auth = OAuthHandler('79V1fZAlA71DLFXDDGCwXRYbE', 'CJRUQ76pt0t7oesinjL1EjPfePVy7RRC1faw2BOMqVIRz5Im6a')
        auth.set_access_token('1145664209205780481-UlEokY6asfJuzSoHeNom5dAA6SUnUc',
                              'bKfKVM8P21IMAlRVqzqEzkvxFO2vZTpDejWeqqV9c9feI')
        self.my_streamer = TweetStream()
        self.api = API(auth)
        self.streamer = Stream(auth,self.my_streamer)

    def start(self, track, show=False):
        self.streamer.filter(track=track)

    def stop(self):
        self.streamer.disconnect()


words = ["kaappaan","bandobast"]

def stream():
    global words
    t = Twitter()
    t.start(track=words)

def w():
    global words
    return words



if __name__ == '__main__':
    global words
    t = Twitter()
    t.start(track=words)




