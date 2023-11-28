##
## JS8msg is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
## 
## a class object to handle all sql processing
import sqlite3


class DB_object():

    ## When we create a new object, we pass the database file name to this class
    ## The reason for the set* and exec* methods is for assisting with debugging.
    ## 'db_file' is a string
    
    def __init__ (self,db_file):
        super().__init__()
        
        self.sql_result = None
        self.db_file = db_file
        
        ## init a handler for SQL messages
        try:
            self.SQL_message = ""
            self.conn = sqlite3.connect(self.db_file)
            ## FOREIGN KEYS not supported
            self.cur = self.conn.cursor()
            return None
        except:
            return sqlite3.DatabaseError
        
    def get_connection(self):
        ## return the connection handler for the opened database
        return self.conn
    
    def get_cursor(self):
        ## return the SQL cursor for the opened database
        return self.cur
        
    def set_SQL(self, message):
        ## 'message' will be a SQL command string
        self.SQL_message = message

    
    def exec_SQL(self):
        ## this method is when you want to do selective inserting or replacing
        ## kind of a SQL 'catch-all' method
        try:
            self.sql_result = self.cur.execute(self.SQL_message)
            self.conn.commit()
            return self.sql_result
        except:
            ## return SQL error
            return self.sql_result
        
    def fetch_all_SQL(self):
        try:
            self.cur.execute(self.SQL_message)
            self.sql_result = self.cur.fetchall()
            return self.sql_result
        except:
            ## return SQL error
            return self.sql_result
        
    def fetch_once_SQL(self):
        try:
            self.cur.execute(self.SQL_message)
            self.sql_result = self.cur.fetchone()
            return self.sql_result
        except:
            ## return SQL error
            return self.sql_result
        
    
    def close_SQL(self):
        self.conn.close()