#!/usr/bin/env python3

import sys
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
	# To be done

if __name__ == "__main__":
	main()
