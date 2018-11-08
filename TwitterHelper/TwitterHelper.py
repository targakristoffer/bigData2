from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import sqlite3


import json


ckey="2AvbG84msbL34BEHslMsWZTUR"
csecret="gzEENqmZoMl2hhHvDIdaWzIF9ShMSLO0o7gh8csZnfqKdK6Y9H"
atoken="14113114-1we8sJQs1z54dWfjWbUwZtDtkQYf3kDOrXLUMBFkZ"
asecret="6Sq95ezVVRNTuLw7grKzm4czA32VqmlM0QwvaLjWLNl5A"




class TwitterHelper():

    def __init__(self):
        super().__init__()

        self.auth = OAuthHandler(ckey, csecret)
        self.auth.set_access_token(atoken, asecret)



    def get_tweet(self, keywords, amount): 
        conn = sqlite3.connect('tweets.db')
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS tweets (
                id integer PRIMARY KEY,
                content text NOT NULL,
                data,
                sentval text,
                confidence integer);
        ''')

        conn.commit()
        conn.close()

        numberOfLines = amount
        tweetConn = TwitterConn(numberOfLines)

        twitterStream = Stream(self.auth, tweetConn)
        twitterStream.filter(track=[keywords[0]], async=True)
    

    def file_len(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1



class TwitterConn(StreamListener):
    def __init__(self, numberOfLines):
        super().__init__()

 
        self.numberOfLines = numberOfLines
        self.count = 0
        
       

    def on_data(self, data):
        
        try:
 
            conn = sqlite3.connect('tweets.db')
            c = conn.cursor()
            all_data = json.loads(data)
            tweet = all_data["text"]

            
            print(tweet)
            info = (self.count, tweet)

            c.execute('''INSERT INTO tweets 
            (id, content) VALUES (?, ?)
            ''', info)

            conn.commit()
            conn.close()

            self.count += 1    
            return True

        except:
            return True
        
    def on_error(self, status):
        print(status)

    def on_status(self, status):
        print(status.text)
        print('rly?')

    



