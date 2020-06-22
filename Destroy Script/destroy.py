#!/usr/bin/python3.7

import subprocess
import time
import numpy as np
import re
vmids = [] #array for vmids
exceptions = []
i = 0 #infinite loop fun :)

def type(): # Function determines what type of input the user wants to put in
	resultCode = 0
	pool = input("Would you like to input a pool? (y/n)")
	range = input("Would you like to input a vmid range? (y/n)")
	single = input("Would you like to input a single vmid? (y/n)")
	if single == "y" or single == "yes":
		resultCode+=1
	if range == "y" or range == "yes":
		resultCode+=2
	if pool == "y" or pool == "yes":
		resultCode+=4
	return resultCode

def is_confirmed(function, vmid, times_ran): # Function asks the user if there were any input errors. The times_ran was to distinguish between beginning vmid, ending vmid, and the resulting range in the range function
	if function == "single":
		confirmed = input("Please confirm if {} is the vmid you want to destroy (y/n) : ".format(vmid))
	elif function == "range" and times_ran == 0:
		confirmed = input("Please confirm if {} is the beginning vmid of the range you want to destroy (y/n) : ".format(vmid))
	elif function == "range" and times_ran == 1:
		confirmed = input("Please confirm if {} is the end vmid of the range you want to destroy (y/n) : ".format(vmid))
	elif function == "range" and times_ran == 2:
		confirmed = input("Please confirm if {} is the range you want to destroy (y/n) : ".format(vmid))
	elif function == "pool" and times_ran == 3:
		confirmed = input("Please confirm if {} is the pool you want to destroy (y/n) : ".format(vmid))
	elif function == "final_confirm" and times_ran == 3:
		print(sorted(vmids))
		confirmed = input("Please confirm if this list of vmids is accurate, if it is not this is your last chance to cancel (don't worry about duplicate values, this program cleans the list (y/n): ")
	elif function == "iterations" and times_ran == 3:
		confirmed = input("Please confirm if after every {} vms you want the script to break (y/n) : ".format(vmid))
	elif function == "sleep" and times_ran == 3:
		confirmed = input("Please confirm if {} seconds is the amount of time the script breaks after your iterations hit (y/n) : ".format(vmid))
	elif function == "exception" and times_ran == 3:
		confirmed = input("Please confirm if you want to exclude {} from destruction (y/n) ".format(vmid))

	if confirmed == 'yes' or confirmed == 'y':
		return True
	else:
		return False

def anotherone(function): #Determines if the user wants to enter in another single vmid, range, or pool
	if function == "single":
		anotherone = input("Do you want to enter in another vmid? (if you want to enter a range or pool say no) (y/n) : ")
	elif function == "range":
		anotherone = input("Do you want to enter in another range? (if you want to enter a single vmid or pool say no) (y/n) : ")
	elif function == "pool":
		anotherone = input("Do you want to enter in another pool? (if you want to enter a single vmid or range say no) (y/n) : ")
	elif function == "exception":
		anotherone = input("Do you want to enter in another exception? (y/n) ")
	if anotherone == "no" or anotherone == "n":
		return False
	else:
		return True

def single(): #Takes user input for single vmid and adds it to the vmids array 
    vmid = int(input("Please enter the vmid you want to destroy : "))

    while [ i == 0 ]:
        if is_confirmed("single", vmid, 0) and vmid not in exceptions: #confirms with user if input is correct, if not has them enter it again
            vmids.append(vmid)
            break
        else:
            vmid = int(input("Try again : "))
            continue
        
    while [ i == 0 ]:
        if anotherone("single"):
            vmid = int(input("Please enter the vmid you want to destroy : "))

            while [ i == 0 ]:
                if is_confirmed("single", vmid, 0) and vmid not in exceptions:
                    vmids.append(vmid)
                    break
                else:
                    vmid = int(input("Try again: "))
                    continue
        else:
            break

def get_range():
    #Determines range of vmids user wants to destroy and returns it
	begvmid = input("Please enter the beginning vmid in the range you want to destroy : ")
	while [ i == 0 ]:
		if is_confirmed("range", begvmid, 0):
			break
		else:
			begvmid = input("Try again: ")
			continue

	endvmid = input("Please enter the ending vmid in the range you want to destroy : ")

	while [ i == 0 ]:
		if is_confirmed("range", endvmid, 1):
			break
		else:
			endvmid = input("Try again: ")
			continue
	range1 = "{}-{}".format(begvmid, endvmid)

	return range1

def use_range():
    # It would have been a lot of code to do what I did for the single function so I split the confirmation into another function
	range1 = get_range()
	while [ i == 0 ]:
		if is_confirmed("range", range1, 2):
			break
		else:
			range1 = get_range()
			continue
	range1 = range1.replace("-"," ")
	begvmid = int(range1.partition(' ')[0].strip())
	endvmid = int(range1.partition(' ')[2].strip())
	endvmid+=1

	for vmid in range(begvmid, endvmid):
		if vmid not in exceptions:
			vmids.append(vmid)

def range_loop():
    # Third function to process if the user wants to enter in another range
	while [ i == 0 ]:
        	if anotherone('range'):
                	use_range()
        	else:
                	break

def pool():
	#Takes user input for pool name and determines what vmids are in a pool. 
    pool = input("What pool do you want to destroy?(Note this destroys the vmids in the pool not the pool itself): ")
    index = 0
    pool_list = []

    while [ i == 0 ]:
        if is_confirmed("pool", pool, 3):
            break
        else:
            pool = input("Try again: ")
            continue
        
    while [ i == 0 ]:
        cmd = "pvesh get /pools/{} --output-format json | jq '.members[{}] .vmid'".format(pool, index)
        vmid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        output, err = vmid.communicate()
        output = output.replace("b","").replace("\n","").strip()

        if output == 'null':
            break
        else:
            output = int(output)
            if output not in pool_list:
                index+=1
                if output not in exceptions:
                	pool_list.append(output)
                
    for vmid in pool_list :
        vmids.append(vmid)

def pool_loop():
    #Determines if the user wants to input another pool name 
	while [ i == 0 ]:
		if anotherone("pool"):
			pool()
		else:
			break
def exception():
# Determines if the user wants to exclude a vm from destruction (if they enter a range, this protects the vm from getting destroyed)
	want_it = input("Do you want to enter a vmid to exclude from destruction (helpful if there are one or two vmids in a range you want to keep) (y/n) :")
	if want_it == "yes" or want_it == "y":
		exception = int(input("Please enter in the vmid you want to exclude : "))
		
		while [ i == 0 ]:
			if is_confirmed("exception", exception, 3):
				exceptions.append(exception)
				break
			else:
				exception = int(input("Try again: "))
		
		while [ i == 0]:
			if anotherone("exception"):
				exception = int(input("Please enter in the vmid you want to exclude : "))
				while [ i == 0]:
					if is_confirmed("exception", exception, 3):
						exceptions.append(exception)
						break
					else:
						exception = int(input("Try again : "))
						continue
			else:
				break
def stop(iterations, sleep):
	#stops all vms that are not already stopped so that they can be destroyed
    vmids_numpy = np.array(vmids)
    vms = 0

    for vmid in np.unique(vmids_numpy):
        cmd = "qm status {}".format(vmid)
        status = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, error = status.communicate()
        output = output.replace("b","").replace("\n","").strip()
        
        if output == "status: running" and iterations == 0:
            cmd = "qm stop {}".format(vmid)
            stopit = subprocess.Popen(cmd, shell=True)
            
        elif output == "status: running" and iterations > 0:
            cmd = "qm stop {}".format(vmid)
            stopit = subprocess.Popen(cmd, shell=True)
            vms+=1

            if iterations == vms:
                iterations = countby + iterations
                time.sleep(sleep)

        elif re.search(r'does not exist', error) and iterations == 0:
                cmd = "pct status {}".format(vmid)
                status = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                output, error = status.communicate()
                output = output.replace("b","").replace("\n","").strip()

                if output == "status: running":
                    cmd = "pct stop {}".format(vmid)
                    stopit = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    output, error = stopit.communicate()

                elif re.search(r'does not exist', error):
                    print("No such vmid. skipping {}".format(vmid))

        elif  re.search(r'does not exist', error) and iterations > 0:
            cmd = "pct status {}".format(vmid)
            status = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output, error = status.communicate()
            output = output.replace("b","").replace("\n","").strip()

            if output == "status: running":
                cmd = "pct stop {}".format(vmid)
                stopit = subprocess.Popen(cmd, shell=True)
                vms+=1

                if iterations == vms:
                    iterations = countby + iterations
                    time.sleep(sleep)

            elif re.search(r'does not exist', error):
                print("No such vmid, skipping {}".format(vmid))

def purge(): #comment this out if your proxmox version does not support this
	purge = input("Do you want to purge the VM from all backup cron jobs? (y/n) ")
	if purge == 'yes' or purge == 'y':
		purge = 'true'
		return purge
	else:
		purge = 'false'
		return purge

def destroy(iterations, sleep, purge): #Delete purge parameter if your proxmox version does not support this
    # Destroys the vmids, runs after stop
    vmids_numpy = np.array(vmids)
    vms = 0

    for vmid in np.unique(vmids_numpy):
        cmd = "qm destroy {} --purge {}".format(vmid, purge) # Delete purge if your proxmox version does not support this.
        if iterations == 0:
            destruction = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output, error = destruction.communicate()

            if re.search(r'does not exist', error):
                cmd = "pct destroy {} --purge {}".format(vmid, purge)
                destruction = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                if re.search(r'does not exist', error):
                    print("No such vmid, skipping {}".format(vmid))

        elif iterations > 0:
            destruction = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output, error = destruction.communicate()

            if re.search(r'successfully removed', output):
                vms+=1
                if iterations == vms:
                    time.sleep(sleep)
                    iterations = iterations + countby

            elif re.search(r'does not exist', error):
                cmd = "pct destroy {} --purge {}".format(vmid, purge)
                destruction = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                output, error = destruction.communicate()

                if re.search(r'successfully removed', output):
                    vms+=1
                    if iterations == vms:
                        time.sleep(sleep)
                        iterations = iterations + countby

                elif re.search(r'does not exist', error):
                    print("No such vmid, skipping {}".format(vmid))
                    

def iterations():
    #determines if the user wants to input iteration counts, if not iteration=0
	Want_iterations = input("Please indicate whether or not you want to pause this script for every x amount of vms destroyed (helps prevent shell crashing) (y/n): ")

	if Want_iterations == 'yes' or Want_iterations == 'y':
		iterations = int(input("Ok, how many vms do you want to stop before forcing a script pause?: "))

		while [ i == 0 ]:
			if is_confirmed("iterations", iterations, 3):
				return iterations
				break

			else:
				iterations = int(input("Try again: "))
				continue
	else:
		iterations = 0
		return iterations

def goto_sleep(number):
    #Takes user input on amount of seconds the script sleeps for. If iterations is 0 returns sleep of 0.
	if number > 0:
		sleep = int(input("How long in seconds do you want to pause the script every {} iterations? ".format(number)))
		while [ i == 0 ]:
			if is_confirmed("sleep", sleep, 3):
				return sleep
				break
			else:
				sleep = int(input("Try again: "))
				continue
	else:
		sleep = 0
		return sleep

while [ i == 0]:
	resultCode = type() #Determines what the user wants to input
	exception()
	print(exceptions)
	if resultCode == 7:
		single() #single has resultcode of 1
		use_range() # range has resultcode of 2
		range_loop()
		pool() #pool has resultcode of 4
		pool_loop() 

	elif resultCode == 6:
		use_range()
		range_loop()
		pool()
		pool_loop()

	elif resultCode == 5:
		pool()
		pool_loop()
		single()

	elif resultCode == 4:
		pool()
		pool_loop()

	elif resultCode == 3:
		single()
		use_range()
		range_loop()

	elif resultCode == 2:
		use_range()
		range_loop()

	elif resultCode == 1:
		single()

	if is_confirmed("final_confirm", 0, 3):
		break

	else:
		print("Okay, let's go through the process again")
		vmids = [] # resets the array, allows the user to reset the process
		continue

iterations = iterations()
countby = iterations #determines when to make script sleep
sleep = goto_sleep(iterations)
stop(iterations, sleep)
destroy(iterations, sleep, purge()) #delete purge if your version does not support it.
