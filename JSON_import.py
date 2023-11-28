import pandas as pd
import os
import json
from tkinter import messagebox as mb
import progress as pb
import global_var as gv

def read_JSON_files(self):
    tmp_dir = os.path.join(self.environment,gv.cve_dir) # self.environment is set at beginning of CVE-DB.py
    
    cve_db = gv.cve_database
    ## self.db_obj created in CVE-DB.py and left open
    db_conn = self.db_obj.get_connection()
    db_cur = self.db_obj.get_cursor()
    self.last_file = ""
    self.cur_file = ""
    ## init progress bar widget as a toplevel window
    progress_bar = pb.Progress(self)
    for vec in gv.vec_list:
        dat_dir = os.path.join(tmp_dir,gv.jsn_store+'_'+vec) ## add VEC to directory name
        ## walk through each potential directory
        ## get a list of files
        file_list = os.listdir(dat_dir)
        ## walk through list, one file at a time
        failed_import = []
        for file_line in file_list:
            if len(self.cur_file) > 0:
                self.last_file = self.cur_file
            self.cur_file = file_line
            master_dict = {} ## receives the JSON output
            progress_bar.update_pb()
            
            dat_file = os.path.join(dat_dir,file_line)
            ## open each file
            with open(dat_file,'r') as incoming_data:
                good_import = True
                try:
                    tmp_var = []
                    master_dict = json.load(incoming_data)
                    tmp_var = list(master_dict.keys())
                    ## Look for JSON file from 'sandbox' session
                    if tmp_var == ['DEVDOC']:
                        ## Skip to the next file to be imported
                        break
                    session_dict = {}
                    applicants_list_of_dict = [] ## for session
                    
                    ## build the session dictionary for the database table
                    session_dict['date'] = master_dict['date']
                    try:    
                        session_dict['teamId'] = master_dict['team']['teamId']+'_'+vec
                    except: ## GLAARG did away with the team id, substituting the lead VE callsign
                        session_dict['teamId'] = master_dict['teamLead']['call']+'_'+vec
                    try:    
                        session_dict['type'] = master_dict['type']
                    except:
                        session_dict['type'] = "UNKNOWN"
                    
                    rec_cols = ', '.join(gv.data_json_sess_cols)
                    q_marks = ','.join(list('?'*len(gv.data_json_sess_cols)))
                    values = tuple(session_dict.values())
                    sql = "INSERT INTO session ("+rec_cols+") VALUES ("+q_marks+")"
                    db_cur.execute(sql,values)
                    
                    
                    # make a copy of the list of applicants
                    applicants_list_of_dict = master_dict['applicants'].copy()
                    
                    ## parse each entry
                    for appl in applicants_list_of_dict:
                        ## appl will be a dictionary within the list
                        appl_dict = {}
                        appl_dict['firstname'] = appl['firstname']
                        try:
                            appl_dict['middle'] = appl['middle']
                        except:
                            appl_dict['middle'] = "None"
                        appl_dict['lastname'] = appl['lastname']
                        try:
                            appl_dict['suffix'] = appl['suffix']
                        except:
                            appl_dict['suffix'] = "None"
                        appl_dict['email'] = appl['email']
                        appl_dict['frn'] = appl['frn']
                        appl_dict['callsign'] = appl['callsign']
                        if appl_dict['callsign'] == 'null':
                            appl_dict['callsign'] = " "
                        appl_dict['city'] = appl['city']
                        appl_dict['state'] = appl['state']
                        ## generate exam data
                        ## grab a list of exams. Most of the time will be a single entry
                        ## this code is in case the applicant takes multiple exams
                        ## in the same session
                        exam_list = appl['exams']
                        e2 = ""
                        e3 = ""
                        e4 = ""
                        for exam in exam_list:
                            if exam['type'] == 'credit':
                                if exam['element'] == 2:
                                    e2 += 'C'
                                elif exam['element'] == 3:
                                    e3 += 'C'
                            elif exam['type'] == 'invalid':
                                if exam['element'] == 2:
                                    e2 += 'I'
                                elif exam['element'] == 3:
                                    e3 += 'I'
                            else:
                                ## in the event one takes the element twice
                                ## i.e. Failed the first time and Passed the sencond time
                                ## coding will be "FP"
                                ## if they fail both time, coding will be "FF"
                                if exam['element'] == 2:
                                    if exam['passed']: ## this element is a Boolean
                                        e2 += 'P'
                                    else:
                                        e2 += 'F'
                                elif exam['element'] == 3:
                                    if exam['passed']: ## this element is a Boolean
                                        e3 += 'P'
                                    else:
                                        e3 += 'F'
                                elif exam['element'] == 4:
                                    if exam['passed']: ## this element is a Boolean
                                        e4 += 'P'
                                    else:
                                        e4 += 'F'
                        ## check if element was taken
                        if e2 == "":
                            e2 = 'None'
                        if e3 == "":
                            e3 = 'None'
                        if e4 == "":
                            e4 = 'None'
                        appl_dict['E2'] = e2
                        appl_dict['E3'] = e3
                        appl_dict['E4'] = e4
                        
                        tmp_var_list = master_dict['date'].split('T')
                        appl_dict['sessionDate'] = tmp_var_list[0]
                        
                        ##
                        ## NOTE: if you renamed your team Id, the latest name will be assigned
                        ##
                        try:
                            appl_dict['teamId'] = master_dict['team']['teamId']+"_"+vec
                        except: ## GLAARG did away with the team id, substituting the lead VE callsign
                            appl_dict['teamId'] = master_dict['teamLead']['call']+'_'+vec
                        
                        signing_ve_list = appl['signingVes'].copy()
                        index = 1
                        for ve in signing_ve_list:
                            field = 'signingVeCs'+str(index)
                            appl_dict[field] = ve['call']
                            index += 1
                        
                        ## substitute "NOCALL" for missing VE data
                        while index < 4:
                            if index == 1: ## no signing VE data
                                field = 'signingVeCs'+str(index)
                                appl_dict[field] = "NOCALL"
                                index += 1
                            elif index == 2: ## missing 2 VE signatures
                                field = 'signingVeCs'+str(index)
                                appl_dict[field] = "NOCALL"
                                index += 1
                            elif index == 3: ## missing 1 VE signature
                                field = 'signingVeCs'+str(index)
                                appl_dict[field] = "NOCALL"
                                index += 1
                                
                            
                        
                        appl_dict['date'] = session_dict['date']
                        
                        rec_cols = ', '.join(gv.data_json_appl_cols)
                        q_marks = ','.join(list('?'*len(gv.data_json_appl_cols)))
                        values = tuple(appl_dict.values())
                        sql = "INSERT INTO applicant ("+rec_cols+") VALUES ("+q_marks+")"
                        db_cur.execute(sql,values)
                        
                    ve_dict_list = master_dict['VEs'].copy()
                    for v in ve_dict_list:
                        ve_dict = {}
                        ve_dict['call'] = v['call']
                        ve_dict['name'] = v['name']
                        ve_dict['date'] = session_dict['date']
                        rec_cols = ', '.join(gv.data_ve_cols)
                        q_marks = ','.join(list('?'*len(gv.data_ve_cols)))
                        values = tuple(ve_dict.values())
                        sql = "INSERT INTO ves ("+rec_cols+") VALUES ("+q_marks+")"
                        db_cur.execute(sql,values)
                    ##
                    ## END of opening and reading a JSON file: 'with open(dat_file,'r') as incoming_data:'
                    ##        
                    ## save all the insert actions    
                    db_conn.commit()
                except:
                    failed_import.append(self.cur_file+'\n')
                    good_import = False
                    
            ##
            ## END of processing list of files: 'for file_line in file_list:'
            ##  
            ## remove the file after importing the data
            if good_import:
                os.remove(dat_file) 
            if len(failed_import) > 0:
                mb.showwarning("Warning","Failed to import files:\n"+failed_import)
    ##
    ## END of 'def read_JSON_files(self):'
    progress_bar.close()
    self.refresh_screen()