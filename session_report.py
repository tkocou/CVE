import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

import global_var as gv
import display_session_result as dr


def sr_data(self):
    
    self.toppr = tk.Toplevel(self)
    self.toppr.title("Session Report Field Selection")
    self.toppr.configure(bg="#b7d7c7")
    
    window_height = gv.top_window_y
    window_width = gv.top_window_x
    if gv.platform_os == "Darwin":
        self.resizable(True, True)
        self.toppr.minsize(gv.top_window_x,gv.top_window_y)
        self.toppr.maxsize(gv.top_window_x,gv.top_window_y)
        
    screen_width = self.toppr.winfo_screenwidth()
    screen_height = self.toppr.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    self.toppr.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    self.cancel3_button = ttk.Button(self.toppr, text = "Cancel", command = self.toppr.destroy)
    self.cancel3_button.grid(row=0, column = 0, sticky='e', padx=(20,20), pady=(8,8))
    
    
    self.toppr.columnconfigure(0,weight=24)
    self.toppr.columnconfigure(1,weight=1)
    
    self.toppr.rowconfigure(0,weight=1)
    self.toppr.rowconfigure(1,weight=1)
    self.toppr.rowconfigure(2,weight=24)
    self.toppr.rowconfigure(3,weight=1)
    self.toppr.rowconfigure(4,weight=1)
    self.toppr.rowconfigure(5,weight=1)
    self.toppr.rowconfigure(6,weight=1)
    self.toppr.rowconfigure(7,weight=1)
    self.toppr.rowconfigure(8,weight=1)
    self.toppr.rowconfigure(9,weight=1)
    self.toppr.rowconfigure(10,weight=1)
    self.toppr.rowconfigure(11,weight=1)
    self.toppr.rowconfigure(12,weight=1)
    self.toppr.rowconfigure(13,weight=1)
    self.toppr.rowconfigure(14,weight=1)
    self.toppr.rowconfigure(15,weight=1)
    self.toppr.rowconfigure(16,weight=1)
    self.toppr.rowconfigure(17,weight=1)
    
    self.date_var = tk.StringVar()
    self.tid_var = tk.StringVar()
    self.type_var = tk.StringVar()
    self.ve_sess_var = tk.StringVar()
    self.ve_sess_list = []
    self.ve_dict = {}
    self.session_dict = {}
    self.sess_sort_key = tk.StringVar()
    self.sess_sort_key.set(gv.def_sess_sort_key)
    self.sess_sort_dir = True
    
    
    set_gui_session(self)
    refresh_session_screen(self)
    
    
def set_gui_session(self):
    
    self.sessionDb = ttk.Treeview(self.toppr, show='headings', selectmode='browse')
    self.sessionDb['columns'] = gv.sess_treeview_cols
    self.sessionDb.column('date', width=80, minwidth=80)
    self.sessionDb.column('teamId', width=80, minwidth=80)
    self.sessionDb.column('type',width=80,minwidth=80)
    
    self.sessionDb.heading('date', text='Session Timestamp', anchor='w')
    self.sessionDb.heading('teamId', text='Team Id', anchor='w')
    self.sessionDb.heading('type', text='Type of Session', anchor='w')
    
    self.sessionDb.bind('<Double-1>', build_session(self))
    self.sessionDb.grid(row=2, column=0,sticky='nsew',padx=(20,0),pady=(0,10))
    self.sdbscrollbar = ttk.Scrollbar(self.toppr, orient=tk.VERTICAL, command=self.sessionDb.yview)
    self.sessionDb.configure(yscroll=self.sdbscrollbar.set)
    self.sdbscrollbar.grid(row=2,column=1, sticky='nsw',padx=(2,5),pady=(0,10))
    
    self.stvframe = tk.Frame(self.toppr)
    self.stvframe.grid(row=3,column=0,sticky='nsew', padx=20, pady=(0,10))
    
    self.clear3_button = tk.Button(self.stvframe, text = 'Clear Selection', bg="#d0ffd0", command = lambda:clear_session_treeview(self))
    self.clear3_button.grid(row=3, column=0, sticky='nw', padx=(0,8), pady=0)
    self.sess_sort_button = tk.Button(self.stvframe, text = 'Sort Direction Toggle', bg="#d0ffd0", command = lambda:toggle_sdir(self))
    self.sess_sort_button.grid(row=3, column=2, sticky='nw',padx=(20,8), pady=0 )
    self.sort_button = tk.Button(self.stvframe, text='Sort List', bg="#d0ffd0", command= lambda:refresh_session_screen(self))
    self.sort_button.grid(row=4, column=1, sticky='ne', padx=(0,8), pady=0)
    self.make_query_button = tk.Button(self.stvframe, text = 'NEXT', bg="#ffb020", command = lambda:build_session(self))
    self.make_query_button.grid(row=3, column=1, sticky='ne',padx=(20,8), pady=2)
    ## set up radio buttons for sort
    for fld in gv.rb2_cols:
        self.rb = ttk.Radiobutton(self.stvframe, text=fld[0], value=fld[1], variable=self.sess_sort_key)
        self.rb.grid(row=4, column=2, sticky='we', padx=fld[2])

def refresh_session_screen(self):
    sess_tree = self.sessionDb.get_children()
    
    for node in sess_tree:
        self.sessionDb.delete(node)
        
    sessions = get_session_db(self)    
    
    if sessions != None:
        sessions.sort(key=lambda tup: tup[int(self.sess_sort_key.get())], reverse=self.sess_sort_dir)
        
        for session in sessions:
            session_list = []
            session_list.append(session[1]) # 'date'
            session_list.append(session[2]) # 'teamId'
            session_list.append(session[3]) # 'type'
            session_tuple = tuple(session_list)
            self.sessionDb.insert('','end', values=session_tuple)
        
def clear_session_treeview(self):
    if len(self.sessionDb.selection()) > 0:
        self.sessionDb.selection_remove(self.sessionDb.selection()[0])

def toggle_sdir(self):
    if self.sess_sort_dir:
        self.sess_sort_dir = False
    else:
        self.sess_sort_dir = True
    refresh_session_screen(self)

def get_session_db(self):
    conn = self.db_obj.get_connection()
    curs = self.db_obj.get_cursor()
    message = "SELECT * FROM session;"
    self.db_obj.set_SQL(message)
    records = self.db_obj.fetch_all_SQL()
    return records

def get_ve_db(self):
    conn = self.db_obj.get_connection()
    curs = self.db_obj.get_cursor()
    message = "SELECT * FROM ves;"
    self.db_obj.set_SQL(message)
    records = self.db_obj.fetch_all_SQL()
    return records

def build_session(self):
    self.session_dict = {}
    self.session_ve_dict = {}
    session_reference = {}
    self.sd = {}
    
    _iid = self.sessionDb.focus()
    session_reference = self.sessionDb.item(_iid)
    sdb_ref_id = ""
    try: ## in case they click Next without selecting a session
        sdb_ref_id = session_reference['values'][0]
    except:
        return
    curs = self.db_obj.get_cursor()
    curs.execute("SELECT * from session WHERE date = ?",[sdb_ref_id])
    session = curs.fetchone()
    slist = list(session)
    slist.pop(0)
    self.sd = dict.fromkeys(gv.data_json_sess_cols)
    index = 0
    for element in slist:
        self.sd[gv.sess_field_dict[str(index)]] = element
        index += 1
            
    ## Add attending VEs
    timeStamp = '%'+self.sd['date']+'%'
    curs.execute("SELECT * FROM ves WHERE date LIKE ?",[timeStamp])
    ves_returned = curs.fetchall()
    ## 'ves_returned' should hold all VEs who attended the session
    master_index = 1
    for ve in ves_returned:
        ve_list = list(ve)
        ## remove DB index number
        ve_list.pop(0)
        ## create new fields for dictionary
        new_call_field = gv.ve_field_dict['0'] + str(master_index)
        new_name_field = gv.ve_field_dict['1'] + str(master_index)
            
        index = 0
        ## asign data to new fields per each VE
        for ve_record in ve_list:
            if index == 0:
                ## make a new field for sd dictionary
                self.sd[new_call_field] = ve_record + ','
            elif index == 1:
                self.sd[new_name_field] = ve_record + ','
            index += 1
        master_index += 1
        ## send data for displaying
    dr.display_the_result(self)