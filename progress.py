import tkinter as tk
from tkinter import ttk


class Progress():
    def __init__(self,master):
        super().__init__()
        ## master is the parent window to this toplevel window
        self.top = tk.Toplevel(master)
        ## kill this window if 'X' is clicked
        self.top.bind('<Escape>', lambda x: self.top.destroy())
        ## center this window
        window_height = 100
        window_width = 300
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        ## set up color style for progress bar
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("green.Horizontal.TProgressbar",
            background="#c0ffc0",
            foreground="black",
            fieldbackground="#c0ffc0"
            )
        ## place the Progressbar widget in the window
        self.progress_bar = ttk.Progressbar(self.top, orient='horizontal', mode='indeterminate', length=120, style="green.Horizontal.TProgressbar")
        self.progress_bar.grid(column=0, row=0, sticky='w', padx=20, pady=20)
        self.progress_bar["value"]=0
        ## init the motion control variables
        self.toggle = 0
        self.delta = True

    ## this method is called when the progress bar needs to be visually updated
    ## during a task
    def update_pb(self):
        ## move the bar position value
        if self.delta:
            self.toggle += 20
        else:
            self.toggle -= 20
        ## reverse direction when hitting limits
        if self.toggle == 100:
            self.delta = False
        elif self.toggle == 0:
            self.delta = True
        ## update the bar position
        self.progress_bar["value"] = self.toggle
        self.top.update_idletasks()
    
    ## Kill this window when finished with tasks
    def close(self):
        self.top.destroy()