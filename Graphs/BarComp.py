try:
    import tkinter as tk
    import tkinter.ttk as ttk
except ImportError:
    import Tkinter as tk
    import ttk

import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

class BarComp():
    def __init__(self):
        super().__init__()

    def drawComp(self, parent, data):
        self.figBar = Figure(figsize=(4,3), dpi=100)
        self.axBar = self.figBar.add_subplot(111)

        ind = np.arange(len(data[0]))
        opacity = 0.4
        bar_width = 0.35
        #self.rects1 = self.axBar.bar(ind, data[0], align='center', alpha=0.5)


        self.rects1 = self.axBar.bar(ind, data[0], bar_width,
                alpha=opacity, align='center', color='b',
                label='Favorites')

        self.rects2 = self.axBar.bar(ind + bar_width, data[1], bar_width,
                alpha=opacity, align='center', color='r',
                label='Retweets')


        
        self.axBar.set_xlabel('Tweet')
        self.axBar.set_ylabel('Score')
        self.axBar.set_title('Scores by fav and retweet')

        self.canvasBar = FigureCanvasTkAgg(self.figBar, master=parent)
        self.canvasBar.draw()
        self.canvasBar.get_tk_widget().grid()
        self.canvasBar._tkcanvas.grid()
        self.figBar.tight_layout()
    
    def changeComp(self, parent, data):
        self.axBar.clear()
        
        ind = np.arange(len(data[0]))
        opacity = 0.4
        bar_width = 0.35

        self.rects1 = self.axBar.bar(ind, data[0], bar_width,
                alpha=opacity, align='center', color='b',
                label='Favorites')

        self.rects2 = self.axBar.bar(ind + bar_width, data[1], bar_width,
                alpha=opacity, align='center', color='r',
                label='Retweets')


        

        self.canvasBar.draw()

    

