#!/usr/bin/env python3

import sys
import re
from pwinput import pwinput
from urllib import request
from os.path import exists, isfile

pylips_url = "https://raw.githubusercontent.com/eslavnov/pylips/master/pylips.py"

def main():
	if (exists("pylips.py") == False) or (isfile("pylips.py") == False):
		download_pylips()
	if (exists("settings.ini") == False) or (isfile("settings.ini") == False):
		config()
	
	while 1:
		x = input("phucker> ")
		process_input(x)

def process_input(input):
	# too bad we don't have switch-case in python :^)
	if input == "exit":
		sys.exit(0)

def download_pylips():
	print("[*] pylips.py not found, downloading...")
	try:
		request.urlretrieve(pylips_url, "pylips.py")
	except:
		print("[!] Failed to download pylips.py, check your internet connection and try again.")
		sys.exit(1)

def config():
	use_mqtt = ask_yesno("Do you want to use MQTT? [no] ")
	if (use_mqtt == "True"):
		mqtt_listen = ask_yesno("Do you wish to listen to MQTT commands? [no] ")
		mqtt_update = ask_yesno("Do you wish to publish status updates over MQTT? [no] ")
		mqtt_host = ask_ip("Enter MQTT broker's IP Address: ")
		mqtt_port = ask_port("Enter MQTT broker's port: ")
		mqtt_user = input("Enter your MQTT Username: ")
		# TODO: Make this not output anything (or at least stars)
		mqtt_pass = pwinput(prompt="Enter your MQTT Password: ", mask="*")
		mqtt_tls = ask_yesno("Do you wish to use TLS? [no] ")
		if (mqtt_tls == "True"):
			mqtt_cert = input("Enter full path to your certificate: ")
		else:
			mqtt_cert = ""
	else:
		mqtt_listen = "False"
		mqtt_update = "False"
		mqtt_host = ""
		mqtt_port = ""
		mqtt_user = ""
		mqtt_pass = ""
		mqtt_tls = "False"
		mqtt_cert = ""
	
	tv_host = ask_ip("Enter TV's IP Address: ")
	
	cfg_buffer = "[DEFAULT]\r\n"
	cfg_buffer += "verbose = True\r\n"
	cfg_buffer += "MQTT_listen = " + mqtt_listen + "\r\n"
	cfg_buffer += "MQTT_update = " + mqtt_update + "\r\n"
	cfg_buffer += "num_retries = 3\r\n"
	cfg_buffer += "update_interval = 2\r\n"
	cfg_buffer += "[TV]\r\n"
	cfg_buffer += "host = " + tv_host + "\r\n"
	cfg_buffer += "port = \r\n"
	cfg_buffer += "apiv = \r\n"
	cfg_buffer += "user = \r\n"
	cfg_buffer += "pass = \r\n"
	cfg_buffer += "protocol = \r\n"
	cfg_buffer += "ambihue_node = \r\n"
	cfg_buffer += "[MQTT]\r\n"
	cfg_buffer += "host = " + mqtt_host + "\r\n"
	cfg_buffer += "port = " + mqtt_port + "\r\n"
	cfg_buffer += "user = " + mqtt_user + "\r\n"
	cfg_buffer += "pass = " + mqtt_pass + "\r\n"
	cfg_buffer += "TLS = " + mqtt_tls + "\r\n"
	cfg_buffer += "cert_path = " + mqtt_cert + "\r\n"
	cfg_buffer += "topic_pylips = \r\n"
	cfg_buffer += "topic_status = \r\n"

	f = open("settings.ini", "w")
	f.write(cfg_buffer)
	f.close()

def ask_yesno(prompt):
	while 1:
		ret = input(prompt)
		if ret.lower() == "yes":
			return "True"
		elif ret.lower() == "no" or ret.lower() == "":
			return "False"
		else:
			print("Please answer 'yes' or 'no'.\n")

def ask_port(prompt):
	while 1:
		ret = input(prompt)
		if ret.isnumeric() and (ret > 0 and ret < 65536):
			return ret
		else:
			print("Supplied port has invalid value.\n")

def ask_ip(prompt):
	while 1:
		ret = input(prompt)
		ip_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
		
		if (re.search(ip_regex, ret)):
			return ret
		else:
			print("Supplied IP address is invalid.\n")

if __name__ == "__main__":
	main()
