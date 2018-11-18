try:
    import tkinter as tk
    import tkinter.ttk as ttk
except ImportError:
    import Tkinter as tk
    import ttk

import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
import numpy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS
from PIL import Image

class WordCloudComp():
    def __init__(self):
        super().__init__()
        

    def drawComp(self, parent, data):

        print(data)
        self.mask = numpy.array(Image.open('cloudy.png'))
        self.cloud = WordCloud(background_color="white", max_words=200, mask=self.mask, stopwords= set(STOPWORDS))

        self.fig = plt.figure(figsize = (4, 3), facecolor = None)
        self.axC = self.fig.add_subplot(111)
        
        self.cloud.generate(data)

        self.axC.imshow(self.cloud) 
        self.axC.axis('off')

        self.canvasBar = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvasBar.draw()
        self.canvasBar.get_tk_widget().grid()
        self.canvasBar._tkcanvas.grid()
   
       

    def changeComp(self, parent, data):
        print(data)
        self.axC.clear()
        self.canvasBar.get_tk_widget().destroy()

        self.cloud.generate(data)
                           
        self.axC.imshow(self.cloud) 
        self.axC.axis('off')


        self.canvasBar = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvasBar.draw()
        self.canvasBar.get_tk_widget().grid()
        self.canvasBar._tkcanvas.grid()
 
    
        