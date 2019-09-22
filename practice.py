import json
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from spacy.lang.en import stop_words
from spacy.lang.en import English
from collections import Counter
import re
from twitter import w
import numpy as np
import geocoder
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


class Practice:

    def __init__(self,file, fresh = False, add_handles = True, add_retweet = True):
        self.file = file
        self.add_retweet = add_retweet
        self.handles = add_handles
        with open(self.file, 'r') as f:
            data_ = f.readlines()
        data = [i for i in data_ if i.strip()]
        self.pointer = len(data) if fresh else 0
        self.w = w()
        self.n = 0
        self.dataframe = pd.DataFrame()
        self.flatten_tweets(data[self.pointer- 1 :])
        self.sia = SentimentIntensityAnalyzer()
        self.s = stop_words.STOP_WORDS
        self.nlp = English()
        self.cnt = Counter()


    def flatten_tweets(self, data):
        tweets = []
        #l = open("location.txt","a")
        for i in data:
            json_obj = json.loads(i)

            #json_obj['loc'] = self.locate(json_obj)
            #l.write(str(json_obj['loc'][0])+','+str(json_obj['loc'][1])) # writing locations to a file

            json_obj['extended_tweet-full_text'] = \
                json_obj['quoted_status-user-screen_name']= \
                json_obj['quoted_status-text']= \
                json_obj['retweeted_status-user-screen_name']= ""
            json_obj['user-screen_name'] = json_obj['user']['screen_name']
            if 'extended_tweet' in json_obj:
                json_obj['extended_tweet-full_text'] = json_obj['extended_tweet']['full_text']
            if 'quoted_status' in json_obj and self.add_retweet:
                json_obj['quoted_status-user-screen_name'] = json_obj['quoted_status']['user']['screen_name']
                json_obj['quoted_status-text'] = json_obj['quoted_status']['text']
            if 'retweeted_status' in json_obj and self.add_retweet:
                json_obj['retweeted_status-user-screen_name'] = json_obj['retweeted_status']['user']['screen_name']

            tweets.append(json_obj)
        df = pd.DataFrame(tweets)
        df['final_text'] = df['text'] + df['extended_tweet-full_text'] + df['quoted_status-text']
        df['created_at'] = pd.to_datetime(df['created_at'])
        df.set_index('created_at', inplace=True)
        self.dataframe = self.dataframe.append(df,sort=True)
        self.n += len(data)

    def reflat(self):
        with open(self.file, 'r') as f:
            data_ = f.readlines()
        data = [i for i in data_ if i.strip()]
        if len(data) > (self.pointer + self.n):
            data = data[(self.pointer + self.n):]
            self.flatten_tweets(data)

    def locate(self,x):
        #coordinates
        lat = None
        long = None
        places = None
        if x['coordinates'] is  None:
            #place
            if x['place'] is not None:
                vals = np.array(x['place']['bounding_box']['coordinates'])
                vals = vals.sum(axis=1) / 4
                long, lat = float(vals[0][0]), float(vals[0][1])
            elif x['user']['location'] is not None:
                #user->location
                d = x['user']['location']
                v = re.findall(r'[a-zA-Z\s]*',d)
                g = geocoder.osm(','.join(v))
                if g.json is not None:
                    lat, long = float(g.json['raw']['lat']), float(g.json['raw']['lon'])

        elif x['coordinates'] is not None:
            long, lat = float(x['coordinates'][0]), float(x['coordinates'][1])
        return (long, lat)


    def check_word(self, word):
        cont_col = self.dataframe['text'].str.contains(word, case=False)
        cont_col |= self.dataframe['extended_tweet-full_text'].str.contains(word, case=False)
        cont_col |= self.dataframe['quoted_status-text'].str.contains(word, case=False)
        return cont_col

    def finalize(self, args):
        dfs = []
        for i in args:
            self.dataframe[i] = self.check_word(i)
            dfs.append(self.dataframe[i].resample('1Min').mean())
        return dfs,args

    def top_words(self):
        total = 0
        self.cnt = Counter()
        for i in self.dataframe['final_text'].values:
            i = i.lower()
            i = i.encode('ascii','ignore').decode('ascii')
            # re.sub(r'[\s.\-!$%^&*()I]*', "", i)
            i = re.sub(r'^[\w]*',"",i)
            if not self.handles:
                i = re.sub(r'@[\w]*', "", i)
                i = re.sub(r'#[\w]*', "", i)
            doc = self.nlp(i)
            for j in doc:
                if j.text not in self.s and len(j.text) > 3 and j.text not in self.w:
                    self.cnt[j.text] += 1
        return self.cnt.most_common(10)

    def sentiments(self,words):
        self.sentiment_scores = []
        for i in words:
            tweets = self.check_word(i)
            self.scores = self.dataframe[tweets]['final_text'].apply(self.sia.polarity_scores)
            self.sentiment_scores.append(self.scores.apply(lambda x: x['compound']).resample('1Min').mean())
        return self.sentiment_scores

    def show_location(self):
        lons, lats = [], []
        """
        try:
            with open("location.txt") as f:
                data = f.readlines()
            for i in data:
                lons.append(float(i[0]))
                lats.append(float(i[1]))
        except FileNotFoundError:
            pass
        """

        l = open("location.txt", "a")
        with open(self.file, 'r') as f:
            data_ = f.readlines()
        data = [i for i in data_ if i.strip()]
        for i in data:
            json_obj = json.loads(i)
            x, y = self.locate(json_obj)
            if x is not None:
                lons.append(x)
                lats.append(y)
                l.write(str(x) + ',' + str(y) + '\n')  # writing locations to a file


        l.close()
        map = Basemap()
        map.drawcountries()
        map.drawstates()
        map.drawcoastlines()
        map.scatter(lons, lats, latlon=True, alpha=0.7)

        plt.show()

if __name__ == "__main__":
    pass