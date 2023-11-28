import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import csv
import os

import global_var as gv

def save_file(self):
    new_dict_list = self.csv_dict_list
    header_info = gv.data_json_appl_cols
    new_file_name = self.file_name.get()
    file_path = os.path.join(gv.base_rpt_dir,new_file_name)
    
    with open(file_path,'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = header_info)
        writer.writeheader()
        writer.writerows(new_dict_list)
        
    mb.showinfo('Done','File '+file_path+' has been written!')
    self.top2.destroy()


def save_as_csv(self):
    self.top2 = tk.Toplevel(self)
    self.top2.title("Save as CSV file")
    self.top2.configure(bg="#b7d7c7")
    
    window_height = 300
    window_width = 600
    screen_width = self.top2.winfo_screenwidth()
    screen_height = self.top2.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    self.top2.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    
    
    self.file_name = tk.StringVar()
    
    self.file_name.set("Default.csv")
    
    self.file_name_label = tk.Label(self.top2,text="Filename? ")
    self.file_name_label.grid(column=0, row=0, sticky='e', padx=(20,1), pady=(8,8))
    self.file_name_entry = tk.Entry(self.top2, textvariable=self.file_name, width=40)
    self.file_name_entry.grid(column=1, row=0, sticky='w', padx=(20,1), pady=(8,8))
    self.file_name_entry.grid_configure(columnspan=2)
    self.save_button = tk.Button(self.top2, text="Save file", command=lambda: save_file(self))
    self.save_button.grid(column=0, row=1, sticky='e', padx=(20,1), pady=(8,8))
    self.cancel_button = ttk.Button(self.top2, text = "Cancel", command = self.top2.destroy)
    self.cancel_button.grid(row=1, column = 1, sticky='w', padx=(20,1), pady=(8,8))
    
    
    self.top2.grab_set()
    self.top2.bind('<Escape>', lambda x: self.top2.destroy())
    
    
