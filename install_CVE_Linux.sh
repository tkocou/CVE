#!/usr/bin/env bash
## The script is written for a Linux Mint / Ubuntu / Debian system
## feel free to alter it as you need to

echo "This script is derived from a script written by ParisNeo"
echo "It is used with the permission of ParisNeo (https://github.com/ParisNeo/lollms-webui)"

sleep 2

if ping -q -c 1 google.com >/dev/null 2>&1; then
    echo -e "\e[32mInternet Connection working fine\e[0m"
    # Install git
    echo -n "Checking for Git..."
    if command -v git > /dev/null 2>&1; then
      echo "is installed"
    else
      read -p "Git is not installed. Would you like to install Git? [Y/N] " choice
      if [ "$choice" = "Y" ] || [ "$choice" = "y" ] ; then
        echo "Installing Git..."
        sudo apt update
        sudo apt install -y git
      else
        echo "Please install Git and try again."
        exit 1
      fi
    fi
    ## some other packages which should be installed
    sudo apt update
    sudo apt -y install python3 python-is-python3 python3-tk
    pip install croniter pandas html5lib bs4 markdown tcl

    ## move to the $HOME directory
    cd ~

    # Check if git directory exists
    if [[ -d ~/CVE/.git ]] ; then
        cd ./CVE
        echo Pulling latest changes
        git pull

    ## Check if we have an older ASC installation
    elif  [[ -d ~/CVE ]] ; then
        echo Saving database and removing old installation
        cp ./CVE/cve.db .
        rm -rf ./CVE
        git clone https://github.com/tkocou/CVE ./CVE
        mv ./cve.db ./CVE
        
    ## no ASC, then clone the repository
    else
        echo Cloning repository...
        git clone https://github.com/tkocou/CVE ./CVE
    fi
else
    echo -e "\e[32mMissing an Internet Connection\e[0m"
fi

## Check if repository has already been cloned
## regardless if there is an Internet Connection
if [ -f ~/CVE/CVE-DB.py ] ;then
    cd ~/CVE
    # Launch the Python application
    python CVE-DB.py &
fi

## The Linux desktop should now have a launcher installed
