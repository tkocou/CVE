## program vars
program = "CVE Session Management"
version = "0.95.4"

root_size_x = 1024
root_size_y = 600
top_window_x = 1024
top_window_y = 600
platform_os = ""

## variables which can span more than one source file
base_dat_dir = ""
base_csv_dir = ""
base_rpt_dir = ""
base_jsn_dir = ""
first_pass = True
cve_dir = "CVE"
dat_store = "DAT"
csv_store = "CSV"
jsn_store = "JSON"
report_dir = "REPORTS"
## path to the database file which is set in 'cve_db_setup.py'
cve_database = ""

csv_common_cols = ['firstname','middle','lastname','suffix','email','frn','callsign','city','state']
## columns displayed in right panel of GUI
appl_treeview_cols = ('index','frn','sessionDate','teamId')
## default sort key -> sessionDate
def_sort_key = '13'
## radio button parameters based on sort of 'appl_treeview_cols'
rb_cols = [('index','0',0),('frn','6',60),('Date','13',102),('Id','14',160)] # used in CVE-DB.py
## reverse lookup dictionary
field_dict = {'0':'firstname','1':'middle','2':'lastname','3':'suffix','4':'email','5':'frn','6':'callsign','7':'city','8':'state','9':'E2','10':'E3','11':'E4','12':'sessionDate','13':'teamId'} # used in do_sql_query.py
## template for SQL variables
flag_dict = {'firstname':"",'middle':"",'lastname':"",'suffix':"",'email':"",'frn':"",'callsign':"",'city':"",'state':"",'E2':"",'E3':"",'E4':"",'sessionDate':"",'teamId':""}

#### New database tables for JSON
data_json_appl_cols = ['firstname','middle','lastname','suffix','email','frn','callsign','city','state','E2','E3','E4','sessionDate','teamId','signingVeCs1','signingVeCs2','signingVeCs3','date'] ## sessionDate is a short version of date for treeview GUI
data_json_sess_cols = ['date','teamId','type']
appl_field_dict = {'0':'firstname','1':'middle','2':'lastname','3':'suffix','4':'email','5':'frn','6':'callsign','7':'city','8':'state','9':'E2','10':'E3','11':'E4','12':'sessionDate','13':'teamId','14':'signingVeCs1','15':'signingVeCs2','16':'signingVeCs3','17':'date'}
appl_flag_dict = {'firstname':"",'middle':"",'lastname':"",'suffix':"",'email':"",'frn':"",'callsign':"",'city':"",'state':"",'E2':"",'E3':"",'E4':"",'sessionDate':"",'teamId':"",'signingVeCs1':"",'signingVeCs2':"",'signingVeCs3':"",'date':""}
data_appl_cols = ['firstname','middle','lastname','suffix','email','frn','callsign','city','state','E2','E3','E4','sessionDate','teamId','date']  ## no signing VEs, for use in listbox in CVE-DB.py
data_appl_cols_listbox = ['firstname','middle','lastname','suffix','email','frn','callsign','city','state','E2','E3','E4','sessionDate','teamId']
sess_field_dict = {'0':'date','1':'teamId','2':'type'}
data_ve_cols = ['call','name','date']
ve_field_dict = {'0':'call','1':'name','2':'date'}

## session report fields
sess_treeview_cols = ('date','teamId','type')

rb2_cols = [('date','1',20),('teamId','2',80),('type','3',140)]
def_sess_sort_key = '1'

vec_list = ['ANCHORAGE','ARRL','CAVEC','GLAARC','JEFFERSON-ARC','LAUREL','SANDARC','W4VEC','W5YI']

ve_treeview_cols = ('call','name','date')

rb3_cols = [('call','1',20),('name','2',80),('date','3',140)]
def_ve_sort_key = '1'