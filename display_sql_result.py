import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

import global_var as gv
import csv_save as cv

    
        
def capture_text_box(self):
    ## save the contents of the Text widget for Text files
    ## clear out old info
    tmp_text = ""
    self.text_text = ""
    self.text_list = []
    ## load up text from display
    self.text_text = self.result_text.get(1.0,tk.END)
    txt_len = len(self.text_text)
    ## check for extra CRs at end of acquired text
    if self.text_text[txt_len - 2:] == '\n\n':
        ## remove them
        tmp_text = self.text_text[:-2]
    ## create list
        self.text_list = tmp_text.split('\n')
    else:
        self.text_list = self.text_text.split('\n')
    
def filter_display(self):
    
    uniq_list = []
    text_in_box = self.text_list
    ## Use 'set' function to filter data
    unique_set = set(text_in_box)
    uniq_list = list(unique_set)
    ## clear out text in box
    self.result_text.delete(1.0,tk.END)
    ## repopulate Text box with unique data
    for item in uniq_list:
        item += '\n'
        self.result_text.insert(tk.END,item)
    ## capture new displayed text
    capture_text_box(self)    


def display_result(self):
    
    self.top = tk.Toplevel(self)
    self.top.title("SQL Result")
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
    
    self.sql_cmd = tk.StringVar()
    
    ## GUI Text box to show result of sql query
    self.result_text = tk.Text(self.top)
    self.result_text.grid(column=0, row=3, pady=4, padx=(20,1), sticky='nws')
    self.result_text.configure(background="#d8f8d8", wrap="word", height=40, width=150,fg="#000000")
    self.result_text.delete(1.0,tk.END)
    self.text_scroll = ttk.Scrollbar(self.top, orient=tk.VERTICAL, command=self.result_text.yview)
    self.text_scroll.grid(column=0, row=3, sticky='nse', rowspan=20, pady=4)
    self.result_text['yscrollcommand'] = self.text_scroll.set
    
    ## GUI Entry to show sql query text
    self.sql_cmd.set(self.sql_message)
    self.sql_query_label = tk.Label(self.top, text="SQL Command:")
    self.sql_query_label.grid(column=0, row=1, sticky='w', padx=(20,1))
    self.sql_query_text = tk.Entry(self.top, textvariable=self.sql_cmd, state=tk.DISABLED, width=150)
    self.sql_query_text.grid(column=0,columnspan=2,row=2,sticky='w',padx=(20,1))
    self.sql_query_text.configure(bg="#000000", fg="#ffffff")
    
    ## Note: self.query_result is a list of tuples
    for line in list(self.query_result):
        text_line = ""
        index = 0
        for s in line:
            if isinstance(s,int) == False:
                if index < 18:
                    if index == 9:
                        text_line += 'E2-'+s.replace('"','')+" "
                    elif index == 10:
                        text_line += 'E3-'+s.replace('"','')+" "
                    elif index == 11:
                        text_line += 'E4-'+s.replace('"','')+" "
                    elif index == 14:
                        text_line += ' '+s.replace('"','')+" "
                    elif s != None:
                        if len(line) == 1:
                            text_line += s.replace('"','')
                        else:
                            text_line += s.replace('"','')+" "
                index += 1
        ## fix end character in text_line
        if text_line[:-1] == ' ':
            text_line = text_line[:-1] + '\n'
        else:
            text_line += '\n'
        if len(text_line) > 1:
            self.result_text.insert(tk.END,text_line)
    ## capture displayed text
    capture_text_box(self)
    
    
    self.cancel2_button = ttk.Button(self.top, text = "Cancel", command = self.top.destroy)
    self.cancel2_button.grid(row=0, column = 0, sticky='e', padx=(20,20), pady=(8,8))
    
    self.csv_save_button = ttk.Button(self.top, text="Save data on screen as CSV file", command=lambda: cv.save_as_csv(self))
    self.csv_save_button.grid(row=0, column = 0, sticky='w', padx=(20,20), pady=(8,8))
    self.uniq_button = ttk.Button(self.top, text="Filter data as unique", command=lambda: filter_display(self))
    self.uniq_button.grid(row=0, column=0, sticky='w',pady=(8,8), padx=(300,20))
    
    self.top.grab_set()
    self.top.bind('<Escape>', lambda x: self.top.destroy())