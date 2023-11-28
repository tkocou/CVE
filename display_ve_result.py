import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

import global_var as gv


        
def display_result(self):
    
    self.top = tk.Toplevel(self)
    self.top.title("VE Report")
    self.top.configure(bg="#b7d7c7")
    
    window_height = gv.top_window_y
    window_width = gv.top_window_x
    if gv.platform_os == "Darwin":
        self.top.resizable(True, True)
        self.top.minsize(gv.top_window_x,gv.top_window_y)
        self.top.maxsize(gv.top_window_x,gv.top_window_y)
        
    screen_width = self.top.winfo_screenwidth()
    screen_height = self.top.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    self.top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    
    
    self.top.columnconfigure(0,weight=24)
    self.top.columnconfigure(1,weight=1)
    self.top.columnconfigure(2,weight=6)
    self.top.columnconfigure(3,weight=6)
    
    ## GUI Text box to show result of VE report
    self.result_ve_text = tk.Text(self.top)
    self.result_ve_text.grid(column=0, row=3, pady=4, padx=(20,1), sticky='nws')
    self.result_ve_text.configure(background="#d8f8d8", wrap="word", height=40, width=150,fg="#000000")
    self.result_ve_text.delete(1.0,tk.END)
    self.text_scroll = ttk.Scrollbar(self.top, orient=tk.VERTICAL, command=self.result_ve_text.yview)
    self.text_scroll.grid(column=0, row=3, sticky='nse', rowspan=20, pady=4)
    self.result_ve_text['yscrollcommand'] = self.text_scroll.set
    
    
    self.cancel2_button = ttk.Button(self.top, text = "Cancel", command = self.top.destroy)
    self.cancel2_button.grid(row=0, column = 0, sticky='e', padx=(20,20), pady=(8,8))
    
    self.top.grab_set()
    self.top.bind('<Escape>', lambda x: self.top.destroy())
    
    self.text_ve = ""
    self.text_ve = self.vdb_ref_call + " has attended " + str(len(self.vlist)) + " sessions and has signed documents for the following FRNs:\n\n"
    for item in self.signing_list:
        self.text_ve += item+'\n'
        
    self.result_ve_text.insert(tk.END,self.text_ve)
    