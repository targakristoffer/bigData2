import optparse

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except ImportError:
    import Tkinter as tk
    import ttk

from TwitterHelper.TwitterHelper import TwitterHelper


class Collector():
    def __init__(self):
        super().__init__()
        self.TwitterHelper = TwitterHelper()

    def initWindow(self, keyword, time):
        root = tk.Tk()
        root.minsize(width=150, height=150)
        root.maxsize(width=1000, height=1000)
        keys = [keyword, time]
        Window(root, keys).grid()
        root.mainloop()


    def startCollecting(self, keyword, time):
        print('[+]  Start col. function')
        self.TwitterHelper.get_tweet(keyword, time)


class Window(tk.Frame):
    ## INIT MAIN FRAME FUNCTION
    #
    def __init__(self, parent, keys, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self['highlightthickness'] = 2
        self.parent['highlightthickness'] = 2
        self.parent['relief'] = 'groove'

        mainFrame = tk.Frame(parent)
        mainFrame.grid()

        Label1 = ttk.Label(mainFrame, text='Checking for keyword[s]: ', font=("Times New Roman", 12))
        Label1.grid(row=1, column=1)
        keywordLabel = ttk.Label(mainFrame, text=keys[0], font=("Times New Roman", 12, "bold"))
        keywordLabel.grid(row=1, column=2)
        Label2 = ttk.Label(mainFrame, text='Collection time: ', font=("Times New Roman", 12))
        Label2.grid(row=2, column=1)
        timeLabel = ttk.Label(mainFrame, text=str(keys[1]), font=("Times New Roman", 12, "bold"))
        timeLabel.grid(row=2, column=2)
        
        

        





def main():

    Col = Collector()

    parser = optparse.OptionParser("usage%prog " + \
                                   "-K <target keywords> -t <target time>")
    parser.add_option('-K', dest='tgtKeyword', type='string', \
                      help='specify target keyword[s]')
    parser.add_option('-t', dest='tgtTimelimit', type='string', \
                      help='specify target collection time')
    (options, args) = parser.parse_args()
    tgtKeyword = str(options.tgtKeyword).split(', ')
    tgtTimelimit = int(options.tgtTimelimit)
    if(tgtKeyword[0] == None) | (tgtTimelimit == None):
        print('[-] You must specify variables to search by.')
        exit(0)
    print(tgtKeyword, tgtTimelimit)

    Col.startCollecting(tgtKeyword, tgtTimelimit)
    Col.initWindow(tgtKeyword, tgtTimelimit)



if __name__ == "__main__":
    main()