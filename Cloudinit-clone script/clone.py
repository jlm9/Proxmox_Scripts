#!/usr/bin/python3.7

import subprocess
import time
import ipaddress
import re

names = []
vmids = []

def types():
	resultcode = 0
	single = input("Do you want to make a single clone (note, you can choose a single clone and also put in a range)?(y/n) ")
	range = input("Do you want to make more than one clone? (note, you can input a range of vmids to create and also input a single vmid to create) (y/n)")

	if single == "y" or single == "yes":
		resultcode+=1
	if range =="y" or range == "yes":
		resultcode+=2
	return resultcode

def cloud_init(oldid):
	print("If you have not installed cloudinit on the vm you want to clone go do that")
	setup = input("Did you set up the cloud init drive on the proxmox hardware tab?(y/n): ").lower()
	template = input("Did you make the vm a template?(y/n): ").lower()
	if (setup == 'yes' or setup == 'y') and (template == 'yes' or template == 'y') :
		print("Great, no further setup needed")
	elif (setup == 'no' or setup == 'n') and (template == 'no' or template == 'n'):
		print("Okay we will create a cloud init drive for the vm and make it a template")
		storage = input("What kind of storage do you use (local-lvm as an example)").lower()
		cloudinit_cmd = 'qm set {} --ide2 {}:cloudinit'.format(oldid, storage)
		template_convert = 'qm template {}'.format(oldid)
		create_cloudinit = subprocess.Popen(cloudinit_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)
		output, error = create_cloudinit.communicate()
		if not error or (error and re.search(r'WARNING', error)):
			convert_to_template = subprocess.Popen(template_convert, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			if re.search(r'WARNING:', error):
				print("There was a warning you might want to see: {}".format(error))
		elif error and not re.search(r'WARNING:', error):
			print("There was an error in creating the cloudinit drive: {}".format(error))
			exit()
	elif (setup == 'yes' or setup == 'y') and (template == 'n' or template == 'n'):
		print("Okay we will convert it to a template")
		template_convert = 'qm template {}'.format(oldid)
		convert_to_template = subprocess.Popen(template_convert, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

def full_clone(oldid):
	if is_confirmed('cloud_init', 0):
		cloud_init(oldid)
		type = input("Do you want to make a linked or full clone? (linked/full) ").lower()
		if type == "full":
			return True, 'cloud_init'
		else:
			return False, 'cloud_init'

	cloning = input("Do you want to clone a template or VM? (VM/template) ").lower()
	print(cloning)
	if cloning == "template" :
		type = input("Do you want to make a linked or full clone? (linked/full) ").lower()
		if type == "full":
			return True, 'no'
		else:
			return False, 'no'
	elif cloning == "vm":
		return True, 'no'
	else:
		print("invalid")
		exit()

def is_confirmed(function, vmid):
	if function == "dolly":
		confirmed = input("Please confirm if {} is the vmid you want to clone (y/n): ".format(vmid))
	elif function == "range":
		confirmed = input("Please confirm if {} is the range you want to create (y/n): ".format(vmid))
	elif function == "single":
		confirmed = input("Please confirm if {} is the vmid you want to create (y/n): ".format(vmid))
	elif function == "final_confirm_vmids":
		print(vmids)
		confirmed = input("Please confirm if these are the vmids you want to create (y/n): ")
	elif function == "final_confirm_names":
		print(names)
		confirmed = input("Please confirm if these are the names of the vmids you want to create (y/n): ")
	elif function == "start":
		confirmed = input("Do you want to start all of the newly created vms?(y/n): ")
	elif function == "disown":
		confirmed = input("Do you want to disown this process? (to survive shell close)? (y/n): ")
	elif function == "cloud_init":
		confirmed = input("Do you want to use cloud init to configure VMs (y/n):").lower()
	if confirmed == 'y' or confirmed == 'yes':
		return True
	else:
		return False

def anotherone(function): #Determines if the user wants to enter in another single vmid, range, or pool
	if function == "single":
		anotherone = input("Do you want to enter in another vmid? (if you want to enter a range or pool say no) (y/n) : ")
	elif function == "range":
		anotherone = input("Do you want to enter in another range? (if you want to enter a single vmid or pool say no) (y/n) : ")
	if anotherone == "no" or anotherone == "n":
		return False
	else:
		return True

def single():

	vmid = input("Please enter the vmid you want to create:")
	while True:
		if is_confirmed("single", vmid) and vmid not in vmids:
			vmids.append(vmid)
		else:
			vmid = input("try again: ")
			continue

		if anotherone("single"):
			vmid = input("Please enter the vmid you want to create: ")
		else:
			break

def get_range():

	begvmid = input("Enter beginning vmid in the range of vmids you want to create: ")
	endvmid = input("Enter the ending vmid in the range you want to create : ")
	range1 = "{}-{}".format(begvmid, endvmid)
	return range1

def use_range():
	while True:
		range1 = get_range()
		while [ i == 0 ]:
			if is_confirmed("range", range1):
				print("triggered")
				break
			else:
				range1 = get_range()
				continue
		range1 = range1.replace("-"," ")
		begvmid = int(range1.partition(' ')[0].strip())
		endvmid = int(range1.partition(' ')[2].strip())
		endvmid+=1
		for vmid in range(begvmid, endvmid):
			if vmid not in vmids:
				vmids.append(vmid)

		if anotherone("range"):
			continue
		else:
			break
def name():
	vmlength = len(vmids)
	print(vmlength)
	for number in range(0,vmlength):
		vmid = vmids[number]
		name = input("Name this vm with vmid {} : ".format(vmid))
		names.append(name)
	
	#namelen = len(vmidnames)

def format():
	format = input("Please select a format<qcow2|raw|vmdk> : ")
	while True:
		if (format == "qcow2" or format == "raw" or format == "vmdk"):
			return format
			break
		else:
			format = input("Invalid input please try again!")

def dolly():
	oldid = int(input("Please input the vmid you want to clone: "))
	while True:
		if is_confirmed("dolly", oldid):
			return oldid
		else:
			oldid = int(input("Try again: "))
			continue

def get_ip_information():
	ip_address_range = input("Please input the ip range you want to set for your vms (cidr is next input)")
	cidr = input("Please input the cidr you want: ")
	ip_list = []
	gateway = input("Please input the gateway for your vms: ")
	nameservers = input("Please input the nameserver for your vms: ")
	ips = ipaddress.IPv4Network('{}/{}'.format(ip_address_range,cidr))
	for ip in ips.hosts():
		if ip != ipaddress.IPv4Address(gateway) and ip != ipaddress.IPv4Address(nameservers):
			finalip = str(ip) + '/' + cidr
			ip_list.append(finalip)

	return ip_list, gateway, nameservers


def qmclone(oldid, full, pool, format):
	print("qmclone triggered")
	vms=0
	counter=0
	for vmid in vmids:
		name = names[counter]
		if full:
			cmd = "nohup qm clone {} {} --full {} --pool {} --format {} --name {}".format(oldid, vmid, full, pool, format, name)
			clone = subprocess.Popen(cmd, shell = True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
			counter+=1
			while True:
				if clone.poll() is None:
					time.sleep(5)
				else:
					break
		elif not full:
			cmd = "nohup qm clone {} {} --full {} --pool {} --name {}".format(oldid, vmid, full, pool, name)
			clone = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			counter+=1
			while True:
				if clone.poll() is None:
					time.sleep(5)
				else:
					break
def customize_machines():
	ip_list, gateway, nameservers = get_ip_information()
	counter = 0
	for vmid in vmids:
		ip = ip_list[counter]
		cmd = "qm set {} --ipconfig0 ip={},gw={} --nameserver {}".format(vmid, ip, gateway, nameservers)
		machine_customization = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		counter+=1

def qm_start():
	vms=0
	for vmid in vmids:
		cmd = "nohup qm start {}".format(vmid)
		start = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		while True:
			if start.poll() is None:
				time.sleep(5)
			else:
				time.sleep(5)
				break

if is_confirmed("disown", 0):
	cmd = "disown -h"
	disown = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

while [ i == 0 ]:

	resultcode= types()

	if resultcode == 1:
		oldid = dolly()
		full, cloudinit = full_clone(oldid)
		pool = input("Please input the pool you want to put the clones in: ")
		single()
		name()
		format = format()

	elif resultcode == 2:
		oldid = dolly()
		full, cloudinit = full_clone(oldid)
		pool = input("Please input the pool you want to put the clones in: ")
		use_range()
		name()
		format = format()

	elif resultcode == 3:
		oldid = dolly()
		full, cloudinit = full_clone(oldid)
		pool = input("Please input the pool you want to put the clones in: ")
		single()
		use_range()
		name()
		format = format()

	if is_confirmed("final_confirm_vmids", 0) and is_confirmed("final_confirm_names", 0):
		break
	else:
		vmids=[]
		names=[]
		cloudinit = None
		pool = None
		format = None

if resultcode != 0:
	print("I got triggered")
	qmclone(oldid, full, pool, format)
else:
	print("Dude, you didn't enter in a type. I'm not even going to bother to code you trying again, rerun the script")
	exit()

if cloudinit == 'cloud_init':
	customize_machines()

if is_confirmed("start",0):
	qm_start()
