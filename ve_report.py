import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

import global_var as gv
import display_ve_result as dvr


def vr_data(self):
    
    self.topr = tk.Toplevel(self)
    self.topr.title("VE Report")
    self.topr.configure(bg="#b7d7c7")
    
    window_height = gv.top_window_y
    window_width = gv.top_window_x
    if gv.platform_os == "Darwin":
        self.topr.resizable(True,True)
        self.topr.minsize(gv.top_window_x,gv.top_window_y)
        self.topr.maxsize(gv.top_window_x,gv.top_window_y)
        
    screen_width = self.topr.winfo_screenwidth()
    screen_height = self.topr.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    self.topr.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    self.cancel2_button = ttk.Button(self.topr, text = "Cancel", command = self.topr.destroy)
    self.cancel2_button.grid(row=0, column = 0, sticky='e', padx=(20,20), pady=(8,8))
    
    self.topr.columnconfigure(0,weight=24)
    self.topr.columnconfigure(1,weight=1)
    
    self.topr.rowconfigure(0,weight=1)
    self.topr.rowconfigure(1,weight=1)
    self.topr.rowconfigure(2,weight=24)
    self.topr.rowconfigure(3,weight=1)
    self.topr.rowconfigure(4,weight=1)
    self.topr.rowconfigure(5,weight=1)
    self.topr.rowconfigure(6,weight=1)
    self.topr.rowconfigure(7,weight=1)
    self.topr.rowconfigure(8,weight=1)
    self.topr.rowconfigure(9,weight=1)
    self.topr.rowconfigure(10,weight=1)
    self.topr.rowconfigure(11,weight=1)
    self.topr.rowconfigure(12,weight=1)
    self.topr.rowconfigure(13,weight=1)
    self.topr.rowconfigure(14,weight=1)
    self.topr.rowconfigure(15,weight=1)
    self.topr.rowconfigure(16,weight=1)
    self.topr.rowconfigure(17,weight=1)
    
    self.date_var = tk.StringVar()
    self.tid_var = tk.StringVar()
    self.type_var = tk.StringVar()
    self.ve_sess_var = tk.StringVar()
    self.ve_sess_list = []
    self.ve_dict = {}
    self.exam_dict = {}
    self.v_exam_sort_key = tk.StringVar()
    self.v_exam_sort_key.set(gv.def_ve_sort_key)
    self.v_exam_sort_dir = True
    
    
    set_gui_vexam(self)
    refresh_exam_screen(self)
    
    
def set_gui_vexam(self):
    
    self.v_exam_DB = ttk.Treeview(self.topr, show='headings', selectmode='browse')
    self.v_exam_DB['columns'] = gv.ve_treeview_cols
    self.v_exam_DB.column('call', width=80, minwidth=80)
    self.v_exam_DB.column('name', width=80, minwidth=80)
    self.v_exam_DB.column('date',width=80,minwidth=80)
    
    self.v_exam_DB.heading('call', text='VE Callsign', anchor='w')
    self.v_exam_DB.heading('name', text='VE name', anchor='w')
    self.v_exam_DB.heading('date', text='Date', anchor='w')
    self.v_exam_DB.bind('<Double-1>', build_ve_list(self))
    self.v_exam_DB.grid(row=2, column=0,sticky='nsew',padx=(20,0),pady=(0,10))
    self.sdbscrollbar = ttk.Scrollbar(self.topr, orient=tk.VERTICAL, command=self.v_exam_DB.yview)
    self.v_exam_DB.configure(yscroll=self.sdbscrollbar.set)
    self.sdbscrollbar.grid(row=2,column=1, sticky='nsw',padx=(2,5),pady=(0,10))
    
    
    self.v_tvframe = tk.Frame(self.topr)
    self.v_tvframe.grid(row=3,column=0,sticky='nsew', padx=20, pady=(0,10))
    
    self.clear3_button = tk.Button(self.v_tvframe, text = 'Clear Selection', bg="#d0ffd0", command = lambda:clear_ve_treeview(self))
    self.clear3_button.grid(row=3, column=0, sticky='nw', padx=(0,8), pady=0)
    self.sess_sort_button = tk.Button(self.v_tvframe, text = 'Sort Direction Toggle', bg="#d0ffd0", command = lambda:toggle_vdir(self))
    self.sess_sort_button.grid(row=3, column=2, sticky='nw',padx=(20,8), pady=0 )
    self.sort_button = tk.Button(self.v_tvframe, text='Sort List', bg="#d0ffd0", command= lambda:refresh_exam_screen(self))
    self.sort_button.grid(row=4, column=1, sticky='ne', padx=(0,8), pady=0)
    self.make_query_button = tk.Button(self.v_tvframe, text = 'NEXT', bg="#ffb020", command = lambda:build_ve_list(self))
    self.make_query_button.grid(row=3, column=1, sticky='ne',padx=(20,8), pady=2)
    ## set up radio buttons for sort
    for fld in gv.rb3_cols:
        self.rb = ttk.Radiobutton(self.v_tvframe, text=fld[0], value=fld[1], variable=self.v_exam_sort_key)
        self.rb.grid(row=4, column=2, sticky='we', padx=fld[2])


def refresh_exam_screen(self):
    v_exam_tree = self.v_exam_DB.get_children()
    
    for node in v_exam_tree:
        self.v_exam_DB.delete(node)
        
    self.examiners = get_v_exam_DB(self)
    ## filter out duplicate callsigns
    uniq_list = []    
    for item in self.examiners:
        tst_item = list(item)
        uniq_flag = True
        try:
            for index in uniq_list:
                if tst_item[1] == index[1]:
                    uniq_flag = False
            if uniq_flag:        
                uniq_list.append(item)
        except:
            if uniq_list == []:
                uniq_list.append(item)
            continue
    ## assign the filtered list to the treeview
    self.examiners =  uniq_list
    
    if self.examiners != None:
        self.examiners.sort(key=lambda tup: tup[int(self.v_exam_sort_key.get())], reverse=self.v_exam_sort_dir)
        
        for exam in self.examiners:
            exam_list = []
            exam_list.append(exam[1]) # 'call'
            exam_list.append(exam[2]) # 'name'
            exam_list.append(exam[3]) # 'date'
            exam_tuple = tuple(exam_list)
            self.v_exam_DB.insert('','end', values=exam_tuple)
        
def clear_ve_treeview(self):
    if len(self.v_exam_DB.selection()) > 0:
        self.v_exam_DB.selection_remove(self.v_exam_DB.selection()[0])

def toggle_vdir(self):
    if self.v_exam_sort_dir:
        self.v_exam_sort_dir = False
    else:
        self.v_exam_sort_dir = True
    refresh_exam_screen(self)

def get_v_exam_DB(self):
    conn = self.db_obj.get_connection()
    curs = self.db_obj.get_cursor()
    message = "SELECT * FROM ves;"
    self.db_obj.set_SQL(message)
    records = self.db_obj.fetch_all_SQL()
    return records

def get_ve_appl_DB(self):
    conn = self.db_obj.get_connection()
    curs = self.db_obj.get_cursor()
    curs.execute("SELECT frn, signingVeCs1, signingVeCs2, signingVeCs3 from applicant WHERE signingVeCs1 = ? OR signingVeCs2 =? OR signingVeCs3 = ?;",[self.vdb_ref_call,self.vdb_ref_call,self.vdb_ref_call])
    selected_ve_list = curs.fetchall()
    return selected_ve_list

def build_ve_list(self):
    ## to hold VE reference data
    self.ve_rpt_dict = {}
    ## hold data to output
    self.vd = {}
    ## helper to extract selected VE data
    ve_reference = {}
    
    _iid = self.v_exam_DB.focus()
    ve_reference = self.v_exam_DB.item(_iid)
    
    self.vdb_ref_call = ""
    self.vdb_ref_name = ""
    self.vdb_ref_id = ""
    try: 
        self.vdb_ref_id = ve_reference['values'][2]
        self.vdb_ref_name = ve_reference['values'][1]
        self.vdb_ref_call = ve_reference['values'][0]
    except:
        ## ignore a 'Next' without selecting first
        return
    
    curs = self.db_obj.get_cursor()
    curs.execute("SELECT * from ves WHERE call = ?",[self.vdb_ref_call])
    ve_session = curs.fetchall()
    
    ## get session stats
    self.vlist = list(ve_session)
    self.vlist.pop(0)
    
    session_dates = []
    for index in self.vlist:
        session_dates.append(list(index)[3])
        
    ## get signature stats
    self.sel_ve_list = get_ve_appl_DB(self)
    
    self.signing_list = []
    
    for index in self.sel_ve_list:
        result = self.vdb_ref_call in index
        if result:
            self.signing_list.append(list(index)[0])
    
    dvr.display_result(self)