# Start Up or Shut Down all Vms in a pool

Use this script to start up or shut down all VMs in a pool. This script was tested on 3.7, it is unknown if this script runs on other versions of Python.

## Installation
git clone https://github.com/jlm9/Proxmox_Scripts.git  
chmod +x startstop.py  
pip install -r requirements.txt (requirements.txt is a work in progress)

## Usage
There are two arguments:  
-a action  
-p pool  
  
possible actions are:   
start    
stop

Example usage: ./startstop.py -p test_pool -a start
