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

from Graphs.BarComp import BarComp
from Graphs.ScatterComp import ScatterComp

class RightFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        


        tabController = ttk.Notebook(parent)
        self.ScatterTab = ttk.Frame(tabController)
        tabController.add(self.ScatterTab, text="Scatter")
  
        self.UnknownTab = ttk.Frame(tabController)
        tabController.add(self.UnknownTab, text="Unknown")
        
        self.BarTab = ttk.Frame(tabController)
        tabController.add(self.BarTab, text="Bar")

        tabController.grid(row=1, column=2)


        ## DATA
        data = [[10, 2, 20, 40, 30, 70, 25],[6, 9, 2, 3, 5, 7, 8]]
      
        close = 2
        volume = 3
        self.scatterChart = ScatterComp()
        self.barChart = BarComp()

        self.scatterChart.drawComp(self.ScatterTab, data, close, volume)
        self.barChart.drawComp(self.BarTab, data)


    def packself(self):
        self.grid(row=1, column=2)

    def changeBar(self, data):
        self.barChart.changeComp(self.BarTab, data)
    
    def changeScatter(self, data):
        close = 2
        volume = 5
        self.scatterChart.changeComp(self.ScatterTab, data, close, volume)


        #fig = Figure(figsize=(4, 3), dpi=100)
        #a = fig.add_subplot(111)
        #t = arange(0.0, 3.0, 0.01)
        #s = sin(2*pi*t)

        #a.plot(t, s)
        #a.set_title('TK embedded matPLot')
        #a.set_xlabel('x lab')
        #a.set_ylabel('y lab')