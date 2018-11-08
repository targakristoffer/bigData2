try:
    import tkinter as tk
    import tkinter.ttk as ttk
except ImportError:
    import Tkinter as tk
    import ttk



class MenuBar():
    def __init__(self, parent, hello):
        super()

        menubar = tk.Menu(parent)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Åpne", command=hello)
        filemenu.add_command(label="Lagre", command=hello)
        filemenu.add_separator()
        filemenu.add_command(label="Gå ut", command=parent.quit)
        menubar.add_cascade(label="Hovedmeny", menu=filemenu)

        # create more pulldown menus
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Klipp ut", command=hello)
        editmenu.add_command(label="Kopier", command=hello)
        editmenu.add_command(label="Lagre", command=hello)
        menubar.add_cascade(label="Verktøy", menu=editmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Hvordan", command=hello)
        menubar.add_cascade(label="Hjelp", menu=helpmenu)

        parent.configure(menu=menubar)