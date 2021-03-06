# Proxmox Destroy Script  
  
## Information  
This script is designed to make it easier to mass destroy virtual machines on a Proxmox server. It is interactive and confirms that the vmid value is correct at every step of the way in order to ensure that the user does not accidently destroy something important. You can specify a pool to destroy, a range of vmids to destroy, and a single vmid to destroy. It also allows you to input as many as each type as you like. The purge option is not available on certain deployments of proxmox. If this happens, comment out the purge information on the script (comments show you where to do this).  
  
  ## FAQS (Even though it was just created and there's been no questions)    
  1. Do I have to stop all the vms I want to destroy first? Answer: Nope! This script has a function that stops all VMs the user inputed before destroying them.  
  2. Does it support destroying containers? Answer: Yes! If the qm status/destroy command fails it tries to use the pct command (the command for containers) to accomplish the task.   
  3. Can I input a range, a pool, & a single vmid at once? Answer: Yeah! Follow the prompts and it will guide you through that process.  
  4. What is with these iterations and sleep options? Answer: It allows you to pause the script between x amount of vms stopped & destroyed. This helps to prevent shell crashing (Don't worry, even without it you will not damage your server in any way)  
  
  ## Installation
  pip3 install -r requirements.txt  
  chmod +x destroyscript.py
  apt-get install jq  
  Make sure you check if your server has the --purge option on the qm destroy command. If not, refer to the script comments to comment out all mentions of --purge.  
  If you want to have less input, get rid of all calls to is_confirmed function (Not Recommended).      
  Recommendation: You can install screen (apt-get install screen) and run the script using screen. Then press ctrl-a then the d key to detach the screen session after all inputs have been completed. Then you can log out and it will still run.
Note: This was tested with python 3.7, it is unknown if it works with lower.  
   Disclaimer: Please ensure you read the confirmations, this is a destructive script.
