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
                date text NOT NULL,
                userloc, 
                userfollow, 
                geo, 
                coords, 
                favcount, 
                repcount,
                sentval,
                confidence);
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
            date = all_data['created_at']
            userloc = all_data['user']['location']
            userfollow = all_data['user']['followers_count']
            
            geo = all_data['geo']
            coords = all_data['coordinates']
            favcount = all_data['favorite_count']
            repcount = all_data['reply_count']
            
            
            info = (self.count, tweet, date, userloc, userfollow, geo, coords, favcount, repcount)
            self.count += 1
            print(info)

            c.execute('''INSERT INTO tweets 
            (id, content, date, userloc, userfollow, geo, coords, favcount, repcount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', info)

            conn.commit()
            conn.close()
    
            return True

        except:
            return True
        
    def on_error(self, status):
        print(status)

    def on_status(self, status):
        print(status.text)
        print('rly?')

    



