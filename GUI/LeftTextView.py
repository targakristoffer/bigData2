try:
    import tkinter as tk
    import tkinter.ttk as ttk
except ImportError:
    import Tkinter as tk
    import ttk


class LeftTextView(tk.Text):
    def __init__(self, parent, setHeight, setWidth):
        super().__init__(parent, height=setHeight, width=setWidth)
        
    def remove(self):
        self.delete('1.0', 'end')

    def fill(self, text):
        text = self.stripChars(text)
        self.insert('1.0', text)

    def getContent(self):
        content = self.get('1.0', 'end')
        return content

    def stripChars(self, text):
        ntext = ''
        allowed_chars = [text[char] for char in range(len(text)) if ord(text[char]) in range(65536)]
        for chars in allowed_chars:
            ntext += chars
        return ntext

    def packself(self):
        self.grid(row=1, column=0)