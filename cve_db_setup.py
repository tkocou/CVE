import os
import sqlite3
import cve_utilities as ut
import global_var as gv


def setup():
    ## get the correct path for working directory
    ## get_environment() only sets up the path
    ## and returns it
    basic_dir = ut.set_environment()
    
    ## Change to correct directory
    os.chdir(basic_dir)
    ## set the flag
    db_result_flag = True
    
    ## set global path to database
    tmp_dir = os.path.join(basic_dir,gv.cve_dir)
    gv.cve_database = os.path.join(tmp_dir,"cve.db")
    
    if os.path.exists(gv.cve_database):
        # do not erase an existing database
        pass
    else:
        # else create a new database
        with open(gv.cve_database,mode="w"):pass

        ## build database ONLY if database did not exist
        
        db_connection = sqlite3.connect(gv.cve_database)
        db_cursor = db_connection.cursor()
        
        ## set parameters of elements in SQL table
        ## date references the timestamp of the session
        ## both tables use the same 'date' data
        ## sessionDate is a short version of date for treeview GUI
        sql = """
                CREATE TABLE IF NOT EXISTS session (id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL, teamId TEXT NOT NULL, type TEXT NOT NULL);
            """
        sql_result = db_cursor.execute(sql)
            
        sql = """
                CREATE TABLE IF NOT EXISTS applicant (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT ,
                middle TEXT , lastname TEXT , suffix TEXT ,
                email TEXT , frn TEXT , callsign TEXT , 
                city TEXT, state TEXT, E2 TEXT, E3 TEXT, E4 TEXT, sessionDate TEXT, teamId TEXT, signingVeCs1 TEXT, signingVeCs2 TEXT, signingVeCs3 TEXT, date TEXT 
                );
            """
        sql_result = db_cursor.execute(sql)
        
        sql = """
                CREATE TABLE IF NOT EXISTS ves (id INTEGER PRIMARY KEY AUTOINCREMENT, call TEXT, name TEXT, 
                date TEXT 
                );
            """
        sql_result = db_cursor.execute(sql)
        
        db_connection.commit()   
            
        db_connection.close()
    ## whether we were successful or not, return a flag
    return db_result_flag

