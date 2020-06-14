#!/usr/bin/python3.7

import subprocess
import sys
import getopt
import time
full_arguments = sys.argv
argument_list= full_arguments[1:]
options = "a:p:s:i:h"
arguments, values = getopt.getopt(argument_list, options)
vmids=[]
iterations = -1
vms = 0
for argument, value in arguments :
	if argument == '-p' :
		pool = value
		#print("I got triggered")
		#print(pool)
	elif argument == '-a' :
		action = value
	elif argument == '-s' :
		sleep = int(value)
	elif argument == '-i' :
		iterations = int(value)
		#print("This is amount of iterations:" , iterations)
		countby = int(value)
	elif argument == '-h' :
		print("Mandatory arguments are: -p (pool) & -a (action). -a can only be start or stop \n Optional arguments: -i (iterations of qm start/stop before pausing to give the server a break) & \n -s (time in seconds for how long to break for). \n For example, ./startstop.py -a start -p example_pool -i 5 -s 10 would start all vms in example_pool and pause every 5 machines for 5 seconds")
		exit()
	else:
		print("invalid argument, type in ./startstop.py -h for help" )
		exit()
index=0
i=0

while [ i == 0 ]:
	cmd= "pvesh get /pools/{} --output-format json | jq '.members[{}] .vmid'".format(pool,index)
	#print(cmd)
	vmid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output, err = vmid.communicate()
	output=output.replace("b","").replace("\n","").strip()
	#print("This is the result", output)
	if output == 'null' :
                break
	if output not in vmids:
		vmids.append(output)
		#print("get in my house")
		index+=1
		#print(index)
	#else:
		#print("Not in my house")
		#print(index)
print("This is the vmid array", vmids)
for vmid in vmids:
	if action == 'stop' :
		cmd = "qm stop {}".format(vmid)
	elif action == 'start' :
		cmd = "qm start {}".format(vmid)
	else :
		print("action must be either start or stop")
		exit()
	subprocess.Popen(cmd, shell=True)
	vms+=1
	#print("vms:", vms)
	#print("This is iterations", iterations)

	if vms == iterations and iterations != -1 :
		print("sleep was triggered")
		time.sleep(sleep)
		iterations = iterations + countby
