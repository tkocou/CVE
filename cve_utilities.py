import os
import base64
import bz2
import platform
import shutil

import global_var as gv
import icons_array as ia 

cve_dir = ""
home_dir = os.path.expanduser('~')
basic_dir = ""
gv.platform_os = platform.system()
sys_platform = gv.platform_os

def set_environment():
    global cve_dir, home_dir, basic_dir
    ### Some code to accomodate the development environment
    ### leaving this in should not affect the production version

    basic_dir = os.getcwd()
    project_dir = basic_dir[-8:]

    ## Is the program running in my development environment?
    ##
    ## Build correct path to working directory and save as a global
    ## That way the correct path can be referenced elsewhere
    ##
    ## The flag 'first_pass' is set to true in 'global_var.py' at start of program
    if gv.first_pass:
        if project_dir == "Projects":
            ## Build a path referencing the home dir
            cve_dir = os.path.join(basic_dir,gv.cve_dir)
            project2_dir = os.path.join(cve_dir, gv.csv_store)
            gv.base_csv_dir = os.path.join(home_dir, project2_dir)
            project3_dir = os.path.join(cve_dir, gv.report_dir)
            gv.base_rpt_dir = os.path.join(home_dir, project3_dir)
            project4_dir = os.path.join(cve_dir, gv.jsn_store)
            gv.base_jsn_dir = os.path.join(home_dir, project4_dir)
            ## while the program is running, set 'first_pass' to False
            gv.first_pass = False
            
        elif project_dir != "Projects":
            basic_dir = home_dir
            cve_dir = os.path.join(home_dir,gv.cve_dir)
            gv.base_csv_dir = os.path.join(cve_dir, gv.csv_store)
            gv.base_jsn_dir = os.path.join(cve_dir, gv.jsn_store)
            gv.base_rpt_dir = os.path.join(cve_dir, gv.report_dir)
            ## while the program is running, set 'first_pass' to False
            gv.first_pass = False
        else:
            pass
        
        ## Create the CVE directory
        try:
            os.mkdir(cve_dir)
        except: ## directory already exists, do nothing
            pass
    
        ## Create the CSV holding directory path
        try:
            os.mkdir(gv.base_csv_dir)
        except: ## directory already exists, do nothing
            pass
        
        try:
            os.mkdir(gv.base_rpt_dir)
        except: ## directory already exists, do nothing
            pass
        
        for vec in gv.vec_list:
            try:
                os.mkdir(gv.base_jsn_dir+'_'+vec)
            except: ## directory already exists, do nothing
                pass
    
        make_launcher()
        
    ## return that path
    return basic_dir

def make_launcher():
    global cve_dir, home_dir, basic_dir
    
     ## Path to Desktop
    desktop_dir = os.path.join(home_dir,"Desktop")
    
    file_dict={'licon':"database.svg",'wicon':"database.ico",'wdesk':"CVE-DB.lnk"}
    
    keys = file_dict.keys()
    for key in keys:
        file_name = os.path.join(cve_dir,file_dict[key])
        string_data = ia.local_array[key]
        byte_data = bytes(string_data,'utf-8')
        decoded_data = base64.b64decode(byte_data)
        bin_data = bz2.decompress(decoded_data)
        with open(file_name,"wb") as f:
            f.write(bin_data)
    
    if sys_platform == "Windows":
        link_file = file_dict['wdesk']
        launcher_file = os.path.join(cve_dir,link_file)
        launcher_dest = os.path.join(desktop_dir,link_file)
        if not os.path.exists(launcher_dest):
            shutil.copy2(launcher_file,launcher_dest)
            
    elif sys_platform  == "Linux":
        ## let's create a desktop launcher
            launcher = "CVE-DB.desktop"
            desktop_launcher_path = os.path.join(desktop_dir,launcher)
            ## get the path towhere js8msg2 is executing from
            exec_path = os.path.join(home_dir,"bin/CVE-DB")
            icon_picture_path = os.path.join(cve_dir,"database.svg")
            ## updating launcher internals
            with open(desktop_launcher_path, "w") as fh:
                fh.write("[Desktop Entry]\n")
                fh.write("Version="+gv.version+"\n")
                fh.write("Type=Application\n")
                fh.write("Terminal=false\n")
                fh.write("Icon="+icon_picture_path+'\n')
                fh.write("Icon[en_US]="+icon_picture_path+'\n')
                fh.write("Name[en_US]=CVE-DB\n")
                fh.write("Exec="+exec_path+'\n')
                fh.write("Comment[en_US]="+gv.program+"\n")
                fh.write("Name=CVE-DB\n")
                fh.write("Comment="+gv.program+"\n")
            os.chmod(desktop_launcher_path,0o755)
