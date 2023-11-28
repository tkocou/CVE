import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

import global_var as gv

def display_the_result(self):
    self.topp = tk.Toplevel(self)
    self.topp.title("Session Report")
    self.topp.configure(bg="#b7d7c7")
    
    window_height = gv.top_window_y
    window_width = gv.top_window_x
    if gv.platform_os == "Darwin":
        self.topp.resizable(True,True)
        self.topp.minsize(gv.top_window_x,gv.top_window_y)
        self.topp.maxsize(gv.top_window_x,gv.top_window_y)
        
    screen_width = self.topp.winfo_screenwidth()
    screen_height = self.topp.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    self.topp.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    
    
    self.topp.columnconfigure(0,weight=24)
    self.topp.columnconfigure(1,weight=1)
    self.topp.columnconfigure(2,weight=6)
    self.topp.columnconfigure(3,weight=6)
    
    ## GUI Text box to show results
    self.result_text = tk.Text(self.topp)
    self.result_text.grid(column=0, row=3, pady=4, padx=(20,1), sticky='nes')
    self.result_text.configure(background="#d8f8d8", wrap="word", height=40, width=150, fg="#000000")
    self.result_text.delete(1.0,tk.END)
    self.text_scroll = ttk.Scrollbar(self.topp, orient=tk.VERTICAL, command=self.result_text.yview)
    self.text_scroll.grid(column=1, row=3, sticky='nsw', rowspan=20, pady=4)
    self.result_text['yscrollcommand'] = self.text_scroll.set
    
    ## Some buttons
    self.cancel4_button = ttk.Button(self.topp, text = "Cancel", command = self.topp.destroy)
    self.cancel4_button.grid(row=0, column = 0, sticky='e', padx=(20,20), pady=(8,8))
    self.topp.grab_set()
    self.topp.bind('<Escape>', lambda x: self.topp.destroy())
    
    result_line = ""
    
    
    ## convert from dictionary to line of text
    result_ln = ' '.join(key+': '+str(val) for key,val in self.sd.items())
    result_line = result_ln[:-1]
    
    if len(result_line) > 1:
        self.result_text.insert(tk.END,result_line)
        
        