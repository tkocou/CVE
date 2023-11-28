import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

import global_var as gv
import display_sql_result as dsr

def get_by_field(self):
   ## The display of the search results in a toplevel window
    if not self.sel_parm_items and not self.sel_col_items and not self.tv_flag:
        mb.showerror('Error', 'No fields were selected for the query!')
        return
    
    self.topper = tk.Toplevel(self)
    self.topper.title("Field Selection")
    self.topper.configure(bg="#b7d7c7")
    
    window_height = gv.top_window_y
    window_width = gv.top_window_x
    if gv.platform_os == "Darwin":
        self.topper.resizable(True, True)
        self.topper.minsize(gv.top_window_x,gv.top_window_y)
        self.topper.maxsize(gv.top_window_x,gv.top_window_y)
        
    screen_width = self.topper.winfo_screenwidth()
    screen_height = self.topper.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    self.topper.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    
    self.topper.columnconfigure(0,weight=8)
    self.topper.columnconfigure(1,weight=8)
    self.topper.columnconfigure(2,weight=24)
    
    self.topper.rowconfigure(0,weight=1)
    self.topper.rowconfigure(1,weight=1)
    self.topper.rowconfigure(2,weight=1)
    self.topper.rowconfigure(3,weight=1)
    self.topper.rowconfigure(4,weight=1)
    self.topper.rowconfigure(5,weight=1)
    self.topper.rowconfigure(6,weight=1)
    self.topper.rowconfigure(7,weight=1)
    self.topper.rowconfigure(8,weight=1)
    self.topper.rowconfigure(9,weight=1)
    self.topper.rowconfigure(10,weight=1)
    self.topper.rowconfigure(11,weight=1)
    self.topper.rowconfigure(12,weight=1)
    self.topper.rowconfigure(13,weight=1)
    self.topper.rowconfigure(14,weight=1)
    self.topper.rowconfigure(15,weight=1)
    self.topper.rowconfigure(16,weight=1)
    self.topper.rowconfigure(17,weight=1)
    
    
    
    self.fn_var = tk.StringVar()
    self.mid_var = tk.StringVar()
    self.last_var = tk.StringVar()
    self.suf_var = tk.StringVar()
    self.email_var = tk.StringVar()
    self.frn_var =tk.StringVar()
    self.cs_var = tk.StringVar()
    self.city_var = tk.StringVar()
    self.st_var = tk.StringVar()
    self.e2_var = tk.StringVar()
    self.e3_var = tk.StringVar()
    self.e4_var = tk.StringVar()
    self.session_date_var = tk.StringVar()
    self.tid_var = tk.StringVar()
    
    ## create a flag dictionary to track which fields are being used for a sql query
    ## first set flags to false
    self.sel_flag_dict = gv.appl_flag_dict.copy()
    self.parm_flag_dict  = gv.appl_flag_dict.copy()
    keys = gv.appl_flag_dict.keys()
    for x in keys:
        self.sel_flag_dict[x]="0" # False
        self.parm_flag_dict[x]="0"
    
    ## raise a flag if the column was selected for query in CVE-DB.py
    self.tmp_sel_list = []
    if  len(self.sel_col_items) > 0:
        ## temporarily save list - used in compile function
        self.tmp_sel_list.extend(self.sel_col_items)
        for x in self.sel_col_items:
            self.sel_flag_dict[x] = '1'
    
    ## Ditto for parameter data        
    if len(self.sel_parm_items) > 0:
        for x in self.sel_parm_items:
            self.parm_flag_dict[x] = '1'
        
    self.gui_query_dict = {}
    ## from 'fetch_applicant()' in CVE-DB.py
    ## did we select someone from the list - treeview? or listbox?
    if self.local_sql_dict:
        keys = self.local_sql_dict.keys()
        for key in keys:
            if self.parm_flag_dict[key] == '1':
                ## assign the data from the selected applicant to the SQL query_dict
                self.gui_query_dict.update({key:self.local_sql_dict[key]})
    
    ##### if applicant was selected from the treeview
    ##### fill variables with treeview data via self.tv_flag
    
    #### first name GUI line
    self.fn_col_label = tk.Label(self.topper)
    self.fn_col_label.grid(row=1,column=0,padx=(2,2),sticky='w')
    ## set background color depending on if selected
    if self.sel_flag_dict[gv.field_dict["0"]] == '1':
        self.fn_col_label.configure(text = "First Name Selected",bg="#6ecfa8")
    else:
        self.fn_col_label.configure(text = "First Name Not Selected",bg="#ffa0b8")
        
    self.fn_label = tk.Label(self.topper, text="First Name:")
    self.fn_label.grid(row=1,column=1, padx=(2,2), sticky='e')
    
    if self.parm_flag_dict[gv.field_dict['0']] == '1':
        self.fn_label.configure(bg="#6ecfa8")
        if self.tv_flag:
            self.fn_var.set(self.local_sql_dict[gv.data_json_appl_cols[0]])
        else:
            if self.local_sql_dict:
                self.fn_var.set(self.gui_query_dict[gv.field_dict['0']])
    else:
        self.fn_label.configure(bg="#ffa0b8")
    self.fn_entry = tk.Entry(self.topper, textvariable=self.fn_var, width=60)
    self.fn_entry.grid(row=1,column=2, padx=(2,2), sticky='w')
    
    #### middle GUI line
    self.mid_col_label = tk.Label(self.topper)
    self.mid_col_label.grid(row=2,column=0,padx=(2,2),sticky='w')
    ## set background color depending on if selected
    if self.sel_flag_dict[gv.field_dict["1"]] == '1':
        self.mid_col_label.configure(text = "Middle Selected",bg="#6ecfa8")
    else:
        self.mid_col_label.configure(text = "Middle Not Selected",bg="#ffa0b8")
        
    self.mid_label = tk.Label(self.topper, text="Middle:")
    self.mid_label.grid(row=2,column=1, padx=(2,2), sticky='e')
    if self.parm_flag_dict[gv.field_dict['1']] == '1':
        self.mid_label.configure(bg="#6ecfa8")
        if self.tv_flag:
            self.mid_var.set(self.local_sql_dict[gv.data_json_appl_cols[1]])
        else:
            if self.local_sql_dict:
                self.mid_var.set(self.gui_query_dict[gv.field_dict['1']])
    else:
        self.mid_label.configure(bg="#ffa0b8")
    self.mid_entry = tk.Entry(self.topper, textvariable=self.mid_var, width=60)
    self.mid_entry.grid(row=2, column=2, padx=(2,2), sticky='w')
    
    #### last name GUI line
    self.ln_col_label = tk.Label(self.topper)
    self.ln_col_label.grid(row=3,column=0,padx=(2,2),sticky='w')
    ## set background color depending on if selected
    if self.sel_flag_dict[gv.field_dict["2"]] == '1':
        self.ln_col_label.configure(text = "Last Name Selected",bg="#6ecfa8")
    else:
        self.ln_col_label.configure(text = "Last Name Not Selected",bg="#ffa0b8")
     
    self.last_label = tk.Label(self.topper, text="Last Name:")
    self.last_label.grid(row=3,column=1, padx=(2,2), sticky='e')
    if self.parm_flag_dict[gv.field_dict['2']] == '1':
        self.last_label.configure(bg="#6ecfa8")
        if self.tv_flag:
            self.last_var.set(self.local_sql_dict[gv.data_json_appl_cols[2]])
        else:
            if self.local_sql_dict:
                self.last_var.set(self.gui_query_dict[gv.field_dict['2']])
    else:
        self.last_label.configure(bg="#ffa0b8")
    self.last_entry = tk.Entry(self.topper, textvariable=self.last_var, width=60)
    self.last_entry.grid(row=3, column=2, padx=(2,2), sticky='w')
    
    #### suffix GUI line
    self.suf_col_label = tk.Label(self.topper)
    self.suf_col_label.grid(row=4,column=0,padx=(2,2),sticky='w')
    ## set background color depending on if selected
    if self.sel_flag_dict[gv.field_dict["3"]] == '1':
        self.suf_col_label.configure(text = "Suffix Selected",bg="#6ecfa8")
    else:
        self.suf_col_label.configure(text = "Suffix Not Selected",bg="#ffa0b8")
     
    self.suf_label = tk.Label(self.topper, text="Suffix:")
    self.suf_label.grid(row=4,column=1, padx=(2,2), sticky='e')
    if self.parm_flag_dict[gv.field_dict['3']] == '1':
        self.suf_label.configure(bg="#6ecfa8")
        if tv_flag:
            self.suf_var.set(self.local_sql_dict[gv.data_json_appl_cols[3]])
        else:
            if self.local_sql_dict:
                self.suf_var.set(self.gui_query_dict[gv.field_dict['3']])
    else:
        self.suf_label.configure(bg="#ffa0b8")
    self.suf_entry = tk.Entry(self.topper, textvariable=self.suf_var, width=60)
    self.suf_entry.grid(row=4, column=2, padx=(2,2), sticky='w')
    
    #### email GUI line
    self.em_col_label = tk.Label(self.topper)
    self.em_col_label.grid(row=5,column=0,padx=(2,2),sticky='w')
    ## set background color depending on if selected
    if self.sel_flag_dict[gv.field_dict["4"]] == '1':
        self.em_col_label.configure(text = "Email Address Selected",bg="#6ecfa8")
    else:
        self.em_col_label.configure(text = "Email Address Not Selected",bg="#ffa0b8")
    
    self.email_label = tk.Label(self.topper, text="Email Address:")
    self.email_label.grid(row=5,column=1, padx=(2,2), sticky='e')
    if self.parm_flag_dict[gv.field_dict['4']] == '1':
        self.email_label.configure(bg="#6ecfa8")
        if self.tv_flag:
            self.email_var.set(self.local_sql_dict[gv.data_json_appl_cols[4]])
        else:
            if self.local_sql_dict:
                self.email_var.set(self.gui_query_dict[gv.field_dict['4']])
    else:
        self.email_label.configure(bg="#ffa0b8")
    self.email_entry = tk.Entry(self.topper, textvariable=self.email_var, width=60)
    self.email_entry.grid(row=5, column=2, padx=(2,2), sticky='w')
    
    #### FRN GUI line
    self.frn_col_label = tk.Label(self.topper)
    self.frn_col_label.grid(row=6,column=0,padx=(2,2),sticky='w')
    ## set background color depending on if selected
    if self.sel_flag_dict[gv.field_dict["5"]] == '1':
        self.frn_col_label.configure(text = "FRN Selected",bg="#6ecfa8")
    else:
        self.frn_col_label.configure(text = "FRN Not Selected",bg="#ffa0b8")
    
    self.frn_label = tk.Label(self.topper, text="FRN:")
    self.frn_label.grid(row=6,column=1, padx=(2,2), sticky='e')
    if self.parm_flag_dict[gv.field_dict['5']] == '1':
        self.frn_label.configure(bg="#6ecfa8")
        if self.tv_flag:
            self.frn_var.set(self.local_sql_dict[gv.data_json_appl_cols[5]])
        else:
            if self.local_sql_dict:
                self.frn_var.set(self.gui_query_dict[gv.field_dict['5']])
    else:
        self.frn_label.configure(bg="#ffa0b8")
    self.frn_entry = tk.Entry(self.topper, textvariable=self.frn_var, width=60)
    self.frn_entry.grid(row=6, column=2, padx=(2,2), sticky='w')
    
    #### Callsign GUI line
    self.cs_col_label = tk.Label(self.topper)
    self.cs_col_label.grid(row=7,column=0,padx=(2,2),sticky='w')
    ## set background color depending on if selected
    if self.sel_flag_dict[gv.field_dict["6"]] == '1':
        self.cs_col_label.configure(text = "Callsign Selected",bg="#6ecfa8")
    else:
        self.cs_col_label.configure(text = "Callsign Not Selected",bg="#ffa0b8")
    
    self.cs_label = tk.Label(self.topper, text="Callsign:")
    self.cs_label.grid(row=7,column=1, padx=(2,2), sticky='e')
    if self.parm_flag_dict[gv.field_dict['6']] == '1':
        self.cs_label.configure(bg="#6ecfa8")
        if self.tv_flag:
            self.cs_var.set(self.local_sql_dict[gv.data_json_appl_cols[6]])
        else:
            if self.local_sql_dict:
                self.cs_var.set(self.gui_query_dict[gv.field_dict['6']])
    else:
        self.cs_label.configure(bg="#ffa0b8")
    self.cs_entry = tk.Entry(self.topper, textvariable=self.cs_var, width=60)
    self.cs_entry.grid(row=7, column=2, padx=(2,2), sticky='w')
    
    #### City GUI line
    self.ct_col_label = tk.Label(self.topper)
    self.ct_col_label.grid(row=8,column=0,padx=(2,2),sticky='w')
    ## set background color depending on if selected
    if self.sel_flag_dict[gv.field_dict["7"]] == '1':
        self.ct_col_label.configure(text = "City Selected",bg="#6ecfa8")
    else:
        self.ct_col_label.configure(text = "City Not Selected",bg="#ffa0b8")
    
    self.city_label = tk.Label(self.topper, text="City:")
    self.city_label.grid(row=8,column=1, padx=(2,2), sticky='e')
    if self.parm_flag_dict[gv.field_dict['7']] == '1':
        self.city_label.configure(bg="#6ecfa8")
        if self.tv_flag:
            self.city_var.set(self.local_sql_dict[gv.data_json_appl_cols[7]])
        else:
            if self.local_sql_dict:
                self.city_var.set(self.gui_query_dict[gv.field_dict['7']])
    else:
        self.city_label.configure(bg="#ffa0b8")
    self.city_entry = tk.Entry(self.topper, textvariable=self.city_var, width=60)
    self.city_entry.grid(row=8, column=2, padx=(2,2), sticky='w')
    
    #### State GUI line
    self.st_col_label = tk.Label(self.topper)
    self.st_col_label.grid(row=9,column=0,padx=(2,2),sticky='w')
    ## set background color depending on if selected
    if self.sel_flag_dict[gv.field_dict["8"]] == '1':
        self.st_col_label.configure(text = "State Selected",bg="#6ecfa8")
    else:
        self.st_col_label.configure(text = "State Not Selected",bg="#ffa0b8")
    
    self.st_label = tk.Label(self.topper, text="State:")
    self.st_label.grid(row=9,column=1, padx=(2,2), sticky='e')
    if self.parm_flag_dict[gv.field_dict['8']] == '1':
        self.st_label.configure(bg="#6ecfa8")
        if self.tv_flag:
            self.st_var.set(self.local_sql_dict[gv.data_json_appl_cols[8]])
        else:
            if self.local_sql_dict:
                self.st_var.set(self.gui_query_dict[gv.field_dict['8']])
    else:
        self.st_label.configure(bg="#ffa0b8")
    self.st_entry = tk.Entry(self.topper, textvariable=self.st_var, width=60)
    self.st_entry.grid(row=9, column=2, padx=(2,2), sticky='w')
    
    #### Element 2 GUI line
    self.e2_col_label = tk.Label(self.topper)
    self.e2_col_label.grid(row=10,column=0,padx=(2,2),sticky='w')
    ## set background color depending on if selected
    if self.sel_flag_dict[gv.field_dict["9"]] == '1':
        self.e2_col_label.configure(text = "Element 2 Selected",bg="#6ecfa8")
    else:
        self.e2_col_label.configure(text = "Element 2 Not Selected",bg="#ffa0b8")
    
    self.e2_label = tk.Label(self.topper, text="Element 2:")
    self.e2_label.grid(row=10,column=1, padx=(2,2), sticky='e')
    if self.parm_flag_dict[gv.field_dict['9']] == '1':
        self.e2_label.configure(bg="#6ecfa8")
        if self.tv_flag:
            self.e2_var.set(self.local_sql_dict[gv.data_json_appl_cols[9]])
        else:
            if self.local_sql_dict:
                self.e2_var.set(self.gui_query_dict[gv.field_dict['9']])
    else:
        self.e2_label.configure(bg="#ffa0b8")
    self.e2_entry = tk.Entry(self.topper, textvariable=self.e2_var, width=60)
    self.e2_entry.grid(row=10, column=2, padx=(2,2), sticky='w')
    
    #### Element 3 GUI line
    self.e3_col_label = tk.Label(self.topper)
    self.e3_col_label.grid(row=11,column=0,padx=(2,2),sticky='w')
    ## set background color depending on if selected
    if self.sel_flag_dict[gv.field_dict["10"]] == '1':
        self.e3_col_label.configure(text = "Element 3 Selected",bg="#6ecfa8")
    else:
        self.e3_col_label.configure(text = "Element 3 Not Selected",bg="#ffa0b8")
    
    self.e3_label = tk.Label(self.topper, text="Element 3:")
    self.e3_label.grid(row=11,column=1, padx=(2,2), sticky='e')
    if self.parm_flag_dict[gv.field_dict['10']] == '1':
        self.e3_label.configure(bg="#6ecfa8")
        if self.tv_flag:
            self.e3_var.set(self.local_sql_dict[gv.data_json_appl_cols[10]])
        else:
            if self.local_sql_dict:
                self.e3_var.set(self.gui_query_dict[gv.field_dict['10']])
    else:
        self.e3_label.configure(bg="#ffa0b8")
    self.e3_entry = tk.Entry(self.topper, textvariable=self.e3_var, width=60)
    self.e3_entry.grid(row=11, column=2, padx=(2,2), sticky='w')
    
    #### Element 4 GUI line
    self.e4_col_label = tk.Label(self.topper)
    self.e4_col_label.grid(row=12,column=0,padx=(2,2),sticky='w')
    ## set background color depending on if selected
    if self.sel_flag_dict[gv.field_dict["11"]] == '1':
        self.e4_col_label.configure(text = "Element 4 Selected",bg="#6ecfa8")
    else:
        self.e4_col_label.configure(text = "Element 4 Not Selected",bg="#ffa0b8")
    
    self.e4_label = tk.Label(self.topper, text="Element 4:")
    self.e4_label.grid(row=12,column=1, padx=(2,2), sticky='e')
    if self.parm_flag_dict[gv.field_dict['11']] == '1':
        self.e4_label.configure(bg="#6ecfa8")
        if self.tv_flag:
            self.e4_var.set(self.local_sql_dict[gv.data_json_appl_cols[11]])
        else:
            if self.local_sql_dict:
                self.e4_var.set(self.gui_query_dict[gv.field_dict['11']])
    else:
        self.e4_label.configure(bg="#ffa0b8")
    self.e4_entry = tk.Entry(self.topper, textvariable=self.e4_var, width=60)
    self.e4_entry.grid(row=12, column=2, padx=(2,2), sticky='w')
    
    #### Session Date GUI line
    self.date_col_label = tk.Label(self.topper)
    self.date_col_label.grid(row=13,column=0,padx=(2,2),sticky='w')
    ## set background color depending on if selected
    if self.sel_flag_dict[gv.field_dict["12"]] == '1':
        self.date_col_label.configure(text = "Session Date Selected",bg="#6ecfa8")
    else:
        self.date_col_label.configure(text = "Session Date Not Selected",bg="#ffa0b8")
    
    self.date_label = tk.Label(self.topper, text="Session Date:")
    self.date_label.grid(row=13,column=1, padx=(2,2), sticky='e')
    if self.parm_flag_dict[gv.field_dict['12']] == '1':
        self.date_label.configure(bg="#6ecfa8")
        if self.tv_flag:
            self.session_date_var.set(self.local_sql_dict[gv.data_json_appl_cols[12]])
        else:
            if self.local_sql_dict:
                self.session_date_var.set(self.gui_query_dict[gv.field_dict['12']])
    else:
        self.date_label.configure(bg="#ffa0b8")
    self.date_entry = tk.Entry(self.topper, textvariable=self.session_date_var, width=60)
    self.date_entry.grid(row=13, column=2, padx=(2,2), sticky='w')
    
    #### Team Id GUI line
    self.tid_col_label = tk.Label(self.topper)
    self.tid_col_label.grid(row=14,column=0,padx=(2,2),sticky='w')
    ## set background color depending on if selected
    if self.sel_flag_dict[gv.field_dict["13"]] == '1':
        self.tid_col_label.configure(text = "Team Id Selected",bg="#6ecfa8")
    else:
        self.tid_col_label.configure(text = "Team Id Not Selected",bg="#ffa0b8")
    
    self.tid_label = tk.Label(self.topper, text="Team Id:")
    self.tid_label.grid(row=14,column=1, padx=(2,2), sticky='e')
    if self.parm_flag_dict[gv.field_dict['13']] == '1':
        self.tid_label.configure(bg="#6ecfa8")
        if self.tv_flag:
            self.tid_var.set(self.local_sql_dict[gv.data_json_appl_cols[13]])
        else:
            if self.local_sql_dict:
                self.tid_var.set(self.gui_query_dict[gv.field_dict['13']])
    else:
        self.tid_label.configure(bg="#ffa0b8")
    self.tid_entry = tk.Entry(self.topper, textvariable=self.tid_var, width=60)
    self.tid_entry.grid(row=14, column=2, padx=(2,2), sticky='w')

    
    self.cancel_button = ttk.Button(self.topper, text = "Cancel", command = self.topper.destroy)
    self.cancel_button.grid(row=0, column = 0, padx=(20,20), pady=(8,8))
                
    self.query_button = tk.Button(self.topper, text="NEXT", command = lambda: compile_query(self))
    self.query_button.grid(row=0, column=1,padx=(20,20),pady=(8,8))
    self.query_button.configure(bg="#f0b020")
    
    self.topper.grab_set()
    self.topper.bind('<Escape>', lambda x: self.topper.destroy())
    
def get_param_data(self):
    self.sql_query_dict = {}
    ## populate sql_query depending on which fields were selected
    for field in gv.data_json_appl_cols:
        if field == "firstname" and self.parm_flag_dict[field] == '1':
            self.sql_query_dict[field] = self.fn_var.get()
        elif field == "middle" and self.parm_flag_dict[field] == '1':
            self.sql_query_dict[field] = self.mid_var.get()
        elif field == "lastname" and self.parm_flag_dict[field] == '1':
            self.sql_query_dict[field] = self.last_var.get()
        elif field == "suffix" and self.parm_flag_dict[field] == '1':
            self.sql_query_dict[field] = self.suf_var.get()
        elif field == "email" and self.parm_flag_dict[field] == '1':
            self.sql_query_dict[field] = self.email_var.get()
        elif field == "frn" and self.parm_flag_dict[field] == '1':
            self.sql_query_dict[field] = self.frn_var.get()
        elif field == "callsign" and self.parm_flag_dict[field] == '1':
            self.sql_query_dict[field] = self.cs_var.get()
        elif field == "city" and self.parm_flag_dict[field] == '1':
            self.sql_query_dict[field] = self.city_var.get()
        elif field == "state" and self.parm_flag_dict[field] == '1':
            self.sql_query_dict[field] = self.st_var.get()
        elif field == "E2" and self.parm_flag_dict[field] == '1':
            self.sql_query_dict[field] = self.e2_var.get()
        elif field == "E3" and self.parm_flag_dict[field] == '1':
            self.sql_query_dict[field] = self.e3_var.get()
        elif field == "E4" and self.parm_flag_dict[field] == '1':
            self.sql_query_dict[field] = self.e4_var.get()
        elif field == "sessionDate" and self.parm_flag_dict[field] == '1':
            self.sql_query_dict[field] = self.session_date_var.get()
        elif field == "teamId" and self.parm_flag_dict[field] == '1':
            self.sql_query_dict[field] = self.tid_var.get()
            
            

def compile_query(self):
    ## convert column, parameter data into DB-API 2.0 statement
    self.sql_message = "SELECT "
    if self.tmp_sel_list:
        keys = self.sel_flag_dict.keys()
        index = 1
        for key in keys:
            if self.sel_flag_dict[key] == '1':
                self.sql_message += " "+key
                if index < len(self.tmp_sel_list):
                    self.sql_message += ','
                    index += 1
    else:
        self.sql_message += " * "
    self.sql_message += " FROM applicant"
    get_param_data(self)
    if self.sql_query_dict:
        self.sql_message += " WHERE "
        keys = self.parm_flag_dict.keys()
        index = 1
        for key in keys:
            if self.parm_flag_dict[key] == '1':
                self.sql_message += key+' LIKE "%'+self.sql_query_dict[key]+'%"'
                if index < len(self.sql_query_dict):
                    self.sql_message += " AND "
                    index += 1
    self.sql_message += ";"
    
    ## test sql query
    c = self.db_obj.get_cursor()
    c.execute(self.sql_message)
    self.query_result = c.fetchall()
    ## Build CSV data from SQL Query
    self.csv_dict_list = []
    ## build reference dictionary list before displaying data
    for line in self.query_result:
        tmp_dict = {}
        ## convert the text from tuple to list
        new_line = list(line)
        ## remove the SQL index
        new_line.pop(0)
        index = 0
        for fld in new_line:
            try:
                new_fld = fld.replace('"','')
                tmp_dict[gv.data_json_appl_cols[index]] = new_fld
            except:
                pass
            index += 1
        self.csv_dict_list.append(tmp_dict)
    ## display the query results
    dsr.display_result(self)
    self.topper.destroy()