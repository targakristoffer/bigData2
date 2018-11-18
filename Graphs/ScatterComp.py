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

class ScatterComp():
    def __init__(self):
        super().__init__()

    def drawComp(self, parent, data, close, volume):

        size = [20*4**n for n in range(len(data))]

        self.fig, self.ax = plt.subplots(figsize=(4,3))  
        self.ax.scatter(data[0], data[1], c='#34D63D', s=size, alpha=0.5)

        self.ax.set_title('TK embedded matPLot')
        self.ax.set_xlabel('x lab')
        self.ax.set_ylabel('y lab')

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid()
        self.canvas._tkcanvas.grid()
        self.fig.tight_layout()
    
    def changeComp(self, parent, data, close, volume):

        size = [20*4**n for n in range(len(data))]

        self.ax.scatter(data[0], data[1], c='#34D63D', s=size, alpha=0.5)

        self.ax.set_title('TK embedded matPLot')
        self.ax.set_xlabel('x lab')
        self.ax.set_ylabel('y lab')
        self.canvas.draw()
        