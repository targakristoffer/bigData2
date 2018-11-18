import sqlite3
from NLPHelper.Basic_NLP_Tasks import Basic_NLP_Tasks, POS_Retriever, NER_Retriever

class ConnAssistant():

    

    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('tweets.db')
        self.Basic_NLP_Tasks = Basic_NLP_Tasks()

    def fetchContent(self):
   
        c = self.conn.cursor()

        content = {}
        cTwo = 0
        for row in c.execute("SELECT * FROM tweets"):
            cOne = 0
            content['tweet_' + str(cTwo)] = {}
            print(row)
            for item in row:        
                content['tweet_' + str(cTwo)]['item_' + str(cOne)] = str(item)
                cOne+=1
            print('----------------------------------------------')

            print(row)
            cTwo+=1

        self.conn.commit()
    
        return content

    def updateSentiment(self, content):

        c = self.conn.cursor()
        for key, val in content.items():
            strings = key.split('_')
            ids = int(strings[1])

            sent_val, conf = self.Basic_NLP_Tasks.find_sentiment(
                    self.Basic_NLP_Tasks.remove_stopwords(str(val['item_1'])))
            info = (sent_val, conf, ids)
            c.execute('''UPDATE tweets SET 
                sentval = ?, confidence = ? WHERE id = ?
                ''', info)

        self.conn.commit()


    def fetchLongtermCollection(self):
        c = self.conn.cursor()

        content = {}
        cTwo = 0
        for row in c.execute("SELECT * FROM tweets"):
            cOne = 0
            content['tweet_' + str(cTwo)] = {}
            print(row)
            for item in row:        
                content['tweet_' + str(cTwo)]['item_' + str(cOne)] = str(item)
                cOne+=1
            print('----------------------------------------------')

            print(row)
            cTwo+=1

        self.conn.commit()
    
        return content

    def saveToLongtermCollection(self, content):
        c = self.conn.cursor()

        c.execute('''

                ''')

        self.conn.commit()
    
    
    def deleteAllTweets(self):
        c = self.conn.cursor()

        c.execute('''
            DROP TABLE IF EXISTS tweets
                ''')

        self.conn.commit()



