try:
    import tkinter as tk
    import tkinter.ttk as ttk
except ImportError:
    import Tkinter as tk
    import ttk

import os
import signal
import subprocess
import sqlite3
import json
import psutil

from GUI.LeftTextView import LeftTextView
from GUI.RightFrame import RightFrame
from GUI.MenuBar import MenuBar
from GUI.BasicButton import Button_run
from GUI.TweetButton import Button_tweet

from NLPHelper.Basic_NLP_Tasks import Basic_NLP_Tasks, POS_Retriever, NER_Retriever

from LODHelper.connectHelper import ConnectHelper
from LODHelper.QueryAssistant import QueryAssistant

### ALL NAVIGATION BAR RELATED BEEZZWAX
##
#


class GUI(tk.Frame):
    ## INIT MAIN FRAME FUNCTION
    #
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.ConnectHelper = ConnectHelper()
        self.Basic_NLP_Tasks = Basic_NLP_Tasks()
        
        self.parent = parent
        
        self.twitterCollection = {}
        self.textCollection = {}
        
        self['highlightthickness'] = 2
        self.parent['highlightthickness'] = 2
        self.parent['relief'] = 'groove'

        ### NAVBAR
        ##
        #
        def hello():
            print('Hello')
        MenuBar(parent, hello)


        ### HEADER FRAME
        ## CONTAINS:
        #
        headerFrame = tk.Frame(parent)
        headerFrame['highlightthickness'] = 2
        headerFrame['relief'] = 'groove'
        totaltxt = ttk.Label(headerFrame, text="EM TEXT EXPLORER", font=("Times", 20))
        totaltxt.pack()
        headerFrame.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)
        

        ### TABS AND MAIN CONTENT
        ##
        #
        mainFrame = tk.Frame(parent)
        mainFrame.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)
        tabController = ttk.Notebook(mainFrame)

        rawTab = ttk.Frame(tabController)
        tabController.add(rawTab, text="Raw Text Tab")
  
        tweetTab = ttk.Frame(tabController)
        tabController.add(tweetTab, text="Get Tweets Tab")
        
        FacebookTab = ttk.Frame(tabController)
        tabController.add(FacebookTab, text="Facebook Tab")

        tabController.pack(expand=1, fill='both', padx=5, pady=5)



        ############################### EVERYTHING BELOW IS IN RAW TEXT TAB ###############################
        ### TREEVIEW
        ##
        #
        rawTreeTab = tk.Frame(rawTab)
        path = "C:/Users/Y/Desktop/ny_styr/skeptics-texts/skeptics-texts"
        self.nodes = dict()
        frame = tk.Frame(rawTreeTab)
        self.tree = ttk.Treeview(frame, height=10)

        ttk.Style().configure("Treeview", background="#383838", foreground="#FFF")

        ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text="SELECT FILE", anchor='center')

        self.tree.pack(fill='x')       
        frame.pack(fill='x')  


        abspath = os.path.abspath(path)
        self.insert_node('', abspath, abspath)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)
        self.tree.bind('<Double-1>', self.OnDoubleClick)

        rawTreeTab['highlightthickness'] = 2
        rawTreeTab['relief'] = 'groove'
        rawTreeTab.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)



        rawLowerTab = tk.Frame(rawTab)
        ### LEFT VIEW
        ## 
        #
        lefttext = """
                TEXT DISPLAY
        """
        self.rawleftscreen = self.initLeftTextView(rawLowerTab, lefttext, 20, 52)


        ### RUN-BUTTONS FRAME 
        ## 
        #
        buttonFrame = tk.Frame(rawLowerTab)

        ## BUTTTON ONE
        self.POS = POS_Retriever()
        self.NER = NER_Retriever()
        firstLabel = ttk.Label(buttonFrame, text=" ", font=("Helvitca", 12))
        firstLabel.grid(row=0, column=0)
        def firstButton():
            results = {}
            content = self.rawleftscreen.getContent()
            results['TEXT'] = [content]
            results['POS'] = self.POS.find_POS(content)
            results['NER'] = self.NER.find_NER(content)
            self.textCollection = results
            self.loadRawTextLeft(results)
        btn_one_row = 1
        btn_one_column = 0
        Button_run(buttonFrame, 'LOAD TEXT', firstButton, btn_one_row, btn_one_column)

        ## BUTTTON TWO
        secondLabel = ttk.Label(buttonFrame, text=" ", font=("Helvitca", 12))
        secondLabel.grid(row=2, column=0)
        def secondButton():
            collection = self.textCollection
            
            sent_val, conf = self.Basic_NLP_Tasks.find_sentiment(collection['TEXT'][0])
            collection['S.VAL'] = [sent_val]
            collection['S.CONF'] = [conf]

            self.textCollection = collection
            self.loadRawTextLeft(collection)

        btn_two_row = 3
        btn_two_column = 0
        Button_run(buttonFrame, 'SENTIMENT', secondButton, btn_two_row, btn_two_column)

        ## BUTTON THREE
        self.QueryAssistant = QueryAssistant()
        thirdLabel = ttk.Label(buttonFrame, text=" ", font=("Helvitca", 12))
        thirdLabel.grid(row=4, column=0)
        def thirdButton():
            content = self.rawleftscreen.getContent()
            print(content)
            primary_subj, other_subj = self.QueryAssistant.test(content)
            for thing in primary_subj:
                print("[+]---------- QUERY SESS STARTED ---------[+]")
                self.ConnectHelper.send_get_query(thing)
                print('--'*15)
                self.ConnectHelper.send_ask_query(thing)
                print('--'*15)
                self.ConnectHelper.send_desc_query(thing)

        btn_three_row = 5
        btn_three_column = 0
        Button_run(buttonFrame, 'SOMETHING', thirdButton, btn_three_row, btn_three_column)

        ## BUTTON FOUR
        fourthLabel = ttk.Label(buttonFrame, text=" ", font=("Helvitca", 12))
        fourthLabel.grid(row=6, column=0)
        def fourthButton():
            content = self.textCollection
            print(content)
            data = [[4, 6, 3, 8, 9, 4, 2],[100, 200, 400, 100, 300, 800, 250]]
            try:
                self.rawrightscreen.changeScatter(data)
            except:
                print('[-] Error')

            try:
                self.rawrightscreen.changeBar(data)
            except:
                print('[-] Error')
            

        btn_fourth_row = 7
        btn_fourth_column = 0
        Button_run(buttonFrame, 'VISUALIZE', fourthButton, btn_fourth_row, btn_fourth_column)

        buttonFrame.grid(row=1, column=1)




        ### RAW RIGHT VIEW 
        ## 
        #

        self.rawrightscreen = self.initRightView(rawLowerTab)

        rawLowerTab['highlightthickness'] = 2
        rawLowerTab['relief'] = 'groove'
        rawLowerTab.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)

        ############################### EVERYTHING BELOW IS IN TWEET TAB ##################################
        ### TWEET TOP FRAME 
        ##  
        #
        tweetTopTab = tk.Frame(tweetTab)
        tweetTopTab['highlightthickness'] = 2
        tweetTopTab['relief'] = 'groove'

        tweetTopTab.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)
       

        tweetInfoLabel = ttk.Label(tweetTopTab, text="Get Tweets", font=("Helvitca", 16))
        tweetInfoLabel.grid(row=0, column=0)

        keywordLabel = ttk.Label(tweetTopTab, text="Keyword:", font=("Helvitca", 12))
        keywordLabel.grid(row=1, column=0)
        keywordEntry = tk.Entry(tweetTopTab)
        keywordEntry.grid(row=2, column=0)

        amountLabel = ttk.Label(tweetTopTab, text="Amount:", font=("Helvitca", 12))
        amountLabel.grid(row=3, column=0)
        amountEntry = tk.Entry(tweetTopTab)
        amountEntry.grid(row=4, column=0)

        def getTweetButton():
            print('[+] Get tweet button working...')
            print('-----'*20)
            a = keywordEntry.get()
            b = amountEntry.get()
            try:
                this = subprocess.Popen('python collector.py -K ' + a + ' -t ' + b, shell=True)
                print(this.pid)
                self.collectionPID = this.pid
            except:
                print('[-] error starting collector.')

        btn_getTweet_row = 5
        btn_getTweet_column = 0
        Button_tweet(tweetTopTab, 'COLLECT', getTweetButton, btn_getTweet_row, btn_getTweet_column)

        def killTweetButton():
            pid = int(self.collectionPID)
            print(pid)
            process = psutil.Process(pid)
            try:
                for proc in process.children(recursive=True):
                    proc.kill()
                process.kill()

            except:
                print('[-] error quiting collector.')

        btn_killTweet_row = 6
        btn_killTweet_column = 0
        Button_tweet(tweetTopTab, 'STOP', killTweetButton, btn_killTweet_row, btn_killTweet_column)

        def purgeTweetButton():
            print('Deleting all tweets in db')

        btn_purgeTweet_row = 7
        btn_purgeTweet_column = 0
        Button_tweet(tweetTopTab, 'DELETE', purgeTweetButton, btn_purgeTweet_row, btn_purgeTweet_column)



        tweetLowerTab = tk.Frame(tweetTab)
        tweetLowerTab['highlightthickness'] = 2
        tweetLowerTab['relief'] = 'groove'

        tweetLowerTab.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)
        ### TWEET LEFT TEXT VIEW
        ##  
        #
        self.tweetleftscreen = self.initLeftTextView(tweetLowerTab, lefttext, 21, 50)

        
        ### TWEET RUN-BUTTONS FRAME 
        ## 
        # 

        tweetButtonFrame = tk.Frame(tweetLowerTab)

        ##BUTTON ONE
        tweetFirstLabel = ttk.Label(tweetButtonFrame, text=" ", font=("Helvitca", 12))
        tweetFirstLabel.grid(row=0, column=0)
        def tweetFirstButton():
            
            
            content = self.fetchContent()
            
            self.twitterCollection = content
            self.loadTweetTextLeft(content)

        tweet_btn_one_row = 1
        tweet_btn_one_column = 0
        Button_run(tweetButtonFrame, 'LOAD TWEET', tweetFirstButton, tweet_btn_one_row, tweet_btn_one_column)

        ##BUTTON TWO
        tweetSecondLabel = ttk.Label(tweetButtonFrame, text=" ", font=("Helvitca", 12))
        tweetSecondLabel.grid(row=2, column=0)
        def tweetSecondButton():
            content = self.twitterCollection
            
            self.updateSentiment(content)

            self.twitterCollection = self.fetchContent()
            self.loadTweetTextLeft(self.twitterCollection)


        tweet_btn_two_row = 3
        tweet_btn_two_column = 0
        Button_run(tweetButtonFrame, 'SENTIMENT', tweetSecondButton, tweet_btn_two_row, tweet_btn_two_column)

        ## BUTTON THREE
        tweetThirdLabel = ttk.Label(tweetButtonFrame, text=" ", font=("Helvitca", 12))
        tweetThirdLabel.grid(row=4, column=0)
        def tweetThirdButton():
            content = self.tweetleftscreen.getContent()
            print(content)
            
        tweet_btn_three_row = 5
        tweet_btn_three_column = 0
        Button_run(tweetButtonFrame, 'SOMETHING', tweetThirdButton, tweet_btn_three_row, tweet_btn_three_column)

        ##BUTTON FOUR
        tweetFourthLabel = ttk.Label(tweetButtonFrame, text=" ", font=("Helvitca", 12))
        tweetFourthLabel.grid(row=6, column=0)
        def tweetFourthButton():
            content = self.twitterCollection
            print(content)
            data = [[90, 50, 70, 30, 10, 40, 20],[10, 20, 40, 10, 30, 80, 25]]
            try:
                self.tweetrightscreen.changeScatter(data)
            except:
                print('[-] Error')

            try:
                self.tweetrightscreen.changeBar(data)
            except:
                print('[-] Error')

        tweet_btn_fourth_row = 7
        tweet_btn_fourth_column = 0
        Button_run(tweetButtonFrame, 'VISUALIZE', tweetFourthButton, tweet_btn_fourth_row, tweet_btn_fourth_column)

        tweetButtonFrame.grid(row=1, column=1)




        ### TWEET RIGHT VIEW 
        ## 
        #

        self.tweetrightscreen = self.initRightView(tweetLowerTab)
        


###################################################################################################################
###################################################################################################################
#################################################FUNCTIONS#########################################################
###################################################################################################################
###################################################################################################################


    ##
    #
    def initLeftTextView(self, parent, text, height, width):
        
        lt = LeftTextView(parent, height, width)
        lt.packself()
        lt.fill(text)

        return lt

    
    def initRightView(self, parent):
        rt = RightFrame(parent)
        rt.packself()
        return rt

#########################################################################################################

    ##
    #
    def removeRawTextLeft(self):
        self.rawleftscreen.remove()

    ##for key, val in text.items():
    #   self.rawleftscreen.fill(key)
    #   if(len(val) >= 1):
    #      self.rawleftscreen.fill('\n\n')
    #      self.rawleftscreen.fill(val)
    #
    def loadRawTextLeft(self, text):
        self.removeRawTextLeft()
        if(isinstance(text, dict)):
            for key, val in text.items():
                if(isinstance(val, dict)):
                    for key, itemlist in val.items():
                        for thing in itemlist:
                            self.rawleftscreen.fill('   --> ' + str(thing) + '\n')
                elif(isinstance(val, list)):                        
                    for thing in val:
                        self.rawleftscreen.fill('    --> ' + str(thing) + '\n')
                        
                self.rawleftscreen.fill('\n[+] ' + str(key))            
        elif(isinstance(text, list)):
            for a in text:
                self.rawleftscreen.fill(str(a))
        else:
            self.rawleftscreen.fill(text)


    #####################################################################################################

    ##
    #
    def removeTweetTextLeft(self):
        self.tweetleftscreen.remove()

    ##
    #
    def loadTweetTextLeft(self, text):
        self.removeTweetTextLeft()
        print('----######----'*50)
        if(isinstance(text, dict)):
            for key, val in text.items():
                self.tweetleftscreen.fill('\n[+] ' + str(key) + '\n')
                self.tweetleftscreen.fill('')
                if(len(val) >= 1):
                    for item in val:
                        self.tweetleftscreen.fill('   --> ' + str(val[item]) + '\n')

        elif(isinstance(text, list)):
            for a in text:
                self.tweetleftscreen.fill(str(a))
        else:
            self.tweetleftscreen.fill('[+] HOUSTON WE HAVE AN ERROR SOMEWHERE')



    ###################################################################################################   

    ##
    #
    def insert_node(self, parent, text, abspath):
        node = self.tree.insert(parent, 'end', text=text, open=False)
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')
    
    ##
    #           
    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            for p in os.listdir(abspath):
                self.insert_node(node, p, os.path.join(abspath, p))

    ##
    #
    def OnDoubleClick(self, event):
        click = self.tree.selection()[0]
        #print('----> ' + self.tree.item(click, 'text'))
        fileToOpen = self.tree.item(click, 'text')     
        self.loadFile(fileToOpen)
    ##
    #
    def loadFile(self, fileToOpen):
        folder = "C:/Users/Y/Desktop/ny_styr/skeptics-texts/skeptics-texts"
        openThus = folder + '/' + fileToOpen
        file = open(openThus, 'r')

        currFile = file.readline()
        self.loadRawTextLeft(currFile)

    def fetchContent(self):
        conn = sqlite3.connect('tweets.db')
        c = conn.cursor()

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

        conn.commit()
        conn.close()
        return content

    def updateSentiment(self, content):
        conn = sqlite3.connect('tweets.db')
        c = conn.cursor()
        for key, val in content.items():
            strings = key.split('_')
            ids = int(strings[1])

            sent_val, conf = self.Basic_NLP_Tasks.find_sentiment(
                    self.Basic_NLP_Tasks.remove_stopwords(str(val['item_1'])))
            info = (sent_val, conf, ids)
            c.execute('''UPDATE tweets SET 
                sentval = ?, confidence = ? WHERE id = ?
                ''', info)

        conn.commit()
        conn.close()





## MAIN LOOP
# - Starts the software
# - Initiates GUI parent
if __name__ == "__main__":
    root = tk.Tk()
    GUI(root).grid()
    root.mainloop()