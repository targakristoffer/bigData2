try:
    import tkinter as tk
    import tkinter.ttk as ttk
except ImportError:
    import Tkinter as tk
    import ttk

class Button_tweet(ttk.Button):
    def __init__(self, parent, text, guiFunction, row, column):
        super().__init__(parent, text=text, command=guiFunction, width=105)
        theme = ttk.Style()
        

        theme.configure(self.winfo_class(), padding=6, background="#FFF", foreground="#DF34DF", font=("Helvitca", 12))
        
        self.grid(row=row, column=column, padx=1, pady=1)

     
    def add(self):
        print('asda')