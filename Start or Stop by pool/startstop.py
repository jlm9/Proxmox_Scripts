#!/usr/bin/python3.7

import subprocess
import sys
import getopt

full_arguments = sys.argv
argument_list= full_arguments[1:]
options = "a:p:"
arguments, values = getopt.getopt(argument_list, options)
vmids=[]
for argument, value in arguments :
	if argument == '-p' :
		pool = value
		print("I got triggered")
		print(pool)
	elif argument == '-a' :
		action = value
	else:
		print("invalid argument, use -a (start or stop) & -p (pool)")
		exit()
index=0
i=0

while [ i == 0 ]:
	cmd= "pvesh get /pools/{} --output-format json | jq '.members[{}] .vmid'".format(pool,index)
	print(cmd)
	vmid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output, err = vmid.communicate()
	output=output.replace("b","").replace("\n","").strip()
	print("This is the result", output)
	if output == 'null' :
                break
	if output not in vmids:
		vmids.append(output)
		print("get in my house")
		index+=1
		print(index)
	else:
		print("Not in my house")
		print(index)
	print("This is the vmid array", vmids)
print("This is the vmid array", vmids)
for vmid in vmids:
	if action == 'stop' :
		cmd = "qm stop {}".format(vmid)
	elif action == 'start' :
		cmd = "qm start {}".format(vmid)
	else :
		print("action must be either start or stop")
		exit()
	process = subprocess.Popen(cmd, shell=True)

